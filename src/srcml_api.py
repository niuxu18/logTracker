from lxml import etree
import re
import commands
import my_constant
import my_util
import json

class SrcmlApi:
  
    def __init__(self, source_file=None, is_function=True):
        """
        @ param source file, flag about is function file or not\n
        @ return nothing\n
        @ involve create xml file for source file and build namespace info\n
        """
        if source_file is not None and is_function:
            self.set_function_file(source_file)
        elif source_file is not None:
            self.set_source_file(source_file)
        self.log_functions = my_util.retrieve_log_function(my_constant.LOG_CALL_FILE_NAME)
        self.log_functions = my_util.function_to_regrex_name_str(self.log_functions)
        self.log_functions_extend = my_constant.LOG_VAGUE

    def set_source_file(self, source_file):
        """
        @ param source file\n
        @ return nothing\n
        @ involve create xml file(temp.xml) for source file and build namespace info\n
        """
        # intiate xml info
        xml_file = 'test/temp.xml'
        # print '%s begin' %source_file
        commands.getoutput('srcml --position ' + source_file + ' -o ' + xml_file)
        # print '%s end' %source_file
        self.parse_xml(xml_file)
        # initiate functions
        self.functions = []

    def get_functions(self, index, postfix):
        """
        @ param index(counter of functions) and postfix\n
        @ return functions info[function file name]\n
        @ involve get all functions in source file, store both file and xml file\n
        """
        if self.root == None:
            return []
        # get all sub functions
        function_nodes = self.root.iterdescendants(tag=self.function_tag)
        if function_nodes is not None:
            for function_node in function_nodes:
                # store xml function
                function_file_name = my_constant.SAVE_REPOS_FUNCTION + str(index) + postfix + '.cpp'
                function_xml_name = function_file_name + '.xml'
                function = etree.tostring(function_node)
                my_util.save_file(function, function_xml_name)
                # store source function(retry util success run srcml)
                output = 'initialize'
                while output != '':
                    # print '%s begin' %function_xml_name
                    output = commands.getoutput('srcml -S ' + function_xml_name + ' -o ' + function_file_name)
                    # print '%s end' %function_xml_name
                # read_file = open(function_file_name, 'rb')
                # read_content_after = read_file.read()
                # if len(read_content_after) == 0:
                #     print 'no content for file:%s, fault:%s' %(function_file_name, output)
                # read_file.close()
                self.functions.append(function_file_name)
                index += 1
        return self.functions

    def set_function_file(self, function_file):
        """
        @ param function file\n
        @ return nothing\n
        @ involve create xml(append xml) file from function file and build info about namespace\n
        """
        # intiate xml info
        xml_file = function_file + '.xml'
        # print '%s begin' %function_file
        commands.getoutput('srcml --position ' + function_file + ' -o ' + xml_file)
        # print '%s end' %function_file
        self.parse_xml(xml_file)
        # initiate log and control info
        self.log_node = None
        self.log = []
        self.control_node = None
        self.control = []
        self.control_depenedence_loc = []
        # initiate logs and calls/types info
        self.logs = []
        self.calls = set()
        self.types = set()

    def set_log_loc(self, log_location):
        """
        @ param log location(int from 0; better not be -1)\n
        @ return flag about whether find log or not\n
        @ involve find call in given loc and set log node and log info\n
        """
        if self.tree is None:
            return False
        log_location = log_location + 1 # from 1
        # iterates all call
        call_nodes = self.tree.findall('//default:call', namespaces=self.namespace_map)
        for call in call_nodes:
            name = call[0]
            location = self._get_location_for_nested_node(name)
            # filter by location
            if location == log_location:
                # print self._get_text(call)
                self.log_node = call
                # get info for log node(call --name --argumentlist)
                self.log, temp_loc = self._get_info_for_node(self.log_node[1])
                # self.log.sort()
                return True
        return False

    def get_log_loc(self, log_location):
        """
        @ param initial log location(int from 0, location of call node)\n
        @ return set of log location(whole statements)\n
        @ involve add location of each sub-element of log node into location set\n
        """
        self.set_log_loc(log_location)
        log_locs = set()
        sub_nodes = self.log_node.iterdescendants()
        # validate each name descendant
        for sub_node in sub_nodes:
            if sub_node.text is not None:
                log_locs.add(self._get_location(sub_node) - 1)
        return log_locs

    def get_log_info(self):
        """
        @ param [call after: self.set_log_loc()]\n
        @ return self.log\n
        @ involve get log info for log\n
        """
        return self.log

    def get_control_info(self):
        """
        @ param [call after: self.set_control_dependence()]\n
        @ return self.control\n
        @ involve get control info for log, getter\n
        """
        return self.control

    def get_control_depenedence_loc(self):
        """
        @ param [call after: self.set_control_dependence()]\n
        @ return self.control_depenedence_loc\n
        @ involve get control dependence locations for log, getter\n
        """
        return set(self.control_depenedence_loc)

    def set_control_dependence(self):
        """
        @ param self.log node not none\n
        @ return true if find control dependence\n
        @ involve get control node for log node(if/switch)\n
        """
        if self.log_node is None:
            return False
        # iterator parent to find if/switch
        self.control_node = []
        skip_next = False
        parent_iter = self.log_node.iterancestors()
        for parent in parent_iter:
            tag = self._remove_prefix(parent)
            # skip current if
            if tag == 'condition':
                skip_next = True
                continue
            # filter by tag[if or switch]
            if tag == 'if' or tag == 'switch':
                # skip first if for log in condition
                if skip_next:
                    skip_next = False
                    continue
                # filter by if/switch --confition
                self.control_node.append(parent[0])
                # print self.get_text(parent[0])
                # add case for switch
                if tag == 'switch':
                    # filter by switch --condition --block ----case
                    for child in parent[1]:
                        tag = self._remove_prefix(child)
                        # filter by sibling descendants
                        if tag == 'case' and \
                    self._is_case_for_node(child, self.log_node):
                            self.control_node.append(child)
                            # print self.get_text(child)
                            # break
                # get info(function, decl) for control dependence
                self.control = []
                self.control_depenedence_loc = []
                for temp_node in self.control_node:
                    control_info, control_loc = self._get_info_for_node(temp_node)
                    self.control += control_info
                    self.control_depenedence_loc += control_loc
                return True
            # filter by tag catch
            if tag == 'catch':
                self.control = []
                # find decl --type ----name
                type_nodes = parent.iterdescendants(tag=self.type_tag)
                for type_node in type_nodes:
                    control_info = ''
                    children = type_node.getchildren()
                    for child in children:
                        if self._remove_prefix(child) == "name":
                            control_info += self._get_text_for_nested_name(child)
                    if control_info == '':
                        control_info = None
                    self.control.append(control_info)

                self.control_depenedence_loc = [self._get_location_for_nested_node(parent)]
                return True

        return False

    def get_logs_calls_types(self):
        """
        @ param nothing\n
        @ return all logs, calls and types in function\n
        @ involve get all log info[loc, log, check, variable], call info[call name], type info[type name]\n
        """
        if self.tree is None:
            return [], [], []
        # get all call node
        call_nodes = self.tree.findall('//default:call', namespaces=self.namespace_map)
        for call_node in call_nodes:
            # filter by call function name -> call info
            name = self._get_text_for_nested_name(call_node[0])
            # if name in self.log_functions:
            if re.search(self.log_functions, name, re.I):
                # loc(from 1)
                loc = self._get_location_for_nested_node(call_node[0]) - 1
                # log
                log = self._get_text(call_node)
                # check
                self.log_node = call_node
                self.set_control_dependence()
                check = self.get_control_info()
                # ignore log without control statement
                if check == []:
                    # call info
                    self.calls.add(name)
                    continue
                # variable (argumentlist)
                variable, temp_loc = self._get_info_for_node(call_node[1])
                self.logs.append([loc, log, json.dumps(check), json.dumps(variable)])
            # call info
            self.calls.add(name)
        # get all type node(type --... --name)
        type_nodes = self.tree.findall('//default:type', namespaces=self.namespace_map)
        for type_node in type_nodes:
            sub_nodes = type_node.getchildren()
            for sub_node in sub_nodes:
                if self._remove_prefix(sub_node) == 'name':
                    name_node = sub_node
                    break
            name = self._get_text_for_nested_name(name_node)
            self.types.add(name)

        return self.logs, list(self.calls), list(self.types)

    def get_semantics_for_variable(self, content):
        """
        @ param content\n
        @ return semantics for given variable\n
        @ involve find semantics info for given variable node\n
        """
        if self.log is None:
            return content
        # retrieve variable node
        variable = content.replace('name: ', '')
        semantics = None       
    
        # variable related to inner function call (name of call or argument)
        index = 0
        find_variable = False
        useful_call_counter = 0
        log_argument_node = self.log_node[1]
        name_descendants = log_argument_node.iterdescendants(tag=self.name_tag)
        call_descendants = list(log_argument_node.iterdescendants(tag=self.call_tag))
        # filter by descendant of call descendants
        for call_node in call_descendants:
            function_name = self._get_text_for_nested_name(call_node[0])
            if not(re.search(self.log_functions, function_name, re.I) or function_name in self.log_functions_extend):
                useful_call_counter += 1

        # validate each name descendant
        for name_node in name_descendants:
            if name_node.text is None:
                continue
            is_valid = True

            # filter by descendant of call descendants
            for call_node in call_descendants:
                if re.search(self.log_functions, function_name, re.I) or function_name in self.log_functions_extend:
                    is_valid = False # do not count this call
                    continue # search search call

                if self._is_ancestor(call_node, name_node):
                    # children of inner call
                    if variable == name_node.text: # find variable
                        # call --name
                        children = call_node.getchildren()
                        for child in children:
                            if name_node == child:
                                return function_name + my_constant.FlAG_FUNC_RETURN + ": " + variable
                        # call --argument
                        return function_name + my_constant.FlAG_FUNC_ARG + ": " + variable
                    else: # no variable
                        is_valid = False
                        break # break call search 

            # increment index
            if is_valid:
                if variable == name_node.text: # find variable
                    find_variable = True
                    break
                index += 1 # index of variable

        # else, get semantics of name nodes by index
        if find_variable:
            # if len(call_descendants) - useless_call_counter + index >= len(self.log) or len(call_descendants) - useless_call_counter + index < 0:
            #     print "%d call, %d useless call, no. %d variable; log: %s" %(len(call_descendants), useless_call_counter, index, self._get_text(self.log_node))
            semantics = self.log[useful_call_counter + index]
        if semantics:
            return semantics + ": " + variable
        else:
            return content

    def transform_operator(self):
        """
        @ param already have xml tree\n
        @ return nothing\n
        @ involve traverse xml tree and replace operator with suitable function\n
        """
        operator_nodes = self.root.iterdescendants(self.operator_tag)
        for operator_node in operator_nodes:
            # find <<: name, operator
            if self._remove_blank(operator_node) == '<<' and self._remove_prefix(operator_node).find("oper") != -1:
                log_node = operator_node.getprevious() 
                stmt_nodes, variable_nodes = self._get_variable_nodes_for_operator(self._get_text_for_nested_name(log_node), operator_node)
                if stmt_nodes is None or len(variable_nodes) == 0:
                    continue

                log_type = self._get_varaible_type(log_node)
                # create statement that call log function
                call_stmt_node = self._make_call_statement(stmt_nodes[0], log_type, variable_nodes)
                # call statement with suitable tail
                # call_stmt_node.tail = stmt_nodes[-1].tail
                stmt_nodes[-1].addnext(call_stmt_node)
                block_node = stmt_nodes[0].getparent()
                if block_node != None:
                    for stmt_node in stmt_nodes:
                        block_node.remove(stmt_node)
        
        # save new xml file
        transformed_file = etree.tostring(self.root)
        my_util.save_file(transformed_file, "test/temp_output.xml")
        

    def parse_xml(self, xml_file):
        """
        @ param xml file\n
        @ return nothing\n
        @ involve parse given xml file build namespace, tag info\n
        """
        try:
            self.tree = etree.parse(xml_file)
        except:
            print 'can not process file:%s' %(xml_file)
            self.tree = None
            self.root = None
        else:
            self.root = self.tree.getroot()
            self.namespace_map = self.root.nsmap
            self.namespace_map['default'] = self.namespace_map[None]
            self.namespace_map.pop(None)
            self.name_tag = "{" + self.namespace_map['default'] + "}name"
            self.call_tag = "{" + self.namespace_map['default'] + "}call"
            self.function_tag = "{" + self.namespace_map['default'] + "}function"
            self.operator_tag = "{" + self.namespace_map['default'] + "}*"
            self.expr_stmt_tag = "{" + self.namespace_map['default'] + "}expr_stmt"
            self.type_tag = "{" + self.namespace_map['default'] + "}type"
            # self.loc_tag = "{" + self.namespace_map['pos'] + "}line"

    def _get_info_for_node(self, node):
        """
        @ param node(not none)\n
        @ return depended info for given node(function name or variable type)\n
        @ involve get and analyze dependent info for given node(call info + name dependence)\n
        """
        # filter out the one with log statement changes
        name_nodes, node_info, loc_info = self._get_pure_name_nodes(node)
        for name_node in name_nodes:
            name_line = int(self._get_location(name_node))
            depended_nodes = self._get_depended_nodes(name_node)
            type_info = None
            arg_info = None
            return_info = None
            type_loc = None
            arg_loc = None
            return_loc = None
            # iterate from name node
            depended_lines = depended_nodes.keys()
            depended_lines.sort(key=lambda d:abs(int(d)-name_line))
            for depended_line in depended_lines:
                depended_info = depended_nodes[depended_line]
                depended_node = depended_info[0]
                depended_type = depended_info[1]                
                # get children whose tag is name [call --name or type (--specifier) --name]
                if depended_node is None:
                    continue
                depended_sub_nodes = depended_node.getchildren()
                for depended_sub_node in depended_sub_nodes:
                    if self._remove_prefix(depended_sub_node) == 'name':
                        depended_node = depended_sub_node
                        break
                info = self._get_text_for_nested_name(depended_node)
                # record nearest arg and decl
                if depended_type == my_constant.VAR_TYPE and type_info is None:
                    type_info = info + my_constant.FlAG_TYPE
                    type_loc = depended_line
                # record nearest arg and decl
                if re.search(self.log_functions, info, re.I) or info.lower() in self.log_functions_extend:
                    continue
                # level 1
                if depended_type == my_constant.VAR_FUNC_RETURN:
                    return_info = info + my_constant.FlAG_FUNC_RETURN
                    return_loc = depended_line
                    break
                if depended_type == my_constant.VAR_FUNC_ARG_RETURN:
                    return_info = info + my_constant.FlAG_FUNC_ARG_RETURN
                    return_loc = depended_line
                    break
                if depended_type == my_constant.VAR_FUNC_ARG and arg_info is None:
                    arg_info = info + my_constant.FlAG_FUNC_ARG
                    arg_loc = depended_line
            # return > arg > var type
            if return_info is not None:
                info = return_info
                loc = return_loc
            elif arg_info is not None:
                info = arg_info
                loc = arg_loc
            else:
                info = type_info
                loc = type_loc
            node_info.append(info)
            if info is not None:
                loc_info.append(loc - 1)

        return node_info, loc_info

    def _get_varaible_type(self, node):
        """
        @ param node(name, not none, has text)\n
        @ return variable type name or variable name\n
        @ involve try to find definition of given node, if failed return node text\n
        """
        node_line = self._get_location(node)
        node_text = self._get_text_for_nested_name(node)
        # find all name node
        candi_nodes = self.tree.findall("//default:name", namespaces=self.namespace_map)
        type_info = None
        for candi_node in candi_nodes:
            # if candi_node == node or candi_node.text != node.text or candi_node.text is None:
            if self._get_text_for_nested_name(candi_node) != node_text:
                continue
            candi_line = self._get_location(candi_node)
            # find use as return or reference argument for functions
            if candi_line <= node_line:
                # filter by decl --type ----name --name
                decl_node = candi_node.getparent()
                if decl_node is not None and self._remove_prefix(decl_node) == 'decl':
                    # mark is pointer or not
                    type_node = self._get_real_type_node(candi_node.getprevious())
                    type_info = self._get_text_for_nested_name(type_node)

        if type_info is None:
            type_info = node_text

        return type_info

    def _get_depended_nodes(self, node):
        """
        @ param node(name, not none, has text)\n
        @ return data depended node {line, [node, depended_type]}\n
        @ involve get data depended nodes for given node(call, decl)\n
        """
        depended_nodes = {}
        node_line = self._get_location(node)
        # find all name node
        candi_nodes = self.tree.findall("//default:name", namespaces=self.namespace_map)
        is_ptr = False # mark for pointer argument
        for candi_node in candi_nodes:
            # if candi_node == node or candi_node.text != node.text or candi_node.text is None:
            if candi_node.text != node.text or candi_node.text is None:
                continue
            candi_line = self._get_location(candi_node)
            # find use as return or reference argument for functions
            if candi_line <= node_line:
                # filter by name = (***) call
                operator_node = candi_node.getnext()
                if operator_node is not None and self._remove_prefix(operator_node) == 'operator'\
                                        and self._remove_blank(operator_node) == '=':
                    expr_node = operator_node.getparent()
                    func_node = self._get_sub_call_node(expr_node)
                    if func_node is not None:
                        self._update_dict(depended_nodes, candi_line, my_constant.VAR_FUNC_RETURN, func_node)
                        continue
                # filter by call ----argument ------expr --------& --------name
                argument_node = candi_node.getparent().getparent()
                if argument_node is not None and self._remove_prefix(argument_node) == 'argument':
                    func_node = argument_node.getparent().getparent()
                    modifier_node = candi_node.getprevious()
                    if modifier_node is not None and self._remove_prefix(modifier_node) == 'operator'\
                                             and self._remove_blank(modifier_node) == '&':
                        self._update_dict(depended_nodes, candi_line, my_constant.VAR_FUNC_ARG_RETURN, func_node)
                    # filter by call ----argument --------name(ptr)
                    elif is_ptr:
                        self._update_dict(depended_nodes, candi_line, my_constant.VAR_FUNC_ARG_RETURN, func_node)
                    continue
                # filter by decl --type --name --init ----expr --call
                init_node = candi_node.getnext()
                if init_node is not None and self._remove_prefix(init_node) == 'init':
                    # mark is pointer or not
                    type_node = self._get_real_type_node(candi_node.getprevious())
                    is_ptr = self._is_pointer(type_node)
                    func_node = self._get_sub_call_node(init_node)
                    if func_node is not None:
                        self._update_dict(depended_nodes, candi_line, my_constant.VAR_FUNC_RETURN, func_node)
                        continue
                    self._update_dict(depended_nodes, candi_line, my_constant.VAR_TYPE, type_node)
                    continue
                # filter by decl --type ----name ----modifier --name
                decl_node = candi_node.getparent()
                if decl_node is not None and self._remove_prefix(decl_node) == 'decl':
                    # mark is pointer or not
                    type_node = self._get_real_type_node(candi_node.getprevious())
                    is_ptr = self._is_pointer(type_node)
                    self._update_dict(depended_nodes, candi_line, my_constant.VAR_TYPE, type_node)
                    continue
            # find use as argument for functions
            else:
                # filter by call ----argument --------name
                argument_node = candi_node.getparent().getparent()
                if argument_node is not None and self._remove_prefix(argument_node) == 'argument':
                    func_node = argument_node.getparent().getparent()
                    self._update_dict(depended_nodes, candi_line, my_constant.VAR_FUNC_ARG, func_node)
                    continue

        return depended_nodes

    def _get_pure_name_nodes(self, node):
        """
        @ param node(not none)\n
        @ return pure name node (no median call, has text), call info and loc info\n
        @ involve get name nodes without expanding call, call info add\n
        """
        name_nodes = []
        name_descendants = node.iterdescendants(tag=self.name_tag)
        # validate each name descendant
        for name_node in name_descendants:
            is_valid = True
            # filter by descendant of call descendants
            for call_node in node.iterdescendants(tag=self.call_tag):
                if self._is_ancestor(call_node, name_node):
                    is_valid = False
                    break
            # append valid name node
            if is_valid and name_node.text is not None:
                name_nodes.append(name_node)

        # add call info for call descendants
        call_info = []
        loc_info = [self._get_location_for_nested_node(node) - 1] # if/switch or case location
        for call_node in node.iterdescendants(tag=self.call_tag):
            # call --name --argument list ----argument
            info = self._get_text_for_nested_name(call_node[0])
            if not re.search(self.log_functions, info, re.I) and info not in self.log_functions_extend:
                call_info.append(info + my_constant.FlAG_FUNC_RETURN)
                # add location for call, index from 0
                loc_info.append(self._get_location_for_nested_node(call_node[0]) - 1)
        return name_nodes, call_info, loc_info

    def _is_case_for_node(self, case_node, node):
        """
        @ param case node (not none) and node\n
        @ return true if is\n
        @ involve judge whether node is under case(no break between case node and node)\n
        """
        next_node = case_node.getnext()
        while next_node is not None and self._remove_prefix(next_node) != "break":
            # node is subnode of node controled by case
            if self._is_ancestor(next_node, node):
                return True
            next_node = next_node.getnext()
        return False

    def _is_ancestor(self, ancestor, node):
        """
        @ param ancestor node(not none) and node\n
        @ return true if is\n
        @ involve judge whether ancestor relation true(without check)\n
        """
        # get descendants by tag
        descendant_iter = ancestor.iterdescendants(tag=node.tag)
        for descendant in descendant_iter:
            # filter by equality
            if descendant == node:
                return True
        return False


    def _get_real_type_node(self, node):
        """
        @ param node(type)(provided check)\n
        @ return real type node\n
        @ involve deal with type reference previous node\n
        """
        while node is not None and self._remove_prefix(node) == 'type':
            if len(node) > 0:
                return node
            else:
                decl_node = node.getparent()
                # traverse previous declare node
                prev_node = decl_node.getprevious()
                while self._remove_prefix(prev_node) != 'decl':
                    prev_node = prev_node.getprevious()
                node = prev_node[0]
        
        # did not find node(xml analysis fault)
        return None

    def _get_sub_call_node(self, node):
        """
        @ param node(not none)(without check)\n
        @ return call node of sub expression\n
        @ involve find sub call node for parent node if possible\n
        """
        func_nodes = node.iterdescendants(tag='{'+self.namespace_map['default']+'}call')
        if func_nodes is not None:
            for func_node in func_nodes:
                return func_node
        return None

    def _is_pointer(self, node):
        """
        @ param node(type)(provided check)\n
        @ return true if is\n
        @ involve judge whether type has a modifier and that modifier is *\n
        """
        if node is not None and self._remove_prefix(node) == 'type':
            # type must has at least two children
            children_nodes = node.getchildren()
            for child in children_nodes:
                # filter by type --specifier(maybe) --name --modifier
                if self._remove_prefix(child) == 'modifier' and self._remove_blank(child) == '*':
                    return True
        return False


    def _get_text(self, node=None):
        """
        @ param node(provided check)\n
        @ return content of this node concate content of sub-nodes\n
        @ involve get text for this node(children whose text is not none)\n
        """
        content = ""
        if node is None or node.prefix == 'pos':
            return content
        # if has text, add to content
        if node.text:
            content += node.text
        # add text of children
        for child in node:
            content += self._get_text(child)
        # if has tail, add tail at last
        if node.tail:
            content += node.tail

        return content

    def _remove_prefix(self, node):
        """
        @ param node(not none)\n
        @ return tag without prefix\n
        @ involve remove prefix for tag without check\n
        """
        # if prefix is None:
        #     prefix = 'default'
        # return node.tag.replace(self.namespace_map[prefix], '')
        return node.tag[node.tag.find('}') + 1:]

    def _remove_blank(self, node):
        """
        @ param node(not none)\n
        @ return text without blank\n
        @ involve remove blank directly without check\n
        """
        if node.text is None:
            # print 'no need to remove for none text'
            return None
        return node.text.replace(' ', '')


    def _get_text_for_nested_name(self, node):
        """
        @ param node(name)\n
        @ return nested text without blank\n
        @ involve deal with nested text which name is formed of two or more names\n
        """
        if node.text is not None:
            text = self._remove_blank(node)
            return text
        # traverse children of name without text
        else:
            text = ''
            name_nodes = node.iterdescendants()
            for name_node in name_nodes:
                # add current name node text
                if name_node.text is not None:
                    text = text + self._remove_blank(name_node)
                else:
                    text = text + self._get_text_for_nested_name(name_node)
            return text

    def _get_location_for_nested_node(self, node):
        """
        @ param node(not none)\n
        @ return loacation(int)\n
        @ involve get location from nested node\n
        """
        if node.text is not None:
            return self._get_location(node)
        # nested node for location info
        sub_nodes = node.iterdescendants()
        for sub_node in sub_nodes:
            if sub_node.text is not None:
                return self._get_location(sub_node)

    def _get_location(self, node):
        """
        @ param node(text can not be none)\n
        @ return loacation(int)\n
        @ involve get location directly without check\n
        """
        if len(node.attrib.values()) >= 2:
            return int(node.attrib.values()[-2])
        else:
            return int(node.sourceline) - 1
    
    def _get_variable_nodes_for_operator(self, variable_name, operator_node):
        """
        @ param variable name and operator node\n
        @ return list of statement node and list of variable node\n
        @ involve find varaible node from the same statements (<< a << b) and following statement(cout << a; cout << b;)\n
        """
        # stmt node
        stmt_node = operator_node.getparent()
        while stmt_node != None and self._remove_prefix(stmt_node) != "expr_stmt":
            stmt_node = stmt_node.getparent()
        if stmt_node is None:
            return None, None
        stmt_nodes = [stmt_node]
        variable_nodes = []

        variable_nodes += self._get_variable_nodes_for_one_statement(operator_node)
        
        # following statement cout << a << b; cout << c << d;
        next_stmt_node = stmt_node.getnext()
        is_continue = True
        while next_stmt_node != None and self._remove_prefix(next_stmt_node) == "expr_stmt" and is_continue:
            is_continue = False
            # first operator node that is <<
            sub_operator_nodes = next_stmt_node.iterdescendants(self.operator_tag)
            for sub_operator_node in sub_operator_nodes:
                if self._remove_blank(sub_operator_node) == "<<" and \
                    self._get_text_for_nested_name(sub_operator_node.getprevious()) == variable_name:

                    variable_nodes += self._get_variable_nodes_for_one_statement(sub_operator_node)
                    stmt_nodes.append(next_stmt_node)
                    is_continue = True
                    break

            next_stmt_node = next_stmt_node.getnext()

        return stmt_nodes, variable_nodes

    def _get_variable_nodes_for_one_statement(self, operator_node):
        """
        @ param operator node\n
        @ return list of variable node\n
        @ involve find varaible node from the same statements (<< a << b)\n
        """  
        variable_nodes = []
        # same statement << a << b
        sibling_nodes = operator_node.itersiblings()
        for sibling_node in sibling_nodes:
            if self._remove_prefix(sibling_node) == "operator" and self._remove_blank(sibling_node) == "<<":
                continue # skip <<
            else:
                variable_nodes.append(sibling_node)
                
        return variable_nodes

    def _make_call_statement(self, demo_node, function_name, variable_nodes):
        """
        @ param demo_node, function name and list of variable nodes\n
        @ return statement node\n
        @ involve make lxml element that call given function with given variables\n
        """
        call_node = demo_node.makeelement("call")
        call_name_node = demo_node.makeelement("name")
        call_name_node.text = function_name
        call_node.append(call_name_node)

        arguments_node = demo_node.makeelement("argument_list")
        arguments_node.text = "("
        arguments_node.tail = ";"
        for variable_node in variable_nodes[:-1]:
            argument_node = demo_node.makeelement("argument")
            argument_node.append(variable_node)
            argument_node.tail = ','
            arguments_node.append(argument_node)
        # last variable node tail with )
        argument_node = demo_node.makeelement("argument")
        argument_node.append(variable_nodes[-1])
        argument_node.tail = ')'
        arguments_node.append(argument_node)

        call_node.append(arguments_node)

        stmt_node = demo_node.makeelement("expr_stmt")
        expr_node = demo_node.makeelement("expr")
        expr_node.append(call_node)
        stmt_node.append(expr_node)

        return stmt_node

    def _update_dict(self, dictionary, key, rank, value):
        """
        @ param dictionary, key, rank and value\n
        @ return updated dictionary\n
        @ involve check whether has key, if has, replace with new value if has rank lower\n
        """
        if dictionary.has_key(key):
            old_rank = dictionary[key][1]
            # old value is not none and current rank is lower
            if dictionary[key][0] is not None and rank > old_rank:
                return dictionary
        # ranker is higher or no key or old value is none
        dictionary[key] = [value, rank]

        return dictionary

if __name__ == "__main__":
    # input function cpp file
    # srcml_api = SrcmlApi('second/download/git/repos/git-2.6.7/commit.c', is_function=False)
    # print srcml_api.get_functions(0, "_test")

    # srcml_api = SrcmlApi('second/sample/wget/generate/gumtree/wget_old_function_1105.cpp', is_function=True)
    # if srcml_api.set_log_loc(26):
    #      print srcml_api.get_log_info()
    #      print srcml_api.get_semantics_for_variable("result")

    #print re.search(r'@@([^@]*)@@', 'add	$$name: quote$$	in	@@argument_list: (stderr, _("%s: %s: Invalid value `%s\'.\n"), exec_name, com, val);@@').groups()
    
    # print srcml_api.get_logs_calls_types()
    # srcml_api = SrcmlApi('/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/httpd/gumtree/httpd_repos_function_2380_httpd-2.2.34.cpp', True)

    # if srcml_api.set_log_loc(6):
    #     print srcml_api.get_log_info()
    #     print srcml_api.get_semantics_for_variable("literal: 60")

    srcml = SrcmlApi()
    filename = "second/sample/ice/versions/Ice-2.1.0/demo/Freeze/library/Parser.cpp"
    # commands.getoutput("srcml " + filename + " -o test/temp_input.xml")
    # srcml.parse_xml("test/temp_input.xml")
    # srcml.transform_operator()
    # # transform source code from temp output file
    # commands.getoutput("srcml " + "test/temp_output.xml -S > test/output.cpp")
    srcml.set_source_file(filename)
    if srcml.set_log_loc(74):
        print srcml.get_log_info()
        srcml.set_control_dependence()
        print srcml.get_control_info()