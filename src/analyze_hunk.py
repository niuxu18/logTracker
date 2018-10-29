#-*-coding: utf-8 -*-
"""
input: hunk info
BY: gumtree
output: log info
log info [hunk info, log type, old log statement, new log statement, log action]
"""
import csv
import sys
import json
from itertools import islice
from gumtree_api import Gumtree
import gumtree_api
import my_constant
import my_util

reload(sys)
sys.setdefaultencoding('utf-8')

def deal_hunk( hunk_record, log_writer, gumtree, total_log):
    """
    @ param hunk record, log writer, gumtree object and log counter\n
    @ return new log counter\n
    @ involve deal with each hunk and retieve log info\n
    """
    # old and new log loc and hunk loc
    old_log_loc = json.loads(hunk_record[my_constant.FETCH_HUNK_OLD_LOG_LOC])
    new_log_loc = json.loads(hunk_record[my_constant.FETCH_HUNK_NEW_LOG_LOC])
    if(len(old_log_loc) > my_constant.MAX_LOG_IN_HUNK or len(new_log_loc) > my_constant.MAX_LOG_IN_HUNK):
        print 'too many logs (old: %d, new: %d) in one hunk %s' %(len(old_log_loc), len(new_log_loc), hunk_record[my_constant.FETCH_HUNK_OLD_HUNK_FILE])
        return total_log

    old_hunk_loc = int(hunk_record[my_constant.FETCH_HUNK_OLD_HUNK_LOC])
    new_hunk_loc = int(hunk_record[my_constant.FETCH_HUNK_NEW_HUNK_LOC])
    old_hunk_file = hunk_record[my_constant.FETCH_HUNK_OLD_HUNK_FILE]
    new_hunk_file = hunk_record[my_constant.FETCH_HUNK_NEW_HUNK_FILE]
    # gumtree deal with old and new hunk file
    hunk_info = hunk_record[:-4]
    gumtree.set_old_new_file(old_hunk_file, new_hunk_file)
    gumtree.add_old_log_nodes(old_log_loc)
    gumtree.add_new_log_nodes(new_log_loc)
    # get hunk action type
    action_type = gumtree.get_hunk_edited_type()

    # deal with log existing in old file
    for old_loc in old_log_loc:
        if gumtree.set_old_loc(old_loc):
            # get log loc in old hunk, old loc and old log
            old_hunk_log_loc = old_loc # index from 0
            old_loc = old_hunk_loc + old_loc - 1 # index from 0
            old_log = gumtree.get_old_log()

            # get log loc in new hunk, new loc and new log
            new_loc = gumtree.get_new_loc()
            new_log = gumtree.get_new_log()
            # if has corresponding new log
            if new_loc != -1:
                # remove mapping new_log_loc
                if new_loc in new_log_loc:
                    new_log_loc.remove(new_loc)
                new_loc = new_hunk_loc + new_loc - 1
            new_hunk_log_loc = new_loc + 1 - new_hunk_loc
            # action type = hunk action type + log edit flag
            curr_action_type = action_type + gumtree.is_old_log_edited()
            # check whether deleted log comes with deleted check
            if new_loc == -1 and gumtree.is_log_check_deleted():
                curr_action_type = my_constant.LOG_DELETE_CHECK
            log_writer.writerow(hunk_info + [old_hunk_log_loc, new_hunk_log_loc, old_loc, new_loc, old_log, new_log, curr_action_type])
            total_log += 1

    # deal with inserted log
    for new_loc in new_log_loc:
        if gumtree.set_new_loc(new_loc):
            # new loc and new log
            new_hunk_log_loc = new_loc
            new_loc = new_hunk_loc + new_loc - 1
            new_log = gumtree.get_new_log()

            # old loc and old log
            old_loc = -1
            old_hunk_log_loc = old_loc + 1 - old_hunk_loc
            old_log = None

            # action type = hunk action type + 1(always edited)
            curr_action_type = action_type + 1
            log_writer.writerow(hunk_info + [old_hunk_log_loc, new_hunk_log_loc, old_loc, new_loc, old_log, new_log, curr_action_type])
            total_log += 1

    return total_log

def fetch_hunk():
    """
    @ param nothing \n
    @ return nothing \n
    @ involve fetch and analyze each hunk with deal hunk function\n
    """
    # initiate csvfile
    hunk_file = file(my_constant.FETCH_HUNK_FILE_NAME, 'rb')
    hunk_records = csv.reader(hunk_file)
    log_file = file(my_constant.FETCH_LOG_FILE_NAME, 'wb')
    log_writer = csv.writer(log_file)
    log_writer.writerow(my_constant.FETCH_LOG_TITLE)

    total_log = 0
    total_hunk = 0
    gumtree = Gumtree()
    hunk_size, hunk_records = my_util.get_csv_record_len(hunk_records)
    # call deal hunk to anlyze each hunk file
    for hunk_record in islice(hunk_records, 1, None):
        total_hunk += 1
        total_log = deal_hunk(hunk_record, log_writer, gumtree, total_log)
        if total_hunk % 10 == 0:
            print 'have dealed with %d/%d hunk, have dealed with %d log' %(total_hunk, hunk_size, total_log)
    
    # close file
    hunk_file.close()
    log_file.close()

"""
main function
"""
if __name__ == "__main__":
    fetch_hunk()
    # gumtree_api.close_jvm()