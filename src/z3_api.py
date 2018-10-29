import re
from z3 import *
import my_constant
import my_util

class Z3_api:

    smt_solver = None

    """
    @ param postfix_expr(List)
    @ return infix expression
    @ involve transform postfix(list) expression into infix one(input for z3)
    """
    def judge_equality_for_statments(self, statement_one, statement_two):

        # help_simplify()
        # statement_one = simplify(statement_one, elim_and = True)
        # print statement_one
        # statement_two = simplify(statement_two, elim_and = True)
        # print statement_two
        if statement_one == statement_two:
            is_equal = True
        elif statement_one is None or statement_two is None:
            is_equal = False
        else:
            if Z3_api.smt_solver is None:
                Z3_api.smt_solver = Solver()
            Z3_api.smt_solver.push()
            # if sat then can be different then unequal
            Z3_api.smt_solver.add(Xor(statement_one, statement_two))
            status = Z3_api.smt_solver.check()
            status_r = status.r
            # sat
            if status_r == 1:
                is_equal = False
            # unsat
            elif status_r == -1:
                is_equal = True
            else:
                print 'unknow status %s, r %d' %(status, status_r)
            Z3_api.smt_solver.pop()
        return is_equal

    """
    @ param postfix_expr(List)
    @ return infix expression
    @ involve transform postfix(list) expression into infix one(input for z3)
    """
    def get_infix_for_postfix(self, postfix_expr):
        infix_expr = []
        for token in postfix_expr:
            if token in ['==', '>', '>=', '!=', '<', '<=', '&&', '||']:
                op_right = infix_expr.pop()
                op_left = infix_expr.pop()
                result = self.__get_infix_for_binary_operator(token, op_left, op_right)
                if result is None:
                    return None
                infix_expr.append(result)
            elif token == '!':
                op = infix_expr.pop()
                result = self.__get_infix_for_unary_operator(op)
                infix_expr.append(result)
            elif token != my_constant.JOERN_UNARY_OPERATOR:
                infix_expr.append(token)
        # check result[postfix without operator]
        if len(infix_expr) == 0:
            return None
        else:
            return self.__normalize_operand(infix_expr.pop())

    """
    @ param operand
    @ return infix expression
    @ involve deal with !, Not(op)
    """
    def __get_infix_for_unary_operator(self, operand):
        # !p normalized to Not(p == null)
        operand = self.__normalize_operand(operand)
        return Not(operand)

    """
    @ param operand left and right
    @ return infix expression
    @ involve deal with binary operator (==, >, >=) (&&, or)
    """
    def __get_infix_for_binary_operator(self, op, op_left, op_right):

        if op == '&&':  
            op_left = self.__normalize_operand(op_left)
            op_right = self.__normalize_operand(op_right)
            return And(op_left, op_right)
        elif op == '||':
            op_left = self.__normalize_operand(op_left)
            op_right = self.__normalize_operand(op_right)
            return Or(op_left, op_right)
        # avoid flase translation
        else:
            if op == "!=":
                return Not(self.__get_infix_for_binary_operator('==', op_left, op_right))
            op_left, op_right = self.__normalize_operands(op, op_left, op_right)
            if op == "==":
                return op_left == op_right
            elif op == ">" or op == "<":
                return op_left > op_right
            elif op == ">=" or op == "<=":
                return op_left >= op_right
            # normalization

            # elif op == "<":
            #     return op_left > op_right
            # elif op == "<=":
            #     return op_left <= op_right
            else:
                print 'can not deal with op: %s, op_left: %s, op_right: %s' %(op, op_left, op_right)

    """
    @ param operand
    @ return operand after normalization
    @ involve remove componnet before ::, ->, .
    """
    def __normalize_operands(self, op, op_left, op_right):
        # normalization
        if isinstance(op_left, unicode) or isinstance(op_left, str):
             op_left = my_util.remove_name_space_and_caller(op_left)
        if isinstance(op_right, unicode) or isinstance(op_right, str):
             op_right = my_util.remove_name_space_and_caller(op_right)
        postfix_dict = {}
        postfix_dict['=='] = '_e_'
        postfix_dict['>'] = '_g_'
        postfix_dict['>='] = '_ge_'
        # swap orperands
        postfix_dict['<'] = '_g_'
        postfix_dict['<='] = '_ge_'
        if op == '==':
            # order for ==
            op_left, op_right = self.__order_operands(op_left, op_right)
        # normalize < to > and <= to >=
        if op == '<' or op == '<=':
            op_left, op_right = op_right, op_left
        if isinstance(op_left, unicode) or isinstance(op_left, str):
            op_left = Int(op_left + postfix_dict[op] + 'l')
        if isinstance(op_right, unicode) or isinstance(op_right, str):
            op_right = Int(op_right + postfix_dict[op] + 'r')
        return op_left, op_right
    """
    @ param operand, p
    @ return p == null
    @ involve p normalized to p == null
    """
    def __normalize_operand(self, operand):
        # p to p == null
        if isinstance(operand, unicode) or isinstance(operand, str):
            operand = my_util.remove_name_space_and_caller(operand)
            normalized_operand = Not(self.__get_infix_for_binary_operator('==', operand, my_constant.JOERN_NULL))
        else:
            normalized_operand = operand
        return normalized_operand

    """
    @ param two operands
    @ return sorted operands
    @ involve sort two operands
    """
    def __order_operands(self, operand_left, operand_right):
        temp_list = [operand_left, operand_right]
        temp_list.sort()
        return temp_list[0], temp_list[1]

   

if __name__ == "__main__":
    z3_api = Z3_api()
    a = z3_api.get_infix_for_postfix(['unknown', 'cm_utf8_decode_character_ret', '&&', 'c', '||'])
    b = z3_api.get_infix_for_postfix(['cm_utf8_decode_character_ret', 'c', '||', 'unknown', 'c', '||', '&&'])
    print z3_api.judge_equality_for_statments(a, b)

    

    
