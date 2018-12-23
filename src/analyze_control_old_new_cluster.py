#-*-coding: utf-8 -*-
import csv
import xlwt
import sys
import re
import commands
import json
from itertools import islice
from gumtree_api import Gumtree
import cluster_api
import my_util
import my_constant
import gumtree_api

reload(sys)
sys.setdefaultencoding('utf-8')

def cluster_feature():
    """
    @ param nothing\n
    @ return nothing\n
    @ involve cluster by feature(check and variable)\n
    """
    # initialize read file
    read_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'rb')
    records = csv.reader(read_file)

    feature_lists = []
    # build feature list
    index = 0
    for record in islice(records, 1, None):  # remove the table title
        if int(record[my_constant.FETCH_LOG_ACTION_TYPE]) %2 == 0:
            continue
        check_feature = json.loads(record[my_constant.ANALYZE_CHECK]) 
        variable_feature = json.loads(record[my_constant.ANALYZE_VARIABLE])
        
        feature_lists.append([check_feature, variable_feature])
    read_file.close()

    # cluster with feature list and write back to given file
    write_file = file(my_constant.CLUSTER_FEATURE_OLD_NEW_FILE_NAME, 'wb')
    write_file_writer = csv.writer(write_file)
    write_file_writer.writerow(my_constant.CLUSTER_OLD_NEW_TITLE)

    _cluster_with_feature_list(feature_lists, write_file_writer)
    
    write_file.close()

def cluster_edition():
    """
    @ param nothing\n
    @ return nothing\n
    @ involve cluster by edition\n
    """
    # initialize read file
    read_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'rb')
    records = csv.reader(read_file)

    feature_lists = []
    # build feature list
    for record in islice(records, 1, None):  # remove the table title
        if int(record[my_constant.FETCH_LOG_ACTION_TYPE]) %2 == 0:
            continue
        # old cdg feature
        edit_feature = json.loads(record[my_constant.ANALYZE_EDIT_FEATURE])
        feature_lists.append(edit_feature)
    read_file.close()

    # cluster with feature list and write back to given file
    write_file = file(my_constant.CLUSTER_EDITION_OLD_NEW_FILE_NAME, 'wb')
    write_file_writer = csv.writer(write_file)
    write_file_writer.writerow(my_constant.CLUSTER_OLD_NEW_TITLE)

    _cluster_with_feature_list(feature_lists, write_file_writer)
    
    write_file.close()

def cluster_edition_and_feature_without_coontent():
    """
    @ param z3 api\n
    @ return nothing\n
    @ involve cluster by edition and feature(do not cluster content modification)\n
    """
    # initialize read file
    read_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'rb')
    records = csv.reader(read_file)

    feature_lists = []
    # build feature list
    index = 0
    for record in islice(records, 1, None):  # remove the table title
        if int(record[my_constant.FETCH_LOG_ACTION_TYPE]) %2 == 0:
            continue
        # context feature
        check_feature = json.loads(record[my_constant.ANALYZE_CHECK])
        variable_feature = json.loads(record[my_constant.ANALYZE_VARIABLE])
       
        # edit feature
        edit_types = json.loads(record[my_constant.ANALYZE_EDIT_TYPE])
        edit_feature = gumtree_api.get_edit_feature_from_edit_types(edit_types)
        feature_lists.append([check_feature, variable_feature, edit_feature])
    read_file.close()

    # cluster with feature list and write back to given file
    write_file = file(my_constant.CLUSTER_EDITION_AND_FEATURE_WITHOUT_CONTENT_OLD_NEW_FILE_NAME, 'wb')
    write_file_writer = csv.writer(write_file)
    write_file_writer.writerow(my_constant.CLUSTER_OLD_NEW_TITLE)

    _cluster_with_feature_list(feature_lists, write_file_writer)
    
    write_file.close()

def cluster_edition_and_feature():
    """
    @ param z3 api\n
    @ return nothing\n
    @ involve cluster by edition and feature\n
    """
    # initialize read file
    read_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'rb')
    records = csv.reader(read_file)

    feature_lists = []
    # build feature list
    index = 0
    for record in islice(records, 1, None):  # remove the table title
        if int(record[my_constant.FETCH_LOG_ACTION_TYPE]) %2 == 0:
            continue
        # context feature
        check_feature = json.loads(record[my_constant.ANALYZE_CHECK])
        variable_feature = json.loads(record[my_constant.ANALYZE_VARIABLE])
        
        # edit feature
        edit_feature = json.loads(record[my_constant.ANALYZE_EDIT_FEATURE])
        feature_lists.append([check_feature, variable_feature, edit_feature])
    read_file.close()

    # cluster with feature list and write back to given file
    write_file = file(my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, 'wb')
    write_file_writer = csv.writer(write_file)
    write_file_writer.writerow(my_constant.CLUSTER_OLD_NEW_TITLE)

    _cluster_with_feature_list(feature_lists, write_file_writer)
    
    write_file.close()

def _cluster_with_feature_list(feature_list, file_writer):
    """
    @ param feature list\n
    @ return nothing\n
    @ involve cluster with given feature lists\n
    """
    # cluster log statement based on feature list
    cluster_lists = cluster_api.cluster_record_with_equality_mine(feature_list)

    # sort cluster by index -> the largest index at the top
    read_file = file(my_constant.ANALYZE_OLD_NEW_LLVM_FILE_NAME, 'rb')
    records = csv.reader(read_file)
    sort_records = []
    index = 0
    for record in islice(records, 1, None):
        if int(record[my_constant.FETCH_LOG_ACTION_TYPE]) %2 == 0:
            continue
        record = record + [cluster_lists[index]]
        sort_records.append(record)
        index += 1
    read_file.close()
    sort_records.sort(key=lambda x:x[-1], reverse=True)
    
    # write back to file
    for record in sort_records:
        file_writer.writerow(record)

def cluster():
    """
    @ param z3 api\n
    @ return nothing\n
    @ involve cluster by feature and edition/ edition/ feature\n
    """
    cluster_edition_and_feature()
    # cluster_edition_and_feature_without_coontent()
    cluster_edition()
    cluster_feature()

def generate_xlsx_from_csv_cluster():
    """
    @ param nothing(the existence of cluster file\n
    @ return nothing\n
    @ involve generate xlsx file by replace each file with hyperlink in cluster file\n
    """
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('edition_and_feature_cluster')

    my_util.csv_to_xlsx(my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, sheet)
    workbook.save(my_constant.CLUSTER_FILE_NAME)

def generate_xlsx_from_csv_class(sheet):
    """
    @ param sheet\n
    @ return nothing\n
    @ involve generate xlsx file by replace each file with hyperlink in class file\n
    """
    my_util.csv_to_xlsx(my_util.concate_file(my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME, '_trivial'), sheet)



def generate_class(cluster_file_name=None, \
                   class_file_name=None, cluster_title=None, class_title=None): 
    """
    @ param nothing\n
    @ return nothing\n
    @ involve generate class for edition and feature cluster\n
    """
    if cluster_file_name is None:
        cluster_file_name = my_constant.CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME
    if class_file_name is None:
        class_file_name = my_constant.CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME
    if cluster_title is None:
        cluster_title = my_constant.CLUSTER_OLD_NEW_TITLE
    if class_title is None:
        class_title = my_constant.CLASS_OLD_NEW_TITLE
    cluster_api.generate_class_from_cluster(cluster_file_name,\
        class_file_name, cluster_title, class_title)

"""
main function
"""
if __name__ == "__main__":

    # cluster(None)
    # generate_class()

    reposes = ['httpd', 'git', 'mutt', 'rsync', 'collectd', 'postfix', 'tar', 'wget']
    workbook = xlwt.Workbook()
    for repos in reposes:
        my_constant.reset_repos_series(repos)
        sheet = workbook.add_sheet(my_constant.REPOS)
        print 'now analyzing repos %s' %(repos)
        generate_xlsx_from_csv_class(sheet)
    workbook.save(my_constant.RULES_DIR + 'analyze_trivial.xlsx')