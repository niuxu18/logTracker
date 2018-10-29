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
import json
import commands
from itertools import islice
from gumtree_api import Gumtree
from srcml_api import SrcmlApi
import cluster_api
import gumtree_api
import my_constant
import my_util

reload(sys);
sys.setdefaultencoding('utf8')

def analyze_file(file_name, function_cnt, postfix, srcml):
    """
    @ param file name, function counter, postfix for store file and srcml \n
    @ return log record list and function record list \n
    @ involve traverse each function in file to build two sort of records\n
    """
    log_record_list = [] #[file, function, loc, log, check, variable]
    function_record_list = [] #[file, function, calls]
    # handle file to get and store all functions
    srcml.set_source_file(file_name)
    functions = srcml.get_functions(function_cnt, postfix)
    # traverse function to get calls and filter log info
    for function in functions:
        srcml.set_function_file(function)
        logs, calls, types = srcml.get_logs_calls_types()
        # log info
        for log in logs:
            log_record_list.append([file_name, function] + log)
        # function info
        function_record_list.append([file_name, function, json.dumps(calls), json.dumps(types)])
    return log_record_list, function_record_list


def fetch_repos_file(repos_name):
    """
    @ param repos name\n
    @ return nothing\n
    @ involve traverse repos name and collect all cpp file\n
    """
    filenames = []
    # read file from repos dir + repos name if repos name is not None
    if repos_name is not None:
        directory = my_constant.REPOS_DIR + repos_name
    else:
        print "please input a repos name"
    # traverse directory for all cpp like while not test like file
    for item in os.walk(directory):
        for filename in item[2]:
            # filter by cpp like and not test like
            if my_util.filter_file(filename):
                # concate and store file
                filename = os.path.join(item[0], filename)
                filenames.append(filename)
    return filenames

def analyze_repos(repos_name, postfix=''):
    """
    @ param repos name(not none) to analyze and postfix of repos info files\n
    @ return nothing \n
    @ involve fetch file from given repos and build two sort of records(log and call)\n
    """
    print 'input repos: %s' %(repos_name),
    # if no given repos name, create info for first or last repos
    if repos_name == my_constant.FIRST_REPOS:
        versions = commands.getoutput('ls ' + my_constant.REPOS_DIR)
        versions = versions.split('\n')
        repos_name = min(versions, key=my_util.get_version_number)
        # if is_first flag is true, then analyze first repos
    elif repos_name == my_constant.LAST_REPOS:
        versions = commands.getoutput('ls ' + my_constant.REPOS_DIR)
        versions = versions.split('\n')
        repos_name = max(versions, key=my_util.get_version_number)
    print 'analyzing repos: %s' %(repos_name)

    srcml = SrcmlApi()
    # fetch file name
    file_names = fetch_repos_file(repos_name)

    # initialize log and call analysis file
    log_file = file(my_util.concate_file(\
            my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix), 'wb')
    log_writer = csv.writer(log_file)
    log_writer.writerow(my_constant.ANALYZE_REPOS_LOG_TITLE)
    function_file = file(my_util.concate_file(\
            my_constant.ANALYZE_REPOS_FUNCTION_FILE_NAME, postfix), 'wb')
    function_writer = csv.writer(function_file)
    function_writer.writerow(my_constant.ANALYZE_REPOS_FUNCTION_TITLE)

    # analyze file in unit of function
    total_file = len(file_names)
    file_cnt = 0
    log_record_cnt = 0
    function_record_cnt = 0
    for file_name in file_names:
        file_cnt += 1
        # analyze functions in file to retieve log records and function records
        log_record_list, function_record_list = analyze_file(file_name, \
                                            function_record_cnt, postfix, srcml)
        for log_record in log_record_list:
            log_writer.writerow(log_record)
        for function_record in function_record_list:
            function_writer.writerow(function_record)
        log_record_cnt += len(log_record_list)
        function_record_cnt += len(function_record_list)
        print 'now analyzing file %d/%d, have found log record %d, function record %d' \
                            %(file_cnt, total_file, log_record_cnt, function_record_cnt)

    # close file
    log_file.close()
    function_file.close()


def cluster_repos_log(postfix=''):
    """
    @ param postfix of repos analysis,cluster and class files\n
    @ return nothing \n
    @ involve call cluster api to cluster repos log records and build class file for it\n
    """
    # intiate csv file
    analyze_repos_log_file = file(my_util.concate_file(\
            my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix), 'rb')
    records = csv.reader(analyze_repos_log_file)
    # build feature lists
    feature_lists = []
    for record in islice(records, 1, None):
        check = json.loads(record[my_constant.ANALYZE_REPOS_LOG_CHECK])
        variable = json.loads(record[my_constant.ANALYZE_REPOS_LOG_VARIABLE])
        feature_lists.append([check, variable])
    analyze_repos_log_file.close()
    # do cluster
    cluster_list = cluster_api.cluster_record_with_equality_mine(feature_lists)
    
    # sort record + cluster
    analyze_repos_log_file = file(my_util.concate_file(\
                my_constant.ANALYZE_REPOS_LOG_FILE_NAME, postfix), 'rb')
    records = csv.reader(analyze_repos_log_file)
    index = 0
    sort_records = []
    for record in islice(records, 1, None):
        sort_records.append(record + [cluster_list[index]])
        index += 1
    sort_records.sort(key=lambda x:x[-1], reverse=True)
    analyze_repos_log_file.close()

    # store back
    cluster_repos_log_file = file(my_util.concate_file(\
                my_constant.CLUSTER_REPOS_LOG_FILE_NAME, postfix), 'wb')
    writer = csv.writer(cluster_repos_log_file)
    writer.writerow(my_constant.CLUSTER_REPOS_LOG_TITLE)
    for record in islice(sort_records, 1, None):
        writer.writerow(record)
    # close file
    cluster_repos_log_file.close()

    # build class from cluster(min frequence is 1)
    cluster_api.generate_class_from_cluster(my_util.concate_file(\
                    my_constant.CLUSTER_REPOS_LOG_FILE_NAME, postfix),\
                    my_util.concate_file(my_constant.CLASS_REPOS_LOG_FILE_NAME, postfix),\
                    my_constant.CLUSTER_REPOS_LOG_TITLE, my_constant.CLASS_REPOS_LOG_TITLE, 1)

"""
main function
"""
if __name__ == "__main__":
    # curl
    # repos_name = "curl-7.41.0"
    # mutt
    # analyze_repos("mutt-1.7.2")
    # rsync
    # repos_name = "rsync-1.4.4"
    # git
    # analyze_repos('git-2.6.7')
    # httpd
    # analyze_repos('httpd-2.3.8')
    # cluster_repos_log()
    # cluster_repos_log()
    # repos_name = 'collectd-4.10.7'
    # analyze_repos(repos_name, '_' + repos_name)
    analyze_repos(my_constant.LAST_REPOS, '_last_repos_if_switch')    
    cluster_repos_log('_last_repos_if_switch')
