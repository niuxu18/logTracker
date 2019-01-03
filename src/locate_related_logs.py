import re
from lxml import etree
import commands

class LogLocator:
    
    FUNC_RETURN = 0
    FUNC_ARG = 1
    RELATION_TYPES = ['return value', 'argument']
    function_file_index = 0
    def __init__(self):
        pass

    def set_log_functions(self, log_functions, spliter=';'):
        """
        retrieve log functions

        input: string of log functions and spliter
        output: list of function names
        """
        log_functions = log_functions.split(spliter)
        
        # create regex from function names (inaccurate compare **func_name**)
        self.log_functions = r'^\w*('
        for func in log_functions:
            self.log_functions += func + r'|'
        self.log_functions = self.log_functions[:-1]
        self.log_functions += r')\w*$'

    def set_interested_functions(self, interested_functions, spliter=';'):
        """
        set interested functions

        input: string of interested functions and spliter
        output: list of function names
        """
        self.interested_functions = interested_functions.split(spliter)

    def locate_related_logs(self, source_file, patch_file, is_old=True):
        """
        locate logs which is related to the changes in patch file

        input: source file, patch file, interested functions and flag about is old file or not
        output: related logs
        """

        # get locs of changes
        locs = self._get_locs_from_patch(patch_file, is_old)

        function_file_names = []
        # get function bodies
        for loc in locs:
            function_file_name = 'test/temp_' + str(LogLocator.function_file_index) + '.cpp'
            # loc -> function
            if self._get_function_from_loc(source_file, loc, function_file_name):
                function_file_names.append(function_file_name)
                LogLocator.function_file_index += 1

        related_logs = []
        # get related logs in functions
        for function_file_name in function_file_names:
            related_logs += self._get_related_logs(function_file_name)
            # function -> log (logs, filter by control dependency)

        print related_logs
        return related_logs

    def _get_locs_from_patch(self, patch_file, is_old):
        """
        process hunk of patch file

        input: patch file and flag about is old file or not
        output: locations of changes (may be old or new)
        """
        locs = []
        change_mark = '-' if is_old else '+'
        loc = 0

        patch = open(patch_file, 'rb')
        lines = patch.readlines()
        for line in lines:
            # skip --- && +++
            if line.startswith('---') or line.startswith('+++'):
                continue
            
            # new hunk
            is_hunk = re.match(r'^@@.*-(.*),.*\+(.*),.*@@$', line)
            if is_hunk:
                # initialize loc
                loc = int(is_hunk.group(1)) - 1 if is_old else int(is_hunk.group(2)) - 1
                continue

            # record change type flag
            change_type = line[0]
            if change_type in [' ', change_mark]:
                loc += 1
                # interested changes
                if change_type == change_mark:
                    # print line, loc
                    locs.append(loc)

        patch.close()

        return locs

    def _get_function_from_loc(self, source_file, location, function_file):
        """
        get function body of given loc

        input: source file and locations, function file to store
        output: flag about whether successfully find the body
        store function body as file
        """
        # get ast structure of source file
        xml_file_name = 'test/temp.xml'
        commands.getoutput('srcml --position ' + source_file + ' -o ' + xml_file_name + ' > null')
        self.__parse_xml(xml_file_name)

        # get node of given location
        func_nodes = self.root.iterdescendants(tag = self.function_tag)

        pre_func = None
        for func in func_nodes:
            loc = self.__get_location_for_nested_node(func)
            # following function
            if loc > location:
                break
            pre_func = func

        # store function to file
        if pre_func is None:
            print "can not find function body for line %d in source file %s" %(location, source_file)
            return False

        function = etree.tostring(pre_func)
        with open(function_file + '.xml', 'wb') as writer:
            writer.write(function)
    
        # retry util success run srcml
        output = 'success'
        while output != '':
             output = commands.getoutput('srcml -S ' + function_file + '.xml' + ' -o ' + function_file + ' > null')
            
        return True

    def _get_related_logs(self, function_file):
        """
        get related log statement in given file

        input: file name (file of function body)
        output: related logs (text of statement)
        first collect all logs (by log functions), then filter them by control depenence
        """
        # get logs of function
        xml_file_name = function_file + '.xml'
        commands.getoutput('srcml --position ' + function_file + ' -o ' + xml_file_name + ' > null')
        self.__parse_xml(xml_file_name)

        logs = []
        call_nodes = self.root.iterdescendants(tag=self.call_tag)
        for call_node in call_nodes:
            # get name of call node
            sub_nodes = call_node.getchildren()
            for sub_node in sub_nodes:
                if self.__remove_prefix(sub_node) == 'name':
                    name_node = sub_node
            call_name = self.__get_text_for_nested_name(name_node)

            if re.search(self.log_functions, call_name, re.I):
                # filter log node by branch
                if self.__has_interested_control_dependence(call_node):
                    logs.append(self.__get_text(call_node))

        return logs

    def __has_interested_control_dependence(self, log_node):
        """
        whether is interested branch

        input: log node
        output: true if interested
        """

        # iterator parent to find if/switch
        skip_next = False
        parent_iter = log_node.iterancestors()
        for parent in parent_iter:
            tag = self.__remove_prefix(parent)
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
                # is interest
                if self.__is_interested_branch(parent):
                    return True

                # add case for switch
                if tag == 'switch':
                    # filter by switch --condition --block ----case
                    for child in parent[1]:
                        tag = self.__remove_prefix(child)
                        # filter by sibling descendants
                        if tag == 'case' and self.__is_case_for_node(child, log_node):
                            if self.__is_interested_branch(child):
                                return True

        return False

    def __is_interested_branch(self, branch_node):
        """
        whether a branch is related to interested functions

        input: branch node
        output: true if relate
        """
        # check call in branch is interested one or not
        call_nodes = branch_node.iterdescendants(tag=self.call_tag)
        for call_node in call_nodes:
            if self.__is_interest_call_node(call_node):
                print 'The node %s is related to interest function by return value' %(self.__get_text(call_node))
                return True

        # check dependencies
        name_nodes = branch_node.iterdescendants(tag=self.name_tag)
        for name_node in name_nodes:
            if self.__is_interested_name_node(name_node):
                return True
            else:
                return False

    def __is_interested_name_node(self, name_node):
        """
        only focus on interested functions

        input name node
        output flag about related to function or not
        """
        name_line = int(self.__get_location(name_node))
        depended_nodes = self.__get_depended_nodes(name_node)
        
        # iterate from name node
        depended_lines = depended_nodes.keys()
        depended_lines.sort(key=lambda d:abs(int(d)-name_line))
        for depended_line in depended_lines:
            depended_info = depended_nodes[depended_line]
            depended_node = depended_info[0]
            depended_type = LogLocator.RELATION_TYPES[depended_info[1]]
            if depended_node is None:
                continue
    
            if self.__is_interest_call_node(depended_node):
                print 'The node ' + self.__get_text_for_nested_name(name_node) + \
                            ' is related to interest function by ' + depended_type
                return True

        return False

    def __is_interest_call_node(self, call_node):
        """
        whether this call not is about the interested function

        input: call node
        output: true if is interested
        first get its name node call --name and then get its name, finally compare with targets
        """
        sub_nodes = call_node.getchildren()
        for sub_node in sub_nodes:
            if self.__remove_prefix(sub_node) == 'name':
                call_node = sub_node
                break
    
        call_name = self.__get_text_for_nested_name(call_node)
        for func in self.interested_functions:
            if call_name.find(func) != -1:
                return True
        
        return False

    def __get_depended_nodes(self, node):
        """
        get data depended nodes for given node

        output: dict of related functions, key is line, and value is list of (depended node and dependency type)
        """
        depended_nodes = {}
        node_line = self.__get_location(node)

        # find all name node
        candi_nodes = self.tree.findall("//default:name", namespaces=self.namespace_map)
        is_ptr = False # mark for pointer argument
        for candi_node in candi_nodes:
            # if candi_node == node or candi_node.text != node.text or candi_node.text is None:
            if candi_node.text != node.text or candi_node.text is None:
                continue
            
            candi_line = self.__get_location(candi_node)
            # filter by name = (***) call
            operator_node = candi_node.getnext()
            if operator_node is not None and self.__remove_blank(operator_node) == '=':
                expr_node = operator_node.getparent()
                call_node = self.__get_sub_call_node(expr_node)
                if call_node is not None:
                    self.__update_dict(depended_nodes, candi_line, LogLocator.FUNC_RETURN, call_node)
                    continue
            # filter by call ----argument ------expr (--------&) --------name
            argument_node = candi_node.getparent().getparent()
            if argument_node is not None and self.__remove_prefix(argument_node) == 'argument':
                call_node = argument_node.getparent().getparent()
                modifier_node = candi_node.getprevious()
                if modifier_node is not None and self.__remove_prefix(modifier_node) == 'operator'\
                                            and self.__remove_blank(modifier_node) == '&':
                    self.__update_dict(depended_nodes, candi_line, LogLocator.FUNC_ARG, call_node)
                else:
                    self.__update_dict(depended_nodes, candi_line, LogLocator.FUNC_ARG, call_node)
    
        return depended_nodes
    
    def __update_dict(self, dictionary, key, rank, value):
        """
        update dict of key, if key exist, then update only when rank is smaller (topper)

        input: dict, key, value and rank
        """
        if dictionary.has_key(key):
            old_rank = dictionary[key][1]
            if dictionary[key][0] is not None and rank > old_rank:
                return dictionary

        dictionary[key] = [value, rank]
        return dictionary
    
    def __get_sub_call_node(self, node):
        """
        return call sub-node of expr node
        """
        func_nodes = node.iterdescendants(tag=self.call_tag)
        if func_nodes is not None:
            for func_node in func_nodes:
                return func_node
        return None
  
    def __parse_xml(self, xml_file):
        """
        parse xml files, set root and tree

        input: xml file name
        output: nothing
        set tr
        """
        try:
            self.tree = etree.parse(xml_file)
        except:
            print 'can not process file: %s' %(xml_file)
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

    def __is_case_for_node(self, case_node, node):   
        """
        whether this node is under given case or default

        """
        next_node = case_node.getnext()
        while next_node is not None and self.__remove_prefix(next_node) != "break":
            # node is subnode of node controled by case
            if self.__is_ancestor(next_node, node):
                return True
            next_node = next_node.getnext()
        return False
    
    def __is_ancestor(self, ancestor, node):
        """
        whether is anscestor or not

        """
        # get descendants by tag
        descendant_iter = ancestor.iterdescendants(tag=node.tag)
        for descendant in descendant_iter:
            # filter by equality
            if descendant == node:
                return True
        return False

    def __remove_prefix(self, node):
        """
        @ param node(not none)\n
        @ return tag without prefix\n
        @ involve remove prefix for tag without check\n
        """
        return node.tag[node.tag.find('}') + 1:]
    
    def __remove_blank(self, node):
        """
        @ param node(not none)\n
        @ return text without blank\n
        @ involve remove blank directly without check\n
        """
        if node.text is None:
            # print 'no need to remove for none text'
            return None
        return node.text.replace(' ', '')
    
    def __get_location_for_nested_node(self, node):
        """
        @ param node(not none)\n
        @ return loacation(int)\n
        @ involve get location from nested node\n
        """
        if node.text is not None:
            return self.__get_location(node)
        # nested node for location info
        sub_nodes = node.iterdescendants()
        for sub_node in sub_nodes:
            if sub_node.text is not None:
                return self.__get_location(sub_node)

    def __get_location(self, node):
        """
        @ param node(text can not be none)\n
        @ return loacation(int)\n
        @ involve get location directly without check\n
        """
        return int(node.attrib.values()[-2])

    def __get_text(self, node=None):
        """
        get text from xml structure

        like print
        """
        content = ""
        if node is None or node.prefix == 'pos':
            return content
        # if has text, add to content
        if node.text:
            content += node.text

        # add text of children
        for child in node:
            content += self.__get_text(child)

        # if has tail, add tail at last
        if node.tail:
            content += node.tail

        return content
    
    def __get_text_for_nested_name(self, node):
        """
        get nested text for name with multi sub-names
        """
        if node.text is not None:
            text = self.__remove_blank(node)
        # traverse children of name without text
        else:
            text = ''
        name_nodes = node.iterdescendants()
        for name_node in name_nodes:
            # add current name node text
            if name_node.text is not None:
                text = text + self.__remove_blank(name_node)
            else:
                text = text + self.__get_text_for_nested_name(name_node)
        return text

if __name__ == '__main__':
    helper = LogLocator()
    helper.set_log_functions('print')
    helper.set_interested_functions('fun')
    helper.locate_related_logs('test/old.cpp', 'test/diff.cpp', True)