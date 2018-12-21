#-*-coding: utf-8 -*-
import os
import xlwt
import commands
import re
import csv
import json
from itertools import islice
import my_util
import my_constant
import cluster_api
import analyze_control_repos
from gumtree_api import Gumtree
from srcml_api import SrcmlApi


def get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, candidate_log):
    """
    @ param gumtree object, srcml object(may be none, has set function and function loc), old log, new log, candidate log\n
    @ return recommended log edit scripts\n
    @ involve generate log edit scripts: first get syntactical edit scripts, then remove variables with semantics\n
    """
    # get syntactical edit scripts
    candidate_log_file = "test/temp_candidate_log_file.cpp"
    my_util.save_file(candidate_log + ';', candidate_log_file)
    syntactical_edit_scripts = gumtree.recommend_log_syntactical_edits(old_log_file, new_log_file, candidate_log_file)

    # substitue variables with semantics while keeping literals
    recommended_log_edits = ""
    edits = syntactical_edit_scripts.split('\n')
    for edit in edits:
        # retrieve codes in new file $$***$$
        content = re.search(r'\$\$(.*)\$\$', edit)
        if content:
            content = content.group(1)
            is_literal = re.search(r'(literal: )*"(.*)"', content)
            # do not deal with literal
            # substitue variables with semantics (function file, function loc)
            if not is_literal and srcml is not None:
                semantics = srcml.get_semantics_for_variable(content)
                # semantics = "srcml_output"
                edit = edit.replace('$$'+content+'$$', '$$'+semantics+'$$')
        recommended_log_edits += edit
        recommended_log_edits += '\n'
    
    return recommended_log_edits

def check_given_log_in_function(function_name, check, variable, postfix=''):
    """
    @ param function name, check and variable constaints and postfix\n
    @ return true if has that kind of log\n
    @ involve traverse log analysis data and try to find logs statisfying given constraints\n
    """
    log_file = file(my_util.concate_file(\
            my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix), 'rb')
    log_records = csv.reader(log_file)
    flag_meet_function = False
    for log_record in islice(log_records, 1, None):
        # logs in given function
        if log_record[my_constant.ANALYZE_REPOS_LOG_FUNCTION] == function_name:
            flag_meet_function = True
            # filter with check and variable info
            # if check == json.loads(log_record[my_constant.ANALYZE_REPOS_LOG_CHECK]):
            if my_util.is_sub_list(check, json.loads(log_record[my_constant.ANALYZE_REPOS_LOG_CHECK])):
                if variable == json.loads(log_record[my_constant.ANALYZE_REPOS_LOG_VARIABLE]):
                    log_file.close()
                    return "accept-false-variable"
                else:
                    log_file.close()
                    return "accept-false-check"
        # records store by function name, so quit if meet new function name
        elif flag_meet_function:
            log_file.close()
            return "accpept-true"

    log_file.close()
    return "accpept-true"

def check_for_insert_rule(rule_feature, function, postfix=''):
    """
    @ param rule feature(check, variable) and function name and postfix\n
    @ return true if need insert log\n
    @ involve check whether there is log that do given check and output given variable, if do, return false\n
    """
    check = rule_feature[0]
    variable = rule_feature[1]
    # has log -> no need
    return check_given_log_in_function(function, check, variable, postfix)

def check_for_modify_rule(edit_words, curr_log):
    """
    @ param edit words(old edits and new edits)\n
    @ return true if need edit\n
    @ involve check whether current log has not old edit and has new edit, if do, then return false\n
    """
    old_edits = edit_words[0]
    new_edits = edit_words[1]

    # log to word list
    curr_log = my_util.remove_given_element('',\
             re.split(my_constant.SPLIT_LOG, curr_log))
    curr_log_copy = list(curr_log)
    # just add new things
    if old_edits == []:
        for new_edit in new_edits:
            # do not has all new
            if new_edit not in curr_log_copy:
                return "accept-true"
            curr_log_copy.remove(new_edit)
        # has all new edit
        return "accept-false"
    # update old, so check whether old exist
    for old_edit in old_edits:
        # do not have all old log -> reject(do not have all new)\
        #                      or accept-false(new is [] or have all new)
        if old_edit not in curr_log:
            # for deleted log, must be same old log
            if new_edits == []:
                return "reject"
            for new_edit in new_edits:
                # do not has all new, and do not has all old
                if new_edit not in curr_log_copy:
                    return "reject"
                curr_log_copy.remove(new_edit)
            # has all new edit -> do not need edit
            return "accept-false"
        # remove matched edit
        curr_log.remove(old_edit)

    # has all old edit -> need edit
    return "accept-true"

def filter_insert_rule(rule_feature, none_ratio=0.5):
    """
    @ param rule feature, maximum none ratio of insert rule feature\n
    @ return true if pass filter\n
    @ involve check insert rule feature must not has more none feature than maximum none ratio\n
    """
    rule_feature = rule_feature[0] + rule_feature[1]
    function_semantics_counter = 0
    for feature in rule_feature:
        if my_util.is_function_semantics(feature):
            function_semantics_counter += 1
    if function_semantics_counter < len(rule_feature) * (1 - none_ratio):
        return False
    else:
        return True

def is_match_for_insert_rule(rule_feature, function_feature):
    """
    @ param rule feature(check, variable) and function feature(calls, types)\n
    @ return true if match\n
    @ involve validate that any element in rule feature must exist in function\n
    """
    # variable = rule_feature[1]
    calls = function_feature[0]
    types = function_feature[1]
    # validate whether any one in check or variable is in calls and types
    rule_infos = rule_feature[0] + rule_feature[1]
    function_info = calls + types
    for info in rule_infos:
        if info is None:
            continue
        infos = info.split('.')
        for info in infos:
            if info != 'None' and not info.replace('_ret','').replace('_arg','') in function_info:
                return False
    return True

def is_match_for_modify_rule(rule_feature, repos_log_feature):
    """
    @ param rule feature(check, variable) and repos log feature(check, variable)\n
    @ return true if match\n
    @ involve validate that check and variable info must be exactly same\n
    """
    return rule_feature == repos_log_feature

def _check_repos_info(repos_name, repos_list=[], rebuild_repos=False, postfix=''):
    """
    @ param repos name and repos list of analyzed repos and flag: true if srcml api update), file postfix\n
    @ return nothing\n
    @ involve create repos info for given old repos name if need\n
    """
    # has file
    if os.path.isfile(my_util.concate_file(my_constant.ANALYZE_REPOS_LOG_FILE_NAME, \
                    postfix)):
        # need rebuild, then check dict(in dict -> nothing)
        if rebuild_repos:
            if repos_name in repos_list:
                return repos_list
        # do not need rebuild -> nothing
        else:
            return repos_list
    # has no file or has file and no key -> re analyze repos
    # analyze repos of given repos name and postfix
    analyze_control_repos.analyze_repos(repos_name, postfix=postfix)    
    # only cluster log for fix repos
    if postfix == my_constant.LAST_REPOS or postfix == '':
        analyze_control_repos.cluster_repos_log(postfix)
    # add to dict
    repos_list.append(repos_name)
    return repos_list

def seek_clone(repos_name, rebuild_repos=False, postfix=''):
    """
    @ param postfix: repos info files \n
    @ return nothing \n
    @ involve match rule class against given repos log class and function\n
    """
    # check repos according to rebuild repos flag(warn:no repos lis_
    #t)
    _check_repos_info(repos_name, [], rebuild_repos, postfix)
    repos_log_class_file = file(my_util.concate_file(\
                my_constant.CLASS_REPOS_LOG_FILE_NAME, postfix), 'rb')
    repos_log_records = csv.reader(repos_log_class_file)
    repos_function_file = file(my_util.concate_file(\
                my_constant.ANALYZE_REPOS_FUNCTION_FILE_NAME, postfix), 'rb')
    repos_function_records = csv.reader(repos_function_file)
    repos_function_records = list(repos_function_records)
    repos_log_records = list(repos_log_records)


    # initiate csv writer file(repos log clone and function clone)
    repos_log_clone_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, postfix), 'wb')
    repos_log_clone_writer = csv.writer(repos_log_clone_file)
    repos_log_clone_writer.writerow(my_constant.ANALYZE_CLONE_LOG_TITLE)
    repos_function_clone_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, postfix), 'wb')
    repos_function_clone_writer = csv.writer(repos_function_clone_file)
    repos_function_clone_writer.writerow(my_constant.ANALYZE_CLONE_FUNCTION_TITLE)

    # initiate csv reader file(rule class, repos log class, function class)
    rule_file = file(my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, 'rb')
    rule_records = csv.reader(rule_file)
    rule_counter = 0
    rule_size, rule_records = my_util.get_csv_record_len(rule_records)
    # search clone instance for each rule
    gumtree = Gumtree()
    for rule_record in islice(rule_records, 1, None):
        rule_counter += 1
        print 'now processing rule %d/%d, ' %(rule_counter, rule_size),

        # old log file, new log file, function file and function loc
        old_loc = rule_record[my_constant.CLASS_OLD_NEW_OLD_LOC]
        old_log_file = "test/temp_old_log_file.cpp"
        my_util.save_file(rule_record[my_constant.CLASS_OLD_NEW_OLD_LOG], old_log_file)
        new_log_file = "test/temp_new_log_file.cpp"
        my_util.save_file(rule_record[my_constant.CLASS_OLD_NEW_NEW_LOG], new_log_file)
        new_file = "test/temp_new_file.cpp"
        print rule_record[my_constant.CLASS_OLD_NEW_NEW_FILE_NAME]
        my_util.copy_file(rule_record[my_constant.CLASS_OLD_NEW_NEW_FILE_NAME], new_file)
        # srcml for new function file
        srcml = None
        if rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC] != '-1':
            srcml = SrcmlApi()
            srcml.set_function_file(rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION])
            if not srcml.set_log_loc(int(rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC])):
                srcml = None
        # check, variable, edit words
        check = json.loads(rule_record[my_constant.CLASS_OLD_NEW_CHECK])
        variable = json.loads(rule_record[my_constant.CLASS_OLD_NEW_VARIABLE])
        edit_words = json.loads(rule_record[my_constant.CLASS_OLD_NEW_EDIT_WORD])
        rule_feature = [check, variable]
        clone_counter_function = 0
        clone_counter_log = 0
        # insert rule -> function records
        if old_loc == '-1':
            # filter insert rule by info
            if not filter_insert_rule(rule_feature):
                    continue
            for repos_function_record in islice(repos_function_records, 1, None):
                calls = json.loads(repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_CALLS])
                types = json.loads(repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_TYPES])
                if is_match_for_insert_rule(rule_feature, [types, calls]):
                    if clone_counter_function > my_constant.MAX_FUNCTION_CLONE:
                        print 'too many candidate functions -> invalid rules'
                        break
                    clone_counter_function += 1
                    recommended_log_edits = get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, "")
                    necessity = check_for_insert_rule(rule_feature, \
                repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_FUNCTION_NAME], postfix)
                    repos_function_clone_writer.writerow(rule_record + \
                                              repos_function_record + [recommended_log_edits, necessity])
        # modification rule -> log records
        else:
            for repos_log_record in islice(repos_log_records, 1, None):
                log_check = json.loads(repos_log_record[my_constant.CLASS_REPOS_LOG_CHECK])
                log_variable = json.loads(repos_log_record[my_constant.CLASS_REPOS_LOG_VARIABLE])
                if is_match_for_modify_rule(rule_feature, [log_check, log_variable]):
                    # get real log records from class index
                    analyze_log_records = cluster_api.generate_records_for_class(my_util.concate_file(\
                            my_constant.CLUSTER_REPOS_LOG_FILE_NAME, postfix), repos_log_record[0])
                    for analyze_log_record in analyze_log_records:
                        clone_counter_log += 1
                        recommended_log_edits = get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, analyze_log_record[my_constant.ANALYZE_REPOS_LOG_LOG])
                        necessity = check_for_modify_rule(edit_words, \
                                analyze_log_record[my_constant.ANALYZE_REPOS_LOG_LOG])
                        repos_log_clone_writer.writerow(rule_record + \
                                            analyze_log_record[:-1] + [recommended_log_edits, necessity])

        print 'find clone instances, function: %d, log: %d' \
                         %(clone_counter_function, clone_counter_log)

    # close file
    rule_file.close()
    repos_log_class_file.close()
    repos_function_file.close()
    repos_function_clone_file.close()
    repos_log_clone_file.close()

def seek_clone_for_lastest_repos(rebuild_repos=False):
    """
    @ param flag: true if need rebuild repos info\n
    @ return nothing\n
    @ involve match every rule against latest repos\n
    """
    seek_clone(my_constant.LAST_REPOS, rebuild_repos, my_constant.LAST_REPOS)

def seek_clone_for_corresponding_repos(rebuild_repos=False, is_train=''):
    """
    @ param true if need reanalyze repos database(e.g. srcml_api update)\n
    @ return nothing \n
    @ involve match each rule with their corresponding repos(log and function)\n
    """
    # initiate csv reader file(rule class, repos log class, function class)
    rule_file_name = my_util.concate_file(my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, is_train)
    rule_file = file(rule_file_name, 'rb')
    rule_records = csv.reader(rule_file)
    # initiate csv writer file(repos log clone and function clone)
    repos_log_clone_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_rule'+is_train), 'wb')
    repos_log_clone_writer = csv.writer(repos_log_clone_file)
    repos_log_clone_writer.writerow(my_constant.ANALYZE_CLONE_LOG_TITLE)
    repos_function_clone_file = file(my_util.concate_file(\
                    my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, '_rule'+is_train), 'wb')
    repos_function_clone_writer = csv.writer(repos_function_clone_file)
    repos_function_clone_writer.writerow(my_constant.ANALYZE_CLONE_FUNCTION_TITLE)
    rule_counter = 0
    # get length and transfer iterator to list
    rule_size, rule_records = my_util.get_csv_record_len(rule_records)
    # list of analyzed reposes
    repos_list = []
    # search clone instance for each rule
    gumtree = Gumtree()
    for rule_record in islice(rule_records, 1, None):
        rule_counter += 1
        print 'now processing rule %d/%d, ' %(rule_counter, rule_size)
        # get cluster record from rule class, since one rule may correspond to multi reposes

        rule_cluster_records = cluster_api.generate_records_for_class(\
                my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, rule_record[0])
        # old log file, new log file, function file and function loc
        old_loc = rule_record[my_constant.CLASS_OLD_NEW_OLD_LOC]
        old_log_file = "test/temp_old_log_file.cpp"
        my_util.save_file(rule_record[my_constant.CLASS_OLD_NEW_OLD_LOG], old_log_file)
        new_log_file = "test/temp_new_log_file.cpp"
        my_util.save_file(rule_record[my_constant.CLASS_OLD_NEW_NEW_LOG], new_log_file)
        # srcml for new function file
        srcml = None
        if rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC] != '-1':
            srcml = SrcmlApi()
            srcml.set_function_file(rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION])
            if not srcml.set_log_loc(int(rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC])):
                srcml = None
        # check, variable, edit words
        check = json.loads(rule_record[my_constant.CLASS_OLD_NEW_CHECK])
        variable = json.loads(rule_record[my_constant.CLASS_OLD_NEW_VARIABLE])
        edit_words = json.loads(rule_record[my_constant.CLASS_OLD_NEW_EDIT_WORD])
        rule_feature = [check, variable]
        # deal with each repos for this rule
        rule_repos_list = []
        for rule_cluster_record in rule_cluster_records:
            # get repos info files with old repos name
            old_repos_name = my_util.get_old_repos_name(rule_cluster_record[0])
            postfix = '_' + old_repos_name
            repos_list = _check_repos_info(old_repos_name, repos_list, rebuild_repos, postfix)
            # do not reanalyze rule
            if old_repos_name in rule_repos_list:
                continue
            rule_repos_list.append(old_repos_name)
            # clone counter
            clone_counter_function = 0
            clone_counter_log = 0
            # insert rule -> function records
            if old_loc == '-1':
                # filter insert rule with information ratio
                if not filter_insert_rule(rule_feature):
                    continue
                repos_function_file = file(my_util.concate_file(\
                        my_constant.ANALYZE_REPOS_FUNCTION_FILE_NAME, postfix))
                repos_function_records = csv.reader(repos_function_file)
                for repos_function_record in islice(repos_function_records, 1, None):
                    calls = json.loads(repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_CALLS])
                    types = json.loads(repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_TYPES])
                    # match rule info against function info
                    if is_match_for_insert_rule(rule_feature, [types, calls]):                    
                        if clone_counter_function > my_constant.MAX_FUNCTION_CLONE:
                            print 'too many candidate functions -> invalid rules'
                            break
                        clone_counter_function += 1
                        recommended_log_edit = get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, "")
                        necessity = check_for_insert_rule(rule_feature, \
                    repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_FUNCTION_NAME], postfix)
                        repos_function_clone_writer.writerow(rule_record + repos_function_record + [recommended_log_edit, necessity])
                # close file
                repos_function_file.close()
            # modification rule -> log records
            else:
                repos_log_file = file(my_util.concate_file(\
                            my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix))
                repos_log_records = csv.reader(repos_log_file)
                for repos_log_record in islice(repos_log_records, 1, None):
                    log_check = json.loads(repos_log_record[my_constant.ANALYZE_REPOS_LOG_CHECK])
                    log_variable = json.loads(repos_log_record[my_constant.ANALYZE_REPOS_LOG_VARIABLE])
                    # match rule info against log info
                    if is_match_for_modify_rule(rule_feature, [log_check, log_variable]):
                        clone_counter_log += 1
                        recommended_log_edit = get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, repos_log_record[my_constant.ANALYZE_REPOS_LOG_LOG])
                        necessity = check_for_modify_rule(edit_words, \
                                repos_log_record[my_constant.ANALYZE_REPOS_LOG_LOG])
                        repos_log_clone_writer.writerow(rule_record + repos_log_record + [recommended_log_edit, necessity])

                # close repos info files
                repos_log_file.close()
        print 'find clone instances, function: %d, log: %d' \
                        %(clone_counter_function, clone_counter_log)

    # close file
    repos_function_clone_file.close()
    repos_log_clone_file.close()

def seek_clone_for_train_rule(repos_name, repos_log_clone_writer,repos_function_clone_writer, rebuild_repos=False):
    """
    @ param repos name, clone file writer and flag about whether rebuild repos \n
    @ return nothing \n
    @ involve match rule class against given repos log class and function\n
    """
    # check repos according to rebuild repos flag(warn:no repos list)
    postfix = '_'+repos_name
    # print postfix
    _check_repos_info(repos_name, [], rebuild_repos, postfix)
    # repos_log_class_file = file(my_util.concate_file(\
    #             my_constant.CLASS_REPOS_LOG_FILE_NAME, postfix), 'rb')
    repos_log_file = file(my_util.concate_file(\
                            my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix), 'rb')
    repos_log_records = csv.reader(repos_log_file)
    repos_function_file = file(my_util.concate_file(\
                my_constant.ANALYZE_REPOS_FUNCTION_FILE_NAME, postfix), 'rb')
    repos_function_records = csv.reader(repos_function_file)
    repos_function_records = list(repos_function_records)
    repos_log_records = list(repos_log_records)

    # initiate csv reader file(rule class, repos log class, function class)
    rule_file_name = my_util.concate_file(my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, '_train')
    rule_file = file(rule_file_name, 'rb')
    rule_records = csv.reader(rule_file)
    rule_counter = 0
    rule_size, rule_records = my_util.get_csv_record_len(rule_records)
    # search clone instance for each rule
    gumtree = Gumtree()
    for rule_record in islice(rule_records, 1, None):
        rule_counter += 1
        print 'now processing rule %d/%d, ' %(rule_counter, rule_size),

        # old log file, new log file, function file and function loc
        old_loc = rule_record[my_constant.CLASS_OLD_NEW_OLD_LOC]
        old_log_file = "test/temp_old_log_file.cpp"
        my_util.save_file(rule_record[my_constant.CLASS_OLD_NEW_OLD_LOG], old_log_file)
        new_log_file = "test/temp_new_log_file.cpp"
        my_util.save_file(rule_record[my_constant.CLASS_OLD_NEW_NEW_LOG], new_log_file)
        srcml = None
        if rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC] != '-1':
            srcml = SrcmlApi()
            srcml.set_function_file(rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION])
            if not srcml.set_log_loc(int(rule_record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC])):
                srcml = None
        # check, variable, edit words
        check = json.loads(rule_record[my_constant.CLASS_OLD_NEW_CHECK])
        variable = json.loads(rule_record[my_constant.CLASS_OLD_NEW_VARIABLE])
        edit_words = json.loads(rule_record[my_constant.CLASS_OLD_NEW_EDIT_WORD])
        rule_feature = [check, variable]

        clone_counter_function = 0
        clone_counter_log = 0
        # insert rule -> function records
        if old_loc == '-1':
            # filter insert rule by info
            if not filter_insert_rule(rule_feature):
                    continue
            for repos_function_record in islice(repos_function_records, 1, None):
                calls = json.loads(repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_CALLS])
                types = json.loads(repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_TYPES])
                if is_match_for_insert_rule(rule_feature, [types, calls]):
                    if clone_counter_function > my_constant.MAX_FUNCTION_CLONE:
                        print 'too many candidate functions -> invalid rules'
                        break
                    clone_counter_function += 1
                    recommended_log_edit = get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, "")
                    necessity = check_for_insert_rule(rule_feature, \
                repos_function_record[my_constant.ANALYZE_REPOS_FUNCTION_FUNCTION_NAME], postfix)
                    repos_function_clone_writer.writerow(rule_record + \
                                              repos_function_record + [recommended_log_edit, necessity])
        # modification rule -> log records
        else:
            for repos_log_record in islice(repos_log_records, 1, None):
                log_check = json.loads(repos_log_record[my_constant.ANALYZE_REPOS_LOG_CHECK])
                log_variable = json.loads(repos_log_record[my_constant.ANALYZE_REPOS_LOG_VARIABLE])
                if is_match_for_modify_rule(rule_feature, [log_check, log_variable]):
                    clone_counter_log += 1
                    recommended_log_edit = get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, repos_log_record[my_constant.ANALYZE_REPOS_LOG_LOG])
                    necessity = check_for_modify_rule(edit_words, \
                            repos_log_record[my_constant.ANALYZE_REPOS_LOG_LOG])
                    repos_log_clone_writer.writerow(rule_record + \
                                        repos_log_record + [recommended_log_edit, necessity])

        print 'find clone instances, function: %d, log: %d' \
                         %(clone_counter_function, clone_counter_log)

    # close file
    rule_file.close()
    repos_log_file.close()
    repos_function_file.close()

def seek_clone_for_history_repos_train(rebuild_repos=False):
    """
    @ param flag: true if need rebuild repos info\n
    @ return nothing\n
    @ involve match every rule against every repos except the last repos\n
    """
    # get all versions
    versions = commands.getoutput('ls ' + my_constant.REPOS_DIR)
    versions = versions.split('\n')
    versions.sort(key=my_util.get_version_number)
    # initiate csv writer file(repos log clone and function clone)
    repos_log_clone_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_train'), 'wb')
    repos_log_clone_writer = csv.writer(repos_log_clone_file)
    repos_log_clone_writer.writerow(my_constant.ANALYZE_CLONE_LOG_TITLE)
    repos_function_clone_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, '_train'), 'wb')
    repos_function_clone_writer = csv.writer(repos_function_clone_file)
    repos_function_clone_writer.writerow(my_constant.ANALYZE_CLONE_FUNCTION_TITLE)
    for version in versions[:-1]:
        seek_clone_for_train_rule(version, repos_log_clone_writer, repos_function_clone_writer, rebuild_repos)
    
    repos_log_clone_file.close()
    repos_function_clone_file.close()

def generate_xlsx_from_clone():
    """
    @ param nothing(the existence of seek clone file and cluster old new file)\n
    @ return nothing\n
    @ involve generate clone file by replace each class in seek clone file with historical revisions\n
    """
    
    workbook = xlwt.Workbook()
    spliter_index = len(my_constant.CLASS_OLD_NEW_TITLE)
    # process log clone file
    sheet = workbook.add_sheet('log_clone')
    clone_file = file(my_constant.ANALYZE_CLONE_LOG_FILE_NAME, 'rb')
    records = csv.reader(clone_file)
    current_dir = commands.getoutput('pwd')
    # sheet title
    c = 0
    for value in my_constant.CLONE_LOG_TITLE:
        sheet.write(0, c, value)
        c += 1
    # sheet content
    r = 1
    for record in islice(records, 1, None):
        class_index = record[0]
        # print 'now save class_index %s' %(class_index)
        # find historical revisions
        revisions = cluster_api.generate_records_for_class(my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, class_index)
        # write into each row
        for revision in revisions:
            c = 0
            # write into each column
            for value in revision:
                value = my_util.value_to_hyperlink(value, current_dir)
                sheet.write(r, c, value)
                c += 1
            log_record = record[spliter_index:]
            for value in log_record:
                value = my_util.value_to_hyperlink(value, current_dir)
                sheet.write(r, c, value)
                c += 1
            r += 1
    clone_file.close()

    # process function clone file
    sheet = workbook.add_sheet('function_clone')
    clone_file = file(my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, 'rb')
    records = csv.reader(clone_file)
    # sheet title
    c = 0
    for value in my_constant.CLONE_FUNCTION_TITLE:
        sheet.write(0, c, value)
        c += 1
    # sheet content
    r = 1
    for record in islice(records, 1, None):
        # print 'now save class_index %s' %(class_index)
        class_index = record[0]
        # find historical revisions
        revisions = cluster_api.generate_records_for_class(my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, class_index)
        # write into each row
        for revision in revisions:
            c = 0
            # write into each column
            for value in revision:
                value = my_util.value_to_hyperlink(value, current_dir)
                sheet.write(r, c, value)
                c += 1
            log_record = record[spliter_index:]
            for value in log_record:
                value = my_util.value_to_hyperlink(value, current_dir)
                sheet.write(r, c, value)
                c += 1
            r += 1
    clone_file.close()

    workbook.save(my_constant.CLONE_FILE_NAME)

"""
main function
"""
if __name__ == "__main__":

    # seek_clone_for_corresponding_repos(True)
    # my_util.value_to_hyperlink('data/fetch')
    # generate_clone_from_class_clone()
    # list_a = [[["!", "struct group_of_users *"]], [["strstr", "char *", "\"group \"", "char *", "=="]]]
    # list_b = [[["!", "struct user *"]], [["strstr", "char *", "\"user \"", "char *", "=="]]]
    # print compute_context_similarity(list_a, list_b, {})

#    old_file = 'second/sample/make/generate/gumtree/make_old_log_630.cpp'
#     new_file = 'second/sample/make/generate/gumtree/make_new_log_630.cpp'
#     candidate_file = 'second/gumtree/c/candidate.cpp'
#     gumtree = Gumtree()
#     print get_recommended_log_edits(gumtree, None, old_file, new_file, 'fatal (NILF, _("create_child_process: DuplicateHandle(In) failed (e=%d)\n"),GetLastError())') 
    print check_for_modify_rule([["cout"], ["cerr"]], 'consoleOut(ICE_STRING_VERSION ,endl)')