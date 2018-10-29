import my_constant
import my_util
import statistics
import fetch_hunk
import analyze_hunk
import gumtree_api
import analyze_control_old_new
import analyze_control_old_new_cluster
import analyze_control_clone
import argparse
import commands

def set_generate_input_and_output(parent_dir):
    """
    @ param parent_dir\n
    @ return flag about whether success\n
    @ involve set input and output for generating rules\n
    """
    # reset log statement dir
    my_constant.reset_logstatement_dir(parent_dir)

    history_versions_dir = parent_dir + '/versions'
    if commands.getoutput('ls ' + history_versions_dir).startswith('ls: cannot'):
        print "can not find historical versions in %s" %history_versions_dir
        return False
    my_constant.reset_generate_input(history_versions_dir)

    generate_output_dir = parent_dir + '/generate'
    my_util.create_dir_if_no(generate_output_dir)
    my_constant.reset_generate_output(generate_output_dir)
    return True

def generate_rules(parent_dir):
    """
    @ param parent_dir\n
    @ return store cluster file etc. in output dir \n
    @ involve generate log revision rules\n
    """
    if set_generate_input_and_output(parent_dir) == False:
        return

    my_util.create_dir_if_no(my_constant.PATCH_DIR)
    my_util.create_dir_if_no(my_constant.GUMTREE_DIR)

    print '\n****************now generating rules for repos %s***************' %(my_constant.REPOS)
    # analyze hunk
    fetch_hunk.fetch_version_diff(True)
    analyze_hunk.fetch_hunk()

    # analyze gumtree and srcml
    analyze_control_old_new.analyze_old_new(True)
    
    # generate rule
    analyze_control_old_new_cluster.cluster()
    print 'now generate class'
    analyze_control_old_new_cluster.generate_class()
    print 'now generate xlsx'
    analyze_control_old_new_cluster.generate_xlsx_from_csv_cluster()
    print 'exit'

def apply_rules(parent_dir, apply_version):
    """
    @ param parent_dir\n
    @ return store candidate file etc. in output dir \n
    @ involve apply log revision rules\n
    """
    if set_generate_input_and_output(parent_dir) == False:
        return

    my_constant.reset_apply_input(apply_version)

    apply_output_dir = parent_dir + '/generate'
    my_util.create_dir_if_no(apply_output_dir)
    my_constant.reset_generate_output(apply_output_dir)
    my_constant.reset_apply_output(apply_output_dir)


    print '\n****************now applying rules for repos %s***************' %(my_constant.REPOS)
    # apply rule
    analyze_control_clone.seek_clone(my_constant.REPOS_NAME, True)
    print 'now generate xlsx'
    analyze_control_clone.generate_xlsx_from_clone()
    print 'now calculate call times'
    statistics.statistical_repos_call_log_times('')


def command():
    """
    @ param nothing\n
    @ return nothing \n
    @ involve show command and deal with command\n
    """
    parser = argparse.ArgumentParser(description="LogTracker: learn and apply log revision rules from software evolution history\n \
                                       e.g., python logTracker.py -r bftpd -p ../second/sample/bftpd -g (-a bftpd-4.8)")

    # argument key, value
    parser.add_argument("-r", "--repos", type=str, required=True, \
        help="set repos name")
    
    # argument input, output
    parser.add_argument("-p", "--parent_dir", type=str,  required=True,\
        help="parent dir for history versions, generate and apply output")

    
    # arguments set, generate, apply
    choice_group = parser.add_mutually_exclusive_group(required=True)
    choice_group.add_argument("-g", "--generate", help="generate log revision rules from historical versions", action="store_true")
    choice_group.add_argument("-a", "--apply", help="apply log revision rules to given version of source code", action="store_true")

    parser.add_argument("-v", "--apply_version", type=str,\
        help="apply version name when applying rules")
    args = parser.parse_args()


    # process with arguments
    if args.repos:
        my_constant.reset_repos(args.repos)

    if args.generate:
        generate_rules(args.parent_dir)
    elif args.apply:
        apply_rules(args.parent_dir, args.apply_version)

"""
main function
"""
if __name__ == "__main__":
    command()