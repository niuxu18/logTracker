import random
import csv
import json
from itertools import islice
import my_constant
import cluster_api
import analyze_control_old_new_cluster
import analyze_control_clone
import my_util
import srcml_api

import gumtree_api

def generate_data(statistic_file, train_data_rate=0.6):
    """
    @ param proportion of train data\n
    @ return nothing \n
    @ involve use random to generate test data and train data and use train data to get rule\n
    """
    # initialize read file
    read_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'rb')
    records = csv.reader(read_file)

    #test and train file name
    test_file_name = my_util.concate_file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, '_test')
    test_file = file(test_file_name, 'wb')
    test_file_writer = csv.writer(test_file)
    test_file_writer.writerow(my_constant.ANALYZE_OLD_NEW_LLVM_TITLE)
    train_file_name = my_util.concate_file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, '_train')
    train_file = file(train_file_name, 'wb')
    train_file_writer = csv.writer(train_file)
    train_file_writer.writerow(my_constant.ANALYZE_OLD_NEW_LLVM_TITLE)

    feature_lists = []
    # build feature list
    test_index = 0
    train_index = 0
    for record in islice(records, 1, None):  # remove the table title
        if int(record[my_constant.FETCH_LOG_ACTION_TYPE]) %2 == 0:
            continue
        # use random() and train data rate to decide whether to be a train data
        if random.random() >= train_data_rate:
            test_file_writer.writerow(record)
            test_index += 1
            continue
        # context feature
        train_file_writer.writerow(record)
        train_index += 1
        check_feature = json.loads(record[my_constant.ANALYZE_CHECK])
        variable_feature = json.loads(record[my_constant.ANALYZE_VARIABLE])
        # edit feature
        edit_feature = json.loads(record[my_constant.ANALYZE_EDIT_FEATURE])
        # edit_types = json.loads(record[my_constant.ANALYZE_EDIT_TYPE])
        # edit_feature = gumtree_api.get_edit_feature_from_edit_types(edit_types)
        feature_lists.append([check_feature, variable_feature, edit_feature])
    read_file.close()
    test_file.close()
    train_file.close()
    print >> statistic_file, 'train record: %s, test record: %s' %(train_index, test_index)

    # cluster log statement based on cdg_list and ddg_list
    cluster_lists = cluster_api.cluster_record_with_equality_mine(feature_lists)
    # record cluster index of each log statement
    read_file = file(train_file_name, 'rb') 

    # sort cluster by index -> the largest index at the top
    records = csv.reader(read_file)
    sort_records = []
    index = 0
    for record in islice(records, 1, None):
        record = record + [cluster_lists[index]]
        sort_records.append(record)
        index += 1
    read_file.close()
    sort_records.sort(key=lambda x:x[-1], reverse=True)

    # write back to file
    train_cluster_file_name = my_util.concate_file(my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, '_train')
    write_file = file(train_cluster_file_name, 'wb')
    write_file_writer = csv.writer(write_file)
    write_file_writer.writerow(my_constant.CLUSTER_OLD_NEW_TITLE)
    for record in sort_records:
        write_file_writer.writerow(record)
    write_file.close()

def validate_log_candidates(statistic_file):
    """
    @ param \n
    @ return nothing \n
    @ involve compare test data set with generated log rules\n
    """
    rule_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_train'), 'rb')
    rule_file_verified = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_verified_train'), 'wb')
    writer = csv.writer(rule_file_verified)
    writer.writerow(my_constant.ANALYZE_CLONE_LOG_TITLE)
    records = csv.reader(rule_file)

    history_info = []
    test_file_name = my_util.concate_file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, '_test')
    test_file = file(test_file_name, 'rb')
    test_records = csv.reader(test_file)
    test_log = 0
    for test_record in islice(test_records, 1, None):
        # just verify modification of logs
        if test_record[my_constant.FETCH_LOG_OLD_LOC] == '-1':
            continue
        test_log += 1
        history_loc = '-1'
        if test_record[my_constant.FETCH_LOG_OLD_LOC] != '-1': # has old -> old
            history_loc = test_record[my_constant.ANALYZE_OLD_FUNCTION_LOC]
        else:
            history_loc = test_record[my_constant.ANALYZE_NEW_FUNCTION_LOC]
        history_log = test_record[my_constant.FETCH_LOG_OLD_LOG]
        history_info.append([history_loc, history_log])

    train_info = {}
    train_file_name = my_util.concate_file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, '_train')
    train_file = file(train_file_name, 'rb')
    train_records = csv.reader(train_file)
    for train_record in islice(train_records, 1, None):
        # just verify insertion of logs
        if train_record[my_constant.FETCH_LOG_OLD_LOC] == '-1':
            continue
        train_loc = '-1'
        if train_record[my_constant.FETCH_LOG_OLD_LOC] != '-1': # has old -> old
            train_loc = train_record[my_constant.ANALYZE_OLD_FUNCTION_LOC]
        else:
            train_loc = train_record[my_constant.ANALYZE_NEW_FUNCTION_LOC]
        train_log = train_record[my_constant.FETCH_LOG_OLD_LOG]
        train_info[train_loc] = train_log[:-1]

    validate_log = 0
    validate_test = 0
    total_log = 0
    test_found_dict = {}
    for record in islice(records, 1, None):
        if record[-1] == 'accept-false':
            continue
        # find history loc and log info
        candidate_loc = record[my_constant.ANALYZE_CLONE_LOG_FUNCTION_LOC]
        candidate_log = record[my_constant.ANALYZE_CLONE_LOG_FUNCTION_LOG]
        # pre-verify correctness of candidates and marked
        for i in range(test_log):
            if history_info[i][0] == candidate_loc and history_info[i][1].find(candidate_log) == -1:
                if not test_found_dict.has_key(i):
                    validate_test += 1
                    test_found_dict[i] = 1
                record[-1] = 'accept-true-verified'
                validate_log += 1
                break
        # do not deal with train log
        if not train_info.has_key(candidate_loc) or train_info[candidate_loc].find(candidate_log) == -1:
            total_log += 1
        writer.writerow(record)
    print >> statistic_file, 'mod test record: %d, mod validate test: %d, mod total record: %d, mod validate record: %d' %(test_log, validate_test, total_log, validate_log)

    test_file.close()
    train_file.close()
    rule_file.close()
    rule_file_verified.close()

def validate_function_candidates(statistic_file):
    """
    @ param \n
    @ return nothing \n
    @ involve compare test data set with generated function rules\n
    """
    rule_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, '_train'), 'rb')
    rule_file_verified = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, '_verified_train'), 'wb')
    writer = csv.writer(rule_file_verified)
    writer.writerow(my_constant.ANALYZE_CLONE_LOG_TITLE)
    records = csv.reader(rule_file)

    history_info = []
    test_file_name = my_util.concate_file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, '_test')
    test_file = file(test_file_name, 'rb')
    test_records = csv.reader(test_file)
    test_log = 0
    for test_record in islice(test_records, 1, None):
        # just verify insertion of logs
        if test_record[my_constant.FETCH_LOG_OLD_LOC] != '-1':
            continue
        test_log += 1
        old_hunk_set = my_util.read_file_content_to_set(test_record[my_constant.FETCH_LOG_OLD_HUNK_FILE])
        history_info.append(old_hunk_set)

    train_info = []
    train_file_name = my_util.concate_file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, '_train')
    train_file = file(train_file_name, 'rb')
    train_records = csv.reader(train_file)
    for train_record in islice(train_records, 1, None):
        # just verify insertion of logs
        if train_record[my_constant.FETCH_LOG_OLD_LOC] != '-1':
            continue
        old_hunk_set = my_util.read_file_content_to_set(train_record[my_constant.FETCH_LOG_OLD_HUNK_FILE])
        train_info.append(old_hunk_set)

    validate_log = 0
    validate_test = 0
    test_found_dict = {}
    total_log = 0
    for record in islice(records, 1, None):
        if record[-1] == 'accept-false-check' or record[-1] == 'accept-false-variable':
            continue
        candidate_function_set = my_util.read_file_content_to_set(record[my_constant.ANALYZE_CLONE_FUNCTION_FUNCTION])

        # pre-verify correctness of candidates and marked
        for i in range(test_log):
            history_function = history_info[i]
            if candidate_function_set.issuperset(history_function):
                # do not count repetitive data
                if not test_found_dict.has_key(i):
                    validate_test += 1
                    test_found_dict[i] = 1
                record[-1] = 'accept-true-verified'
                validate_log += 1
                break
        # do not count train data
        for train_function in train_info:
            if not candidate_function_set.issuperset(train_function):
                total_log += 1
        writer.writerow(record)
    print >> statistic_file, 'insert test record: %d, insert validate test: %d, insert total record: %d, insert validate record: %d' %(test_log, validate_test, total_log, validate_log)

    test_file.close()
    train_file.close()
    rule_file.close()
    rule_file_verified.close()

def test(is_rebuild_data=True, train_ratio=0.5):
    """
    @ param \n
    @ return nothing \n
    @ involve train rule, apply trained rules to all history repos and validate\n
    """
    statistic_file = open('data/evaluate/train_test_2.txt', 'ab')
    print >> statistic_file, "------- %s ----------" %(my_constant.REPOS)
    if is_rebuild_data:
        # split data set and train rule
        generate_data(statistic_file, train_ratio)
        # generate class from cluster
        train_cluster_file_name = my_util.concate_file(my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, '_train')
        train_class_file_name = my_util.concate_file(my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, '_train')
        analyze_control_old_new_cluster.generate_class(train_cluster_file_name, train_class_file_name)
        # apply rules to correpsonding repos
        analyze_control_clone.seek_clone_for_history_repos_train(False)
    # validate
    validate_log_candidates(statistic_file)
    validate_function_candidates(statistic_file)
    statistic_file.close()

def generate_recommended_edit():
    """
    @ param \n
    @ return nothing \n
    @ involve regenerate edit script based on the old log, new log and candidate log\n
    """
    rule_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_verified_train'), 'rb')
    rule_file_verified = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_verify_train'), 'wb')
    writer = csv.writer(rule_file_verified)
    writer.writerow(my_constant.ANALYZE_CLONE_LOG_TITLE)
    records = csv.reader(rule_file)

    gumtree = gumtree_api.Gumtree()
    index = 0
    for record in islice(records, 1, None):
        old_log_file = "temp_old_log_file.cpp"
        my_util.save_file(record[my_constant.CLASS_OLD_NEW_OLD_LOG], old_log_file)
        new_log_file = "temp_new_log_file.cpp"
        my_util.save_file(record[my_constant.CLASS_OLD_NEW_NEW_LOG], new_log_file)
        srcml = None
        if record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC] != '-1':
            srcml = srcml_api.SrcmlApi()
            srcml.set_function_file(record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION])
            if not srcml.set_log_loc(int(record[my_constant.CLASS_OLD_NEW_NEW_FUNCTION_LOC])):
                srcml = None 
        if index % 10 == 0:
            print index
        index += 1
        record[-2] = analyze_control_clone.get_recommended_log_edits(gumtree, srcml, old_log_file, new_log_file, record[my_constant.ANALYZE_CLONE_LOG_FUNCTION_LOG])
        writer.writerow(record)

    rule_file.close()
    rule_file_verified.close()

if __name__ == "__main__":
    # 'httpd', 'git',
    reposes = ['httpd', 'git', 'collectd', 'postfix', 'mutt', 'rsync', 'tar', 'wget']
    train_ratios = [0.5, 0.8]
    # for repos in reposes[0:4]:
    for repos in reposes[1:4]:
        my_constant.reset_repos_series(repos)
        generate_recommended_edit()
    gumtree_api.close_jvm()
    #     my_constant.reset_repos_series(repos)
    #     for train_ratio in train_ratios:
    #         for i in range(5):
    #             test(True, train_ratio)

