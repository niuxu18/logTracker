#-*-coding: utf-8 -*-
import csv
import re
import commands
import json
import my_constant
import my_util

def store_hunk(old_hunk, new_hunk, patch_hunk, total_log_hunk):
    """
    @ param old and new hunk, patch hunk, log hunk counter\n
    @ return hunk counter, old and new and patch hunk name\n
    @ involve store hunk file, including old, new and intial patch hunk\n
    """
    total_log_hunk += 1
    print 'now storing hunk: %d' %(total_log_hunk)
    # store old hunk file
    old_hunk_name = my_constant.DOWNLOAD_OLD_HUNK + str(total_log_hunk) + '.cpp'
    my_util.save_file(old_hunk, old_hunk_name)

    # store new hunk file
    new_hunk_name = my_constant.DOWNLOAD_NEW_HUNK + str(total_log_hunk) + '.cpp'
    my_util.save_file(new_hunk, new_hunk_name)

    # store patch hunk file
    patch_hunk_name = my_constant.DOWNLOAD_PATCH_HUNK + str(total_log_hunk) + '.cpp'
    my_util.save_file(patch_hunk, patch_hunk_name)

    return total_log_hunk, old_hunk_name, new_hunk_name, patch_hunk_name

def deal_file_diff( file_diff_info, file_diff, log_function, total_log_hunk, total_hunk, total_log_changes, total_changes, writer):
    """
    @ param file diff info[version, old and new file],
            patch, log function, log hunk counter, hunk counter, changed lines counter and file writer\n
    @ return new log hunk counter and new hunk counter as well as changed lines counter\n
    @ involve recognize and deal with each hunk in file diff
              and save hunk info(has log)\n
    """
    # old and new hunk content
    old_hunk = new_hunk = patch_hunk = ''
    # old and new file location of hunk top
    old_hunk_loc = new_hunk_loc = 0
    old_loc = new_loc = 0
    # old and new log locations
    old_log_loc = []
    new_log_loc = []

    # deal with each line of patch
    file_diff = file_diff[2:]
    for line in file_diff:
        # recognize change hunk by description info
        is_hunk = re.match(r'^@@.*-(.*),.*\+(.*),.*@@$', line)
        # deal with past hunk and record new one
        if is_hunk:
            total_hunk += 1
            print 'now processing hunk %d' %(total_hunk)
            # if has log modification
            if len(old_log_loc) != 0 or len(new_log_loc) != 0:
                total_log_hunk, old_hunk_name, new_hunk_name, patch_hunk_name = store_hunk(old_hunk, new_hunk, patch_hunk, total_log_hunk)
                writer.writerow(file_diff_info + [patch_hunk_name, old_hunk_name, new_hunk_name, \
                    old_hunk_loc, new_hunk_loc, json.dumps(old_log_loc), json.dumps(new_log_loc)])
            # initialize hunk info
            old_hunk = new_hunk = patch_hunk = ''
            old_hunk_loc = is_hunk.group(1)
            new_hunk_loc = is_hunk.group(2)
            old_loc = new_loc = 0
            old_log_loc = []
            new_log_loc = []
            continue

        # record change type flag
        change_type = line[0]
        if change_type not in ['-', '+', ' ']:
            continue
        patch_hunk += line
        line = line[1:]
        # decide if it belongs to log change
        is_log_change = re.search(log_function, line, re.I)
        # + and common
        if change_type != '-':
            new_hunk += line
            if is_log_change:
                new_log_loc.append(new_loc)
            new_loc += 1
        # - and common
        if change_type != '+':
            old_hunk += line
            if is_log_change:
                old_log_loc.append(old_loc)
            old_loc += 1
        if change_type == '-' or change_type == '+':
            if is_log_change:
                total_log_changes += 1
            else:
                total_changes += 1

    # deal with last hunk, if has log update
    total_hunk += 1
    print 'now processing hunk %d' %(total_hunk)
    if len(old_log_loc) != 0 or len(new_log_loc) != 0:
        total_log_hunk, old_hunk_name, new_hunk_name, patch_hunk_name = store_hunk(old_hunk, new_hunk, patch_hunk, total_log_hunk)
        writer.writerow(file_diff_info + [patch_hunk_name, old_hunk_name, new_hunk_name, \
            old_hunk_loc, new_hunk_loc, json.dumps(old_log_loc), json.dumps(new_log_loc)])

    return total_log_hunk, total_hunk, total_log_changes, total_changes

def deal_version_diff( version_diff_file, log_function, total_log_hunk, total_hunk, total_log_changes, total_changes, writer):
    """
    @ param version diff file, log function, log hunk writer, hunk counter, changed line counter and file writer\n
    @ return new log hunk counter and hunk counter as well as changed line counter\n
    @ involve recognize and deal with each patch diff file from version diff file\n
    """
    # open version diff file
    full_version_diff_file = open(my_constant.PATCH_DIR + version_diff_file, 'rb')
    version_diff = full_version_diff_file.readlines()

    file_diff = []
    is_diff_file = False
    old_file = new_file = None
    for i in range(len(version_diff)):
        # get diff file
        is_diff = re.match(r'^diff .*', version_diff[i])
        if is_diff:
            # get old file name
            i += 1
            is_old = re.match(r'^--- (\S*)\s*.*', version_diff[i])
            if is_old:
                temp_old_file = is_old.group(1)
                # filter file by name (cpp like and not test like)
                if my_util.filter_file(temp_old_file):
                    # get new file name
                    i += 1
                    is_new = re.match(r'^\+\+\+ (\S*)\s*.*', version_diff[i])
                    if is_new:
                        temp_new_file = is_new.group(1)
                        # filter file by name (cpp like and not test like)
                        if my_util.filter_file(temp_new_file):
                            # deal with previous diff file
                            if is_diff_file:
                                total_log_hunk, total_hunk, total_log_changes, total_changes = \
                                             deal_file_diff([version_diff_file, old_file, new_file], \
                                                    file_diff, log_function, total_log_hunk, total_hunk, total_log_changes, total_changes, writer)
                                file_diff = []
                            # mark this file need to be dealed
                            is_diff_file = True
                            old_file = temp_old_file
                            new_file = temp_new_file
                            continue            
            # mark end of previous diff file and deal with previous diff file
            if is_diff_file:
                is_diff_file = False
                total_log_hunk, total_hunk, total_log_changes, total_changes = \
                     deal_file_diff([version_diff_file, old_file, new_file], \
                                    file_diff, log_function, total_log_hunk, total_hunk, total_log_changes, total_changes, writer)
                file_diff = []
        # record diff file content
        if is_diff_file:
            file_diff.append(version_diff[i])

    # deal with last file diff
    if is_diff_file:
        total_log_hunk, total_hunk, total_log_changes, total_changes = \
             deal_file_diff([version_diff_file, old_file, new_file], \
                                file_diff, log_function, total_log_hunk, total_hunk, total_log_changes, total_changes, writer)
    # close file
    full_version_diff_file.close()
    return total_log_hunk, total_hunk, total_log_changes, total_changes

def fetch_version_diff(is_recreate=False):
    """
    @ param flag about whether recreate version diff\n
    @ return nothing\n
    @ involve read patch file from patch dir and deal with each version patch file\n
    """
    # call create version diff if is_recreate flag is set
    if is_recreate:
        create_version_diff()
    # choose the one with log statement changes
    log_functions = my_util.retrieve_log_function(my_constant.LOG_CALL_FILE_NAME)
    log_function = my_util.function_to_regrex_str(log_functions)
    # initiate csv file
    hunk_file = file(my_constant.FETCH_HUNK_FILE_NAME, 'wb')
    hunk_writer = csv.writer(hunk_file)
    hunk_writer.writerow(my_constant.FETCH_HUNK_TITLE)
    # fetch patch file from patch dir and deal with each diff file
    version_diff_files = commands.getoutput('ls ' + my_constant.PATCH_DIR)
    version_diff_files = version_diff_files.split('\n')
    total_log_hunk = 0
    total_hunk = 0
    total_log_changes = 0
    total_changes = 0
    for version_diff_file in version_diff_files:
        print 'now processing patch %s' %version_diff_file
        total_log_hunk, total_hunk, total_log_changes, total_changes = \
            deal_version_diff(version_diff_file, log_function, \
                total_log_hunk, total_hunk, total_log_changes, total_changes, hunk_writer)
    # close file and output analysis result
    hunk_file.close()
    commands.getoutput('echo ' + my_constant.REPOS + ': log hunk, hunk >> data/evaluate/statistics.txt')
    commands.getoutput('echo ' + str(total_log_hunk) + ',' + str(total_hunk) + ' >> data/evaluate/statistics.txt')
    commands.getoutput('echo ' + my_constant.REPOS + ': log changes, changes >> data/evaluate/statistics.txt')
    commands.getoutput('echo ' + str(total_log_changes) + ',' + str(total_changes) + ' >> data/evaluate/statistics.txt')



def create_version_diff():
    """
    @ param nothing\n
    @ return nothing\n
    @ involve create dir diff file(store in patch dir) for dirs in repos dir\n
    """
    # clear old patch file
    clear = commands.getoutput('rm ' + my_constant.PATCH_DIR + '*')
    # get all versions
    versions = commands.getoutput('ls ' + my_constant.REPOS_DIR)
    versions = versions.split('\n')
    versions.sort(key=my_util.get_version_number)
    size = len(versions)
    for i in range(size - 1):
        print 'now creating patch for %s and %s' %(versions[i], versions[i + 1])
        patch = commands.getoutput('diff -BEr -U 6 ' + my_constant.REPOS_DIR + versions[i] + ' '\
                                + my_constant.REPOS_DIR + versions[i + 1] + ' > ' \
                                + my_constant.PATCH_DIR + versions[i] + '_diff_' + versions[i + 1])

"""
main function
"""
if __name__ == "__main__":
    # param is about whether call create version diff before analysis
    # fetch_version_diff(True)
    create_version_diff()


