from itertools import islice 
import srcml_api
import cluster_api
import csv
import json
import my_constant
import my_util

def statistical_cluster_cross_feature():
    """
    @ param nothing\n
    @ return class counter, cross file counter, cross function counter and cross version counter\n
    @ involve count the number of cross file and cross function and cross version\n
    """
    reading_file = file(my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME)
    records = csv.reader(reading_file)

    cluster_counter = 0
    cross_file_counter = 0
    file_name = None
    cross_function_counter = 0
    function_name = None
    cross_version_counter = 0
    version_info = None
    # check each class
    for record in islice(records, 1, None):
        cluster_counter += 1
        log_revisions = cluster_api.generate_records_for_class(my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, record[0])
        # record the one that crosses files
        file_name = log_revisions[0][my_constant.FETCH_LOG_OLD_FILE]
        for log_revision in islice(log_revisions, 1, None):
            # quit if find different files
            if log_revision[my_constant.FETCH_LOG_OLD_FILE] != file_name:
                cross_file_counter += 1
                break
        # record the one that crosses functions
        function_name = ''
        if log_revisions[0][my_constant.FETCH_LOG_OLD_LOC] != '-1': # has old -> old
            function_name = log_revisions[0][my_constant.ANALYZE_OLD_FUNCTION]
        else:
            function_name = log_revisions[0][my_constant.ANALYZE_NEW_FUNCTION]
        for log_revision in islice(log_revisions, 1, None):
            curr_function_name = ''
            if log_revision[my_constant.FETCH_LOG_OLD_LOC] != '-1': # has old -> old
                curr_function_name = log_revision[my_constant.ANALYZE_OLD_FUNCTION]
            else:
                curr_function_name = log_revision[my_constant.ANALYZE_NEW_FUNCTION]

            # quit if find different files
            if my_util.is_same_file(function_name, curr_function_name):
                cross_function_counter += 1
                break
        version_info = log_revisions[0][0]
        for log_revision in islice(log_revisions, 1, None):
            # quit if find different files
            if log_revision[0] != version_info:
                cross_version_counter += 1
                break
    reading_file.close()

    return cluster_counter, cross_file_counter, cross_function_counter, cross_version_counter

def statistical_cluster(csv_file_name, statistic_file, edit_type_dict=None):
    """
    @ param csv file name and statistical file to write and dictory of edit types\n
    @ return statistical info about log records(number of instance, edit type frequence)\n
    @ involve get statistical info about cluster as well as all records\n
    """
    reading_file = file(csv_file_name)
    records = csv.reader(reading_file)
    # define and initialize edit type dictary type -> number of instances
    edit_type_for_log_dict = {}
    edit_type_for_cluster_dict = {}
    for i in my_constant.LOG_EDIT_TYPES:
        edit_type_for_log_dict[i] = 0
        edit_type_for_cluster_dict[i] = 0
    # define and initialize log edit dict
    log_edit_dict = {}
    # cluster dictary: cluster index -> cluster size
    cluster_dict = {}
    number_log = 0
    number_cluster = 0
    repeted_cluster = 0
    repeted_log = 0
    for record in islice(records, 1, None):
        number_log += 1
        # record number of instance for each edit type
        edit_types = json.loads(record[my_constant.ANALYZE_EDIT_TYPE])
        for edit_type in edit_types:
            edit_type_for_log_dict[edit_type] += 1
        # filter by edit feature != 0 (cluster of empty edit is unsure)
        edit_feature = json.loads(record[my_constant.ANALYZE_EDIT_FEATURE])
        if edit_feature == [0]:
            continue
        cluster = json.loads(record[my_constant.ANALYZE_CLUSTER])
        # record number of cluster for each cluster index
        # if has been in dict -> repeted log and cluster size
        if cluster_dict.has_key(cluster):
            # current edit type info
            for edit_type in edit_types:
                edit_type_for_cluster_dict[edit_type] += 1
            # first repetetion -> repeted cluster and repeted log(historical one)
            if len(cluster_dict[cluster]) == 1:
                # historical edit type info
                edit_types = log_edit_dict[cluster_dict[cluster][0]]
                for edit_type in edit_types:
                    edit_type_for_cluster_dict[edit_type] += 1
                # edit type dictory for all rules
                if edit_type_dict is not None:
                    for edit_type in edit_types:
                        edit_type_dict[edit_type] += 1
                repeted_cluster += 1
                repeted_log += 1
            # if have repetion, increment value(mark)
            cluster_dict[cluster].append(number_log)
            # repeted log
            repeted_log += 1
        # new cluster -> cluster count and cluster size
        else:
            # record log edit info for each log
            log_edit_dict[number_log] = edit_types
            cluster_dict[cluster] = [number_log]
            number_cluster += 1

    # show edition type result
    for edit_type in my_constant.LOG_EDIT_TYPES:
        print >> statistic_file, "%s:%d," %(edit_type, edit_type_for_cluster_dict[edit_type]),
    print >> statistic_file, ''
    # show cluster result
    print >> statistic_file, "cluster is:%d, repeted cluster is:%d, repeted log is:%d" %(number_cluster, repeted_cluster, repeted_log)

    reading_file.close()

    return number_log, edit_type_for_log_dict, edit_type_dict

def statistical_rule_class(csv_file_name):
    """
    @ param csv file name\n
    @ return number of insert rule and number of modify rule\n
    @ involve count two sort of rules and statistic its edit type\n
    """
    reading_file = file(csv_file_name)
    records = csv.reader(reading_file)
    modify_counter = 0
    insert_counter = 0
    for record in islice(records, 1, None):
        old_loc = record[my_constant.CLASS_OLD_NEW_OLD_LOC]
        if old_loc == '-1':
            insert_counter += 1
        else:
            modify_counter += 1
    reading_file.close()
    return insert_counter, modify_counter

def statistical_verify_log():
    """
    @ param nothing\n
    @ return nothing\n
    @ involve pre-verify historical modifications by function_loc and log content\n
    """
    rule_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_rule'), 'rb')
    rule_file_verified = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_LOG_FILE_NAME, '_rule_verified'), 'wb')
    writer = csv.writer(rule_file_verified)
    writer.writerow(my_constant.ANALYZE_CLONE_LOG_TITLE)
    records = csv.reader(rule_file)
    cluster_id = None
    for record in islice(records, 1, None):
        # find new cluster
        if record[0] != cluster_id:        
            cluster_id = record[0]
            # find history loc and log info
            history_info = {}
            history_records = cluster_api.generate_records_for_class\
                        (my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, cluster_id)
            for history_record in history_records:
                history_loc = -1
                if history_record[my_constant.FETCH_LOG_OLD_LOC] != '-1': # has old -> old
                    history_loc = int(history_record[my_constant.ANALYZE_OLD_FUNCTION_LOC])
                else:
                    history_loc = int(history_record[my_constant.ANALYZE_NEW_FUNCTION_LOC])
                history_log = history_record[my_constant.FETCH_LOG_OLD_LOG]
                history_info[history_loc] = history_log[:-1]
        candidate_loc = record[my_constant.ANALYZE_CLONE_LOG_FUNCTION_LOC]
        candidate_log = record[my_constant.ANALYZE_CLONE_LOG_FUNCTION_LOG]
        # pre-verify correctness of candidates and marked
        if history_info.has_key(candidate_loc) and history_info[candidate_loc] == candidate_log:
            record[-1] = 'accept-true-verified'
        writer.writerow(record)

    rule_file.close()
    rule_file_verified.close()

def statistical_verify_function():
    """
    @ param nothing\n
    @ return nothing\n
    @ involve pre-verify historical modifications by hunk < function\n
    """
    rule_file = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, '_rule'), 'rb')
    rule_file_verified = file(my_util.concate_file(\
                my_constant.ANALYZE_CLONE_FUNCTION_FILE_NAME, '_rule_verified'), 'wb')
    writer = csv.writer(rule_file_verified)
    writer.writerow(my_constant.ANALYZE_CLONE_FUNCTION_TITLE)
    records = csv.reader(rule_file)
    cluster_id = None
    for record in islice(records, 1, None):
        # do not verify that already have logs
        if record[-1] == 'accept-false-check' or record[-1] == 'accept-false-variable':
            writer.writerow(record)
            continue
        # find new cluster
        if record[0] != cluster_id:        
            cluster_id = record[0]
            # find history hunk + function
            history_info = []
            history_records = cluster_api.generate_records_for_class\
                        (my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, cluster_id)
            for history_record in history_records:
                old_hunk_set = my_util.read_file_content_to_set(history_record[my_constant.FETCH_LOG_OLD_HUNK_FILE])
                history_info.append(old_hunk_set)
        candidate_function_set = my_util.read_file_content_to_set(record[my_constant.ANALYZE_CLONE_FUNCTION_FUNCTION])
        # pre-verify correctness of candidates and marked
        for history_function in history_info:
            if candidate_function_set.issuperset(history_function):
                record[-1] = 'accept-true-verified'
        writer.writerow(record)
    rule_file.close()
    rule_file_verified.close()

def statistical_verify_history():
    """
    @ param nothing\n
    @ return nothing\n
    @ involve pre-verify historical modifications for log and function seperately\n
    """
    statistical_verify_log()
    statistical_verify_function()
    statistical_repos_call_log_times()

def statistical_repos_call_log_times(postfix=my_constant.LAST_REPOS):
    """
    @ param postfix of csv file name\n
    @ return nothing(writing out the log times for each function call)\n
    @ involve summarize times of function call and times of being logged retuer value\n
    """
    # read file initialization
    call_file = file(my_util.concate_file(my_constant.ANALYZE_REPOS_FUNCTION_FILE_NAME, postfix), 'rb')
    log_file = file(my_util.concate_file(my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix), 'rb')
    call_records = csv.reader(call_file)
    log_records = csv.reader(log_file)
    call_log_times_dict = {}
    # record call times
    for call_record in islice(call_records, 1, None):
        calls = json.loads(call_record[my_constant.ANALYZE_REPOS_FUNCTION_CALLS])
        for call in calls:
            if call_log_times_dict.has_key(call):
                call_log_times_dict[call][0] += 1
            else:
                call_log_times_dict[call] = [1, 0]
    call_file.close()
    # record log times
    for log_record in islice(log_records, 1, None):
        checks = json.loads(log_record[my_constant.ANALYZE_REPOS_LOG_CHECK])
        for check in checks:
            if check is not None and check.endswith(my_constant.FlAG_FUNC_RETURN) and \
                    not check.endswith(my_constant.FlAG_FUNC_ARG_RETURN):
                call = check[:-1*len(my_constant.FlAG_FUNC_RETURN)]
                if call_log_times_dict.has_key(call):
                    call_log_times_dict[call][1] += 1
                else:
                    print 'weird phenomenon: %s, %s logged but never called' %(call, check)
                    call_log_times_dict[call] = [0, 1]
    log_file.close()
    # flush result out

    # write file initialization
    statistic_file = file(my_constant.CALL_LOG_TIMES_FILE_NAME, 'wb')
    writer = csv.writer(statistic_file)
    writer.writerow(my_constant.CALL_LOG_TIMES_TITLE)
    for (key, value) in call_log_times_dict.items():
        writer.writerow([key] + value)
    statistic_file.close()

def statistical_repos_log(postfix=my_constant.LAST_REPOS, statistic_file_name = 'data/evaluate/lloc.txt'):
    """
    @ param postfix of csv file name, statistical file name\n
    @ return nothing(print out the line of logging codes)\n
    @ involve sumarize logging LOC in given repos decided by postfix\n
    """
    statistic_file = open(statistic_file_name, 'ab')
    csv_file = file(my_util.concate_file(my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix), 'rb')
    records = csv.reader(csv_file)
    srcml = srcml_api.SrcmlApi()
    log_loc = 0
    counter = 0
    for record in islice(records, 1, None):
        counter += 1
        print 'now analyzing record: %d' %counter
        call_node_loc = int(record[my_constant.ANALYZE_REPOS_LOG_LOC])
        function_file = record[my_constant.ANALYZE_REPOS_LOG_FUNCTION]
        srcml.set_function_file(function_file)
        srcml.set_log_loc(call_node_loc)
        log_loc += len(srcml.get_log_loc(call_node_loc))
    print >> statistic_file, "\n# repos %s: %d" %(my_constant.REPOS, log_loc)
    csv_file.close()
    statistic_file.close()


def perform_statistic(edit_type_dict, statistic_file_name = 'data/evaluate/statistics.txt'):
    """
    @ param dictory of edit types, statistic file name\n
    @ return dictory of edit type\n
    @ involve get statistical info about cluster and log,
            edit type info and cluster info (no.cluster, no.>1cluster, no.repeted log)\n 
    """
    statistic_file = open(statistic_file_name, 'ab')
    print >> statistic_file, "\n#now analyzing repos:%s" %(my_constant.REPOS)
    # statistics about edition cluster
    print >> statistic_file, "#edition cluster info"
    edition_file_name = my_constant.CLUSTER_EDITION_OLD_NEW_FILE_NAME
    statistical_cluster(edition_file_name, statistic_file)
    print >> statistic_file, "#feature cluster info"
    # statistics about feature cluster
    feature_file_name = my_constant.CLUSTER_FEATURE_OLD_NEW_FILE_NAME
    statistical_cluster(feature_file_name, statistic_file)
    # print >> statistic_file, "#feature and edition cluster without content info"
    # # statistics about feature and edition without content modification cluster
    # feature_edition_without_content_file_name = my_constant.CLUSTER_EDITION_AND_FEATURE_WITHOUT_CONTENT_OLD_NEW_FILE_NAME
    # statistical_cluster(feature_edition_without_content_file_name, statistic_file)
    print >> statistic_file, "#edition and feature cluster info"
    # statistics about edition and feature cluster
    edition_and_feature_file_name = my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME
    number_log, edit_type_for_log_dict, edit_type_dict = statistical_cluster(edition_and_feature_file_name, statistic_file, edit_type_dict)
    print >> statistic_file, "#log info"
    print >> statistic_file, "number of log is:%d"  %number_log
    # show edition type result
    for edit_type in my_constant.LOG_EDIT_TYPES:
        print >> statistic_file, "%s:%d," %(edit_type, edit_type_for_log_dict[edit_type]),
    print >> statistic_file, ''
    # statistics about rule class
    insert_counter, modify_counter = statistical_rule_class(my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME)
    print >> statistic_file, '#rule info'
    print >> statistic_file, 'insert rule:%d, modify rule:%d' %(insert_counter, modify_counter)
    statistic_file.close()

    return edit_type_dict

"""
main function
"""
if __name__ == "__main__":
    perform_statistic(None)   

    # reposes = ['httpd', 'git', 'mutt', 'rsync', 'collectd', 'postfix', 'tar', 'wget']
    # cluster_counter = 0
    # cross_file_counter = 0
    # cross_function_counter = 0
    # cross_version_counter = 0
    # for repos in reposes:
    #     my_constant.reset_repos(repos)
    #     print '\n****************now analyzing repos %s***************' %repos
    #     cluster, cross_file, cross_function, cross_version = statistical_cluster_cross_feature()
    #     print 'cluster: %d, cross file: %d, cross function: %d, cross version: %d' %(cluster, cross_file, cross_function, cross_version)
    #     cluster_counter += cluster
    #     cross_file_counter += cross_file
    #     cross_function_counter += cross_function
    #     cross_version_counter += cross_version
    
    # print 'cluster: %d, cross file: %d, cross function: %d, cross version: %d' %(cluster_counter, cross_file_counter, cross_function_counter, cross_version_counter)