#-*-coding: utf-8 -*-
"""
input: hunk info
BY: gumtree
output: log info
log info [hunk info, log type, old log statement, new log statement, log action]
"""
import csv
import sys
import re
import os
import commands
import base64
import json
from itertools import islice
from srcml_api import SrcmlApi
from gumtree_api import Gumtree
import gumtree_api
import my_constant
import my_util

reload(sys)
sys.setdefaultencoding('utf-8')

def _get_semantics_for_new_log(syntactical_edit, srcml):
    """
    @ param syntactical edits and srcml(already set old function and corresponding location)\n
    @ return semantical log edit scripts\n
    @ involve generate log edit scripts: first get syntactical edit scripts, then replace variables with semantics\n
    """
    # substitue old variables with semantics while keeping literals
    semantical_edit = ""
    edits = syntactical_edit.split('\n')
    for edit in edits:
        # retrieve codes in new file my_constant.EDIT_NEW_MARK***my_constant.EDIT_NEW_MARK
        content = re.search(my_constant.EDIT_NEW_MARK+r'(.*)'+my_constant.EDIT_NEW_MARK, edit)
        if content:
            content = content.group(1)
            is_literal = re.search(r'literal: (.*)', content) # do not modify literal
            is_literal = False
            if not is_literal:
                semantics = content
                is_name = re.search(r'name: .*', content)
                # substitue variables with semantics (function file, function loc)
                if is_name and srcml is not None:
                    semantics = srcml.get_semantics_for_variable(content)
                # remove detail info
                if semantics.find(':') != -1:
                    semantics = semantics[:semantics.find(':')]
                edit = edit.replace(my_constant.EDIT_NEW_MARK+content+my_constant.EDIT_NEW_MARK, \
                                        my_constant.EDIT_NEW_MARK+semantics+my_constant.EDIT_NEW_MARK)
        semantical_edit += edit
        semantical_edit += '\n'

    return semantical_edit

def _get_semantics_for_old_log(syntactical_edit, srcml):
    """
    @ param syntactical edits and srcml(already set old function and corresponding location)\n
    @ return semantical log edit scripts\n
    @ involve generate log edit scripts: first get syntactical edit scripts, then replace variables with semantics\n
    """
    # substitue old variables with semantics while keeping literals
    semantical_edit = ""
    edits = syntactical_edit.split('\n')
    for edit in edits:
        # retrieve codes in new file @@***@@
        # deal multiple @@
        old_pattern = my_constant.EDIT_OLD_MARK + r'([^@]*)' + my_constant.EDIT_OLD_MARK
        temp_edit = edit
        content = re.search(old_pattern, temp_edit)
        while content:
            content = content.group(1)
            is_literal = re.search(r'literal: (.*)', content) # do not modify literal
            is_literal = False
            if not is_literal:
                semantics = content
                is_name = re.search(r'name: .*', content)
                # substitue variables with semantics (function file, function loc)
                if is_name and srcml is not None:
                    semantics = srcml.get_semantics_for_variable(content)
                # remove detail info
                if semantics.find(':') != -1:
                    semantics = semantics[:semantics.find(':')]
                edit = edit.replace(my_constant.EDIT_OLD_MARK +content+my_constant.EDIT_OLD_MARK, my_constant.EDIT_OLD_MARK+semantics+my_constant.EDIT_OLD_MARK)

            # find next content
            temp_edit = temp_edit.replace(my_constant.EDIT_OLD_MARK+content+my_constant.EDIT_OLD_MARK, '')
            content = re.search(old_pattern, temp_edit)

        semantical_edit += edit
        semantical_edit += '\n'

    return semantical_edit

def _get_hash_for_semantics(semantical_edit):
    """
    @ param semantical edits\n
    @ return hash number\n
    @ involve hash semantical edits by calculating the difference between literals\n
    """
    edits = semantical_edit.split('\n')
    hash_number = 0
    for edit in edits:
        # find update literal to literal
        update_literal = re.search(r'update\t' + my_constant.EDIT_OLD_MARK + r'literal: "(.*)"' + my_constant.EDIT_OLD_MARK \
          +r'\tto\t' + my_constant.EDIT_NEW_MARK + r'literal: "(.*)"' +  my_constant.EDIT_NEW_MARK+ r'literal:.*' +  my_constant.EDIT_NEW_MARK, edit)
        if update_literal:
            hash_diff = 0
            old_literals = my_util.remove_given_element('', \
                        re.split(my_constant.SPLIT_LOG, update_literal.group(1)))
            new_literals = my_util.remove_given_element('', \
                        re.split(my_constant.SPLIT_LOG, update_literal.group(2)))
            for new_literal in new_literals:
                hash_diff += hash(new_literal.lower())
            for old_literal in old_literals:
                hash_diff -= hash(old_literal.lower())
            hash_number += hash_diff
        else:
            hash_number += hash(edit)

    return hash_number

def deal_log( log_record, gumtree, log_records, total_log):
    """
    @ param log record, gumtree object and log records and log counter\n
    @ return log counter and log records\n
    @ involve deal with each log and save log info[function and edition]\n
    """
    # filter log that has no modification LOG_NO_MODIFY
    action_type = log_record[my_constant.FETCH_LOG_ACTION_TYPE]
    if int(action_type) % 2 == 0:
        return total_log, log_records
    # old loc and old file
    old_loc = log_record[my_constant.FETCH_LOG_OLD_LOC]
    old_file = log_record[my_constant.FETCH_LOG_OLD_FILE]

    new_loc = log_record[my_constant.FETCH_LOG_NEW_LOC]
    new_file = log_record[my_constant.FETCH_LOG_NEW_FILE]

    temp_file = my_constant.GUMTREE_DIR + 'temp.cpp'
    # get old function and new function and corresponding location
    old_function = new_function = new_log = old_log = ''
    old_function_loc = new_function_loc = -1
    old_function_file_name = my_constant.SAVE_OLD_FUNCTION + str(total_log) + '.cpp'
    # parse old log if is not inserted
    if old_loc != '-1':
        # use srcml parser(.cpp temp file)
        my_util.copy_file(old_file, temp_file)
        gumtree.set_file(temp_file)
        if gumtree.set_loc(int(old_loc)):
            old_log = gumtree.get_log()
            old_function = gumtree.get_function()
            old_function_loc = gumtree.get_function_loc()
            my_util.save_file(old_function, old_function_file_name)
    # parse new log if is not deleted
    new_function_file_name = my_constant.SAVE_NEW_FUNCTION + str(total_log) + '.cpp'
    if new_loc != '-1':
        my_util.copy_file(new_file, temp_file)
        gumtree.set_file(temp_file)
        if gumtree.set_loc(int(new_loc)):
            new_log = gumtree.get_log()
            # refresh function if is insert(update so care about old context)
            new_function = gumtree.get_function()
            new_function_loc = gumtree.get_function_loc()
            my_util.save_file(new_function, new_function_file_name)
    # write old and new log file as well as function file
    # # get edit word and feature
    # edit_words, edit_feature = gumtree.get_word_edit_from_log(old_log, new_log)    
    old_log_file = "test/temp_old_log_file.cpp"
    my_util.save_file(old_log, old_log_file)
    new_log_file = "test/temp_new_log_file.cpp"
    my_util.save_file(new_log, new_log_file)
    # get edit type and edit word and edit feature
    gumtree.set_old_new_file(old_log_file, new_log_file)
    srcml = SrcmlApi()
    if new_loc == '-1': # remove log, only old edited
        edit_types = ['removeLog']
    elif old_loc == '-1': # add log, only new edited
        edit_types = ['addLog']
    else:
        edit_types = gumtree.get_log_edited_type()
    syntactical_edits = gumtree.get_log_syntactical_edits_with_symbol()
    semantical_edits = syntactical_edits
    if old_function_loc != -1: # has old. try to replace old
        srcml.set_function_file(old_function_file_name)
        if srcml.set_log_loc(old_function_loc):
            semantical_edits = _get_semantics_for_old_log(semantical_edits, srcml)
        else:
            semantical_edits = _get_semantics_for_old_log(semantical_edits, None)
            print 'WARN: no log in %s: %s, file info %s: %s' %(old_function_file_name, old_function_loc, old_file, old_loc)
    if new_function_loc != -1: # has new. try to replace new
        srcml.set_function_file(new_function_file_name)
        if srcml.set_log_loc(new_function_loc):
            semantical_edits = _get_semantics_for_new_log(semantical_edits, srcml)
        else: 
            semantical_edits = _get_semantics_for_new_log(semantical_edits, None)
            print 'WARN: no log in %s: %d, file info %s: %s' %(new_function_file_name, new_function_loc, new_file, new_loc)
    edit_feature = _get_hash_for_semantics(semantical_edits)
    edit_word, temp = gumtree.get_word_edit_from_log(old_log, new_log)

    log_record[my_constant.FETCH_LOG_OLD_LOG] = old_log
    log_record[my_constant.FETCH_LOG_NEW_LOG] = new_log
    log_records.append(log_record + [old_function_file_name, old_function_loc, new_function_file_name, new_function_loc,\
                     json.dumps(edit_types), syntactical_edits, semantical_edits, json.dumps(edit_word), edit_feature])
    total_log += 1

    return total_log, log_records

def filter_reverted_log_revisions(log_records):
    """
    @ param log records\n
    @ return filtered log records \n
    @ involve compare sorted log records one by one and choose the one that have not been reverted\n
    """
    index = 0
    while index < len(log_records):
        log_record_old = log_records[index]
        for log_record_new in log_records:
            # new file of old log record
            new_file_for_old_record = log_record_old[my_constant.FETCH_LOG_NEW_FILE]
            old_file_for_new_record = log_record_new[my_constant.FETCH_LOG_OLD_FILE]
            if new_file_for_old_record == old_file_for_new_record: # sequential revisions
                # reverted log (old log for old== new log for new)
                old_log_for_old = log_record_old[my_constant.FETCH_LOG_OLD_LOG]
                new_log_for_new = log_record_new[my_constant.FETCH_LOG_NEW_LOG]
                if old_log_for_old == new_log_for_new:
                    log_records.remove(log_record_old)
                    index -= 1 # do not update index
                    break
        
        index += 1 # increase index each time

    return log_records

def fetch_old_new_gumtree(gumtree):
    """
    @ param gumtree object\n
    @ return nothing \n
    @ involve fetch and analyze each log record\n
    """
    # read record from fetched log
    log_file = file(my_constant.FETCH_LOG_FILE_NAME, 'rb')
    log_records = csv.reader(log_file)
    old_new_gumtree_file = file(my_constant.ANALYZE_OLD_NEW_GUMTREE_FILE_NAME, 'wb')
    old_new_gumtree_writer = csv.writer(old_new_gumtree_file)
    old_new_gumtree_writer.writerow(my_constant.ANALYZE_OLD_NEW_GUMTREE_TITLE)

    old_new_records = []
    # call deal log to deal with each record
    total_log = 0
    total_record = 0
    log_size, log_records =  my_util.get_csv_record_len(log_records)
    for log_record in islice(log_records, 1, None):
        total_record += 1
        total_log, old_new_records = deal_log(log_record, gumtree, old_new_records, total_log)
        if total_record % 10 == 0:
            print 'have dealed with %d/%d record, have dealed with %d log' %(total_record, log_size, total_log)
    # filter log records
    old_new_records = filter_reverted_log_revisions(old_new_records)
    for record in old_new_records:
        old_new_gumtree_writer.writerow(record)

    # close file
    log_file.close()
    old_new_gumtree_file.close()

def analyze_old_new(is_rebuild = False):
    """
    @ param flag about whether rebuild(function and edition info)\n
    @ return nothing \n
    @ involve fetch and analyze each log[ddg and cdg]\n
    """
    # if to rebuild, then call fetch_old_new_gumtree to analyze log record
    gumtree = Gumtree()
    if is_rebuild:
        fetch_old_new_gumtree(gumtree)
    # intiate csv file
    old_new_gumtree_file = file(my_constant.ANALYZE_OLD_NEW_GUMTREE_FILE_NAME, 'rb')
    old_new_gumtree_records = csv.reader(old_new_gumtree_file)
    old_new_llvm_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'wb')
    old_new_llvm_writer = csv.writer(old_new_llvm_file)
    old_new_llvm_writer.writerow(my_constant.ANALYZE_OLD_NEW_LLVM_TITLE)

    total_record = 0
    total_log = 0
    old_new_gumtree_size, old_new_gumtree_records = my_util.get_csv_record_len(old_new_gumtree_records)
    for record in islice(old_new_gumtree_records, 1, None):
        if total_record % 10 == 0:
            print 'have dealed with %d/%d record; %d log' %(total_record, old_new_gumtree_size, total_log)
        total_record += 1
        # call srcml to get check and variable info
        function = ''
        function_loc = -1
        if record[my_constant.FETCH_LOG_OLD_LOC] != '-1': # has old -> old
            function = record[my_constant.ANALYZE_OLD_FUNCTION]
            function_loc = int(record[my_constant.ANALYZE_OLD_FUNCTION_LOC])
        else:
            function = record[my_constant.ANALYZE_NEW_FUNCTION]
            function_loc = int(record[my_constant.ANALYZE_NEW_FUNCTION_LOC])
            
        srcml = SrcmlApi()
        srcml.set_function_file(function)
        check = []
        variable = []
        if srcml.set_log_loc(function_loc):
            if srcml.set_control_dependence():
                check = srcml.get_control_info()
                variable = srcml.get_log_info()
        # do not keep empty check(not diagnosis log)
        if check == []:
            continue
        # depended statement locations
        ddg_codes = set()
        ddg_locs = set()
        old_loc = record[my_constant.FETCH_LOG_OLD_LOC]
        new_loc = record[my_constant.FETCH_LOG_NEW_LOC]
        is_new_hunk = None
        # insert log, in new hunk
        if old_loc == '-1':
            is_new_hunk = True
            hunk_loc = int(record[my_constant.FETCH_HUNK_NEW_HUNK_LOC])
        # delete log, in old hunk
        elif new_loc == '-1':
            is_new_hunk = False
            hunk_loc = int(record[my_constant.FETCH_HUNK_OLD_HUNK_LOC])
        else:
            old_new_llvm_writer.writerow(record + [json.dumps(check), json.dumps(variable), ddg_codes, ddg_locs])
            total_log += 1
            continue
        # filter by no check dependence is insert or delete for insert or delete log
        ddg_locs = srcml.get_control_depenedence_loc()
        constant = hunk_loc - function_loc
        # function loactions -> hunk locations
        ddg_hunk_locs = set()
        for ddg_loc in ddg_locs:
            ddg_hunk_locs.add(constant + ddg_loc)
        # use gumtree to justify whether check of hunk is edited or not
        gumtree.set_old_new_file(record[my_constant.FETCH_HUNK_OLD_HUNK_FILE], record[my_constant.FETCH_HUNK_NEW_HUNK_FILE])
        gumtree.set_ddg_flag(is_new_hunk)
        if gumtree.get_ddg_edited_type(ddg_hunk_locs):
            record[my_constant.FETCH_LOG_ACTION_TYPE] = my_constant.LOG_DDG_MODIFY
            continue
        old_new_llvm_writer.writerow(record + [json.dumps(check), json.dumps(variable), ddg_codes, ddg_hunk_locs])
        total_log += 1

    # close file
    old_new_gumtree_file.close()
    old_new_llvm_file.close()


"""
main function
"""
if __name__ == "__main__":
    gumtree = Gumtree()
    fetch_old_new_gumtree(gumtree)
    gumtree_api.close_jvm()
    # a = [1,2,3]
    # index = 0
    # while index < len(a):
    #     for ele_b in a:
    #         print a[index]
    #         print a
    #         print ele_b
    #         print "next"
    #         a.remove(a[index])
    #         break
