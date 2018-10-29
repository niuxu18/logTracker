from lxml import etree
import re
import commands
from itertools import islice
import my_constant
import my_util
import json
import csv

class DatabaseApi:

    def __init__(self):
        pass

    def store_old_new_file_to_database(self):
        """
        @ param nothing\n
        @ return nothing\n
        @ involve transform each record to corresponding dot file and then store into graph db\n
        """ 
        old_new_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'rb')
        old_new_records = csv.reader(old_new_file)
        for old_new_record in islice(old_new_records, 1, 2):
            self.deal_old_new_record(old_new_record)
        
        old_new_file.close()

    def deal_old_new_record(self, record):
        """
        @ param record from old new llvm file\n
        @ return nothing\n
        @ involve modify function xml file (append context attributes) and transform it into dot file\n
        """ 
        function = ''
        function_loc = -1
        if record[my_constant.FETCH_LOG_OLD_LOC] != '-1': # has old -> old
            function = record[my_constant.ANALYZE_OLD_FUNCTION]
            function_loc = int(record[my_constant.ANALYZE_OLD_FUNCTION_LOC])
        else:
            function = record[my_constant.ANALYZE_NEW_FUNCTION]
            function_loc = int(record[my_constant.ANALYZE_NEW_FUNCTION_LOC])
        function_xml_file_name = function + '.xml'
        log_loc = function_loc
        self.parse_xml(function_xml_file_name)
        if self.set_log_loc(log_loc):
            # modify xml
            new_labels = []
            old_loc = record[my_constant.FETCH_LOG_OLD_LOC]
            file_name = ''
            file_loc = -1
            if old_loc != '-1': # old file
                file_name = record[my_constant.FETCH_LOG_OLD_FILE]
                file_loc = old_loc
            else:
                file_name = record[my_constant.FETCH_LOG_NEW_FILE]
                file_loc = int(record[my_constant.FETCH_LOG_NEW_LOC])
            new_labels.append(['file_name', file_name])
            new_labels.append(['file_loc', str(file_loc)])
            old_log = record[my_constant.FETCH_LOG_OLD_LOG]
            new_labels.append(['old_log', old_log])
            new_log = record[my_constant.FETCH_LOG_NEW_LOG]
            new_labels.append(['new_log', new_log])
            semantical_edits = record[my_constant.ANALYZE_SEMANTICAL_EDIT]
            new_labels.append(['semantical_edits', semantical_edits])
            edit_feature = record[my_constant.ANALYZE_EDIT_FEATURE]
            new_labels.append(['edit_feature', edit_feature])
            check = record[my_constant.ANALYZE_CHECK]
            new_labels.append(['check', check])
            variable = record[my_constant.ANALYZE_VARIABLE]
            new_labels.append(['variable', variable])
            self.add_labels(new_labels)

            self.xml_to_dot(self.tree.getroot(), function_xml_file_name + '.dot')
            print "transform %s file" %(function_xml_file_name)
        else:
            print "can not find log in %d of %s file" %(log_loc, function_xml_file_name)


    def xml_to_dot(self, root_node, dot_file_name):
        """
        @ param node which contain the xml structure, dot file name the output file\n
        @ return nothing\n
        @ involve transform xml structure to dot file\n
        """
        dot_content = 'digraph g {\n'
        count = 0
        left_nodes = [root_node]
        count_of_left_ndes = [count]
        dot_content += self._xml_node_to_dot_node(root_node, count) # root can not be none

        while len(left_nodes) != 0:
            # fetch the tail node
            curr_node = left_nodes.pop()
            parent_count = count_of_left_ndes.pop()

            children = curr_node.getchildren()
            for child_node in children:
                count += 1
                # add child node
                curr_content = self._xml_node_to_dot_node(child_node, count)
                if curr_content is None:
                    continue
                dot_content += curr_content
                # add edge between children
                dot_content += str(parent_count) + ' -> ' + str(count) + ';\n'
                # add child node to list head
                left_nodes.insert(0, child_node)
                count_of_left_ndes.insert(0, count)

        dot_content += '}\n'

        my_util.save_file(dot_content, dot_file_name)

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

    def set_log_loc(self, log_location):
        """
        @ param log location(int from 0; better not be -1)\n
        @ return flag about whether find log or not\n
        @ involve find call in given loc and set log node\n
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
                self.log_node = call
                # etree.dump(self.log_node)
                # print self._get_text(self.log_node)
                return True
        return False

    def add_labels(self, new_labels):
        """
        @ param list of labels, label is pair of key value(check: [null, null])\n
        @ return nothing\n
        @ involve add these new labels to log node as new attributes\n
        """
        if self.log_node is None:
            return False

        for label in new_labels:
            self.log_node.set(label[0], label[1]) # label[1] json dumps for list objects

        # etree.dump(self.log_node) 

    def _xml_node_to_dot_node(self, node, id):
        """
        @ param node and its unique id\n
        @ return string of dot node or none(skip this node)\n
        @ involve transform node to dot node with name as the unique id and attributes as those of the input xml node\n
        """
        attributes = ' ['
        # tag as label
        tag = self._remove_prefix(node)
        if tag == "position":
            return None
        attributes += 'label=' + json.dumps(tag)

        if node == self.log_node:
            attributes += ', '
            for label in node.items():
                attributes += label[0] + '=' + json.dumps(label[1]) + ', '### label[1] may be json dump output or simple string
            return str(id) + attributes[:-2] + '];\n'
        else:
            # text if has
            if node.text != None:
                attributes += ', text=' + json.dumps(node.text)
            return str(id) + attributes + '];\n'


    def _remove_prefix(self, node):
        """
        @ param node(not none)\n
        @ return tag without prefix\n
        @ involve remove prefix for tag without check\n
        """
        return node.tag[node.tag.find('}') + 1:]

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
        return int(node.attrib.values()[-2])

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

if __name__ == "__main__":
    db_api = DatabaseApi()
    db_api.store_old_new_file_to_database()
