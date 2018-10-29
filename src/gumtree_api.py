#-*-coding: utf-8 -*-
from jpype import *
import my_constant
import my_util
import re

class Gumtree:  
    gumtree = None

    def __init__(self, class_name='gumtree.GumTreeApi'):
        """
        @ param java class name\n
        @ return nothing\n
        @ involve open jvm and create object for given java class\n
        """
        if Gumtree.gumtree is None:
            # class path
            jvm_arg = "-Djava.class.path=" + my_constant.JAVA_CLASS_PATH
            startJVM(getDefaultJVMPath(), '-d64', jvm_arg)
            # initial class and object
            GumtreeApi = JClass(class_name)
            Gumtree.gumtree = GumtreeApi()

    def set_old_new_file(self, old_file, new_file):
        """
        @ param old and new file\n
        @ return nothing\n
        @ involve set old and new file for gumtree object\n
        """
        Gumtree.gumtree.setOldAndNewFile(old_file, new_file)


    def set_old_loc(self, line):
        """
        @ param line(int)\n
        @ return true if find old log\n
        @ involve mark old log for node in given line\n
        """
        return Gumtree.gumtree.setOldLoc(line)

    def get_new_loc(self):
        """
        @ param nothing\n
        @ return line(int)\n
        @ involve get mapping line of old log\n
        """
        return Gumtree.gumtree.getNewLoc()


    def get_new_log(self):
        """
        @ param nothing\n
        @ return new log content\n
        @ involve get mapping log of old log\n
        """
        new_log = Gumtree.gumtree.getNewLog()
        if new_log is not None:
            return new_log + ';'
        else:
            return new_log

    def get_old_log(self):
        """
        @ param nothing\n
        @ return old log content\n
        @ involve get old log content\n
        """
        return Gumtree.gumtree.getOldLog() + ';'

    def is_old_log_edited(self):
        """
        @ param nothing\n
        @ return true if log modified\n
        @ involve tell if log in old location has been edited\n
        """
        return Gumtree.gumtree.isOldLogEdited()

    def is_log_check_deleted(self):
        """
        @ param nothing\n
        @ return true if check modified\n
        @ involve tell if check of log in old hunk has modified\n
        """
        return Gumtree.gumtree.isLogCheckDeleted()

    def set_new_loc(self, line):
        """
        @ param line(int)\n
        @ return true is find new log\n
        @ involve find new log node for given line\n
        """
        return Gumtree.gumtree.setNewLoc(line)

    def get_old_loc(self):
        """
        @ param nothing\n
        @ return line(int)\n
        @ involve get old loc for the inserted node\n
        """
        return Gumtree.gumtree.getOldLoc()

    def add_old_log_nodes(self, lines):
        """
        @ param old log locations\n
        @ return nothing\n
        @ involve mark to be old log for nodes in given lines\n
        """
        for line in lines:
            Gumtree.gumtree.addOldLogNode(line)

    def add_new_log_nodes(self, lines):
        """
        @ param new log locations\n
        @ return nothing\n
        @ involve mark to be new log for nodes in given lines\n
        """
        for line in lines:
            Gumtree.gumtree.addNewLogNode(line)

    def get_hunk_edited_type(self):
        """
        @ param nothing\n
        @ return hunk edition type\n
        @ involve get action type for hunk\n
        """
        return Gumtree.gumtree.getActionType()

    def set_ddg_flag(self, is_new_hunk):
        """
        @ param true if in new hunk\n
        @ return nothing\n
        @ involve set ddg file info, true for locations in new hunk file\n
        """
        Gumtree.gumtree.setDDGFlag(is_new_hunk)
            
    def get_ddg_edited_type(self, ddg_locs):
        """
        @ param ddg locations in new or old hunks(index from 0)\n
        @ return true is ddg is modified\n
        @ involve tell whether data dependence nodes for control statement is modified\n
        """
        for ddg_loc in ddg_locs:
            Gumtree.gumtree.addDDGNode(ddg_loc)
        return Gumtree.gumtree.isDDGModified()

    def get_log_syntactical_edits_with_symbol(self): 
        """
        @ param already set old log and new log files\n
        @ return syntactical log edit scripts with tokens\n
        @ involve set old and new file and get log edit\n
        """
        return Gumtree.gumtree.getSyntacticalEditWithSymbol()
    
    def get_log_syntactical_edits(self):
        """
        @ param already set old log and new log\n
        @ return syntactical log edit scripts\n
        @ involve set old and new file and get log edit\n
        """
        return Gumtree.gumtree.getSyntacticalEdit()

    def recommend_log_syntactical_edits(self, old_log_file, new_log_file, candidate_log_file):
        """
        @ param old log file and new log file and candidate log file\n
        @ return recomended syntactical log edit scripts\n
        @ involve get recommended syntatictical log edit scripts with three files which are connectted through old file\n
        """
        # Gumtree.gumtree.setOldAndNewFile(old_file, new_file)
        return Gumtree.gumtree.recommendSyntacticalEdit(old_log_file, new_log_file, candidate_log_file)

    def get_log_edited_type(self):
        """
        @ param nothing\n
        @ return log edition type(update,remove,add) x (log, variable, content)\n
        @ involve tell whethwe log node is modified\n
        """
        return list(Gumtree.gumtree.getLogEditType())

    def set_file(self, filename):
        """
        @ param filename\n
        @ return nothing\n
        @ involve set file\n
        """
        Gumtree.gumtree.setFile(filename)

    def set_loc(self, line):
        """
        @ param line(int)\n
        @ return true if find log in given line\n
        @ involve set loccation of log\n
        """
        return Gumtree.gumtree.setLoc(line)

    def get_log(self):
        """
        @ param nothing[call after set loc]\n
        @ return log content\n
        @ involve get log statement plus;\n
        """
        return Gumtree.gumtree.getLog() + ';'

    def get_block(self):
        """
        @ param nothing[call after set loc]\n
        @ return block content\n
        @ involve get block which contains log\n
        """
        return Gumtree.gumtree.getBlock()

    def get_function(self):
        """
        @ param nothing[call after set loc]\n
        @ return function content\n
        @ involve get function which contains log\n
        """
        return Gumtree.gumtree.getFunction()

    def get_function_loc(self):
        """
        @ param nothing[call after get function]\n
        @ return loc in function\n
        @ involve get loc of log in function\n
        """
        return Gumtree.gumtree.getFunctionLoc()

    def get_block_feature(self):
        """
        @ param nothing[call after get block]\n
        @ return block feature\n
        @ involve get feature vector for block[type vs frequence]\n
        """
        vector_str = Gumtree.gumtree.getBlockFeature()
        vector = vector_str[1:-1].split(",")
        vector = [int(i) for i in vector]
        return vector

    def get_block_type(self):
        """
        @ param nothing[call after get block]\n
        @ return block type\n
        @ involve get type vector of block\n
        """
        return Gumtree.gumtree.getBlockType()

    def is_match(self, old_log_file, new_log_file):
        """
        @ param old and new log file\n
        @ return true if match\n
        @ involve validate that no edition between old and new log file\n
        """
        Gumtree.gumtree.setOldAndNewFile(old_log_file, new_log_file)
        return Gumtree.gumtree.isMatch()

    def is_match_with_edit(self, old_log_file, new_log_file, repos_log_file):
        """
        @ param old and new log file, and repos log file\n
        @ return true if match\n
        @ involve validate that no actions in edited node between old and new log\n
        """
        Gumtree.gumtree.setOldAndNewFile(old_log_file, new_log_file)
        Gumtree.gumtree.getEditedNodes()
        return Gumtree.gumtree.isMatchWithEdit(repos_log_file)

    def get_word_edit(self, old_log_file, new_log_file):
        """
        @ param old and new log file\n
        @ return list of edited word and list of edit feature\n
        @ involve use gumtree to get edited ast node and corresponding elements\n
        """
        Gumtree.gumtree.setOldAndNewFile(old_log_file, new_log_file)
        edit_elements = list(Gumtree.gumtree.getWordEdit())
        edit_words = []
        edit_feature = []
        for edit_element in edit_elements:
            old_element = edit_element[0]
            new_element = edit_element[1]
            edit_words.append([old_element, new_element])
            edit_feature.append(abs(hash(new_element.lower()) - hash(old_element.lower())))

        return edit_words, edit_feature

    def get_word_edit_from_log(self, old_log, new_log):
        """
        @ param old and new log\n
        @ return list of edited words and list of edit feature\n
        @ involve split log into tokens, remove exact match tokens to get edit words\n
        """
        # split to get list of words
        old_log = my_util.remove_given_element('', \
                        re.split(my_constant.SPLIT_LOG, old_log))
        new_log = my_util.remove_given_element('', \
                        re.split(my_constant.SPLIT_LOG, new_log))
        # get edition(match and compute delta)
        edit_words = []
        edit_feature = []
        is_continue = True
        # stop if can not find new exact match
        while is_continue:
            is_continue = False
            for old_element in old_log:
                # remove both if find exact match
                if old_element in new_log:
                    new_log.remove(old_element)
                    old_log.remove(old_element)
                    is_continue = True
                    break
        edit_words.append(old_log)
        edit_words.append(new_log)
        # get edit feature = hash(new feature - old feature)
        old_feature = 0
        for old_element in old_log:
            old_feature += hash(old_element.lower())
        new_feature = 0
        for new_element in new_log:
            new_feature += hash(new_element.lower())
        edit_feature.append(new_feature - old_feature)
        return edit_words, edit_feature

def close_jvm():
    """
    @ param nothing\n
    @ return nothing\n
    @ involve close jvm(notice:just call at end of program)\n
    """
    shutdownJVM()

def get_edit_feature_from_edit_types(edit_types):
    """
    @ param edit types\n
    @ return edit feature\n
    @ involve specify edit feature for edit types involving text modification\n
    """
    # add log, delete log, update content
    old_log = []
    new_log = []
    for edit_type in edit_types:
        if edit_type == 'addLog':
            new_log.append('addLog')
            break
        if edit_type == 'removeLog':
            old_log.append('removeLog')
            break
        if 'Content' in edit_type:
            old_log.append('updateContent')
            break

    # get edition(match and compute delta)
    edit_feature = []
    # get edit feature = hash(new feature - old feature)
    old_feature = 0
    for old_element in old_log:
        old_feature += hash(old_element.lower())
    new_feature = 0
    for new_element in new_log:
        new_feature += hash(new_element.lower())
    edit_feature.append(new_feature - old_feature)
    return edit_feature

"""
main function
"""
if __name__ == "__main__":
    # old_file = 'second/download/httpd/gumtree/httpd_old_log_63.cpp'
    # new_file = 'second/download/httpd/gumtree/httpd_new_log_63.cpp'
    old_file = 'second/gumtree/c/old.cpp'
    new_file = 'second/gumtree/c/new.cpp'
    candidate_file = 'second/gumtree/c/candidate.cpp'
    gumtree = Gumtree()
    # print gumtree.recommend_log_syntactical_edits(old_file, new_file, candidate_file)
    print gumtree.get_log_syntactical_edits(old_file, new_file)
    print gumtree.get_log_syntactical_edits_with_symbol(old_file, new_file)
    # gumtree.set_old_new_file(old_file, new_file)
    # print gumtree.get_log_edited_type()
    # gumtree.set_old_loc(7)
    # gumtree.get_new_log()
    # old_log = 'ap_log_error(APLOG_MARK, APLOG_CRIT, errno, server_conf,\
    #             "make_secure_socket: for %s, WSAIoctl: (SO_SSL_SET_FLAGS)", addr);'
    # new_log = 'ap_log_error(APLOG_MARK, APLOG_CRIT, apr_get_netos_error(), sconf,\
    #                      "make_secure_socket: for %s, WSAIoctl: "\
    #                      (SO_SSL_SET_FLAGS), addr);'
    # print gumtree.get_word_edit_from_log(old_log, new_log)



  