#-*-coding: utf-8 -*-
"""
@ involve : constant definition
"""

"""
repository
"""
REPOS = 'opendds'

"""
generate related files
"""
RULES_DIR = 'second/sample/' + REPOS + '/generate/'
FUNC_SIMILAIRTY_FILE_NAME = RULES_DIR + REPOS + '_func_similarity.csv'
FETCH_HUNK_FILE_NAME = RULES_DIR + REPOS + '_hunk_fetch.csv'
FETCH_LOG_FILE_NAME = RULES_DIR + REPOS + '_log_fetch.csv'
ANALYZE_OLD_NEW_GUMTREE_FILE_NAME = RULES_DIR + REPOS + '_old_new_gumtree_analyze.csv'
ANALYZE_OLD_NEW_LLVM_FILE_NAME = RULES_DIR + REPOS + '_old_new_llvm_analyze.csv'
CLUSTER_FEATURE_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_feature.csv'
CLUSTER_EDITION_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_edition.csv'
CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_edition_and_feature.csv'
CLUSTER_EDITION_AND_FEATURE_WITHOUT_CONTENT_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_edition_and_feature_without_content.csv'
CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_class_edition_and_feature.csv'
CLUSTER_FILE_NAME = RULES_DIR + REPOS + '_cluster.xlsx'
CLASS_FILE_NAME = RULES_DIR + REPOS + '_class.xlsx'

"""
stroed file name prefix
"""
# # parent
# CURR_REPOS_DIR = 'second/sample/' + REPOS + '/versions'
# repos
REPOS_DIR = 'second/sample/' + REPOS + '/versions/'
# patch dir
PATCH_DIR = RULES_DIR + 'patch/'
# gumtree dir(hunk, block, function)
GUMTREE_DIR = RULES_DIR + 'gumtree/'
"""
middle files
"""
# hunk
DOWNLOAD_PATCH_HUNK = GUMTREE_DIR + REPOS + '_patch_hunk_'
DOWNLOAD_OLD_HUNK = GUMTREE_DIR + REPOS + '_old_hunk_'
DOWNLOAD_NEW_HUNK = GUMTREE_DIR + REPOS + '_new_hunk_'
# log
SAVE_OLD_LOG = GUMTREE_DIR + REPOS + '_old_log_'
SAVE_NEW_LOG = GUMTREE_DIR + REPOS + '_new_log_'
# function
SAVE_OLD_FUNCTION = GUMTREE_DIR + REPOS + '_old_function_'
SAVE_NEW_FUNCTION = GUMTREE_DIR + REPOS + '_new_function_'
SAVE_REPOS_FUNCTION = GUMTREE_DIR + REPOS + '_repos_function_'

"""
log statement dir and file name
"""
LOG_STATMENT_DIR = 'second/sample/' + REPOS
LOG_CALL_FILE_NAME = LOG_STATMENT_DIR + '/' + REPOS + '_logging_statement.csv'

"""
apply related files
"""
LOG_REVISION_DIR = 'second/sample/' + REPOS + '/generate/'
# clone
ANALYZE_CLONE_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_log_seek_clone.csv'
ANALYZE_CLONE_FUNCTION_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_function_seek_clone.csv'
CLONE_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_clone.xlsx'
# repos
CLUSTER_REPOS_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_cluster.csv'
ANALYZE_REPOS_FUNCTION_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_call.csv'
ANALYZE_REPOS_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_log.csv'
CLUSTER_REPOS_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_cluster_log.csv'
CLASS_REPOS_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_class_log.csv'
CALL_LOG_TIMES_FILE_NAME = LOG_REVISION_DIR + REPOS + '_call_log_times.csv'

"""
class path for java
"""
# GUMTREE_HOME = '/opt/gumtree/dist/build/distributions/gumtree-20170722-2.1.0-SNAPSHOT'
GUMTREE_HOME = '/opt/gumtree/gumtree/dist/build/distributions/gumtree-20170703-2.1.0-SNAPSHOT'
JAVA_CLASS_PATH = '.:/usr/info/code/java/GumTreeUse/bin:' + GUMTREE_HOME + '/lib/annotations-2.0.1.jar:' + GUMTREE_HOME + '/lib/antlr-3.5.2.jar:' + GUMTREE_HOME + '/lib/antlr-runtime-3.5.2.jar:' + GUMTREE_HOME + '/lib/aopalliance-1.0.jar:' + GUMTREE_HOME + '/lib/app-1.3.200-v20130910-1609.jar:' + GUMTREE_HOME + '/lib/asm-3.1.jar:' + GUMTREE_HOME + '/lib/cglib-2.2.1-v20090111.jar:' + GUMTREE_HOME + '/lib/client.diff-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/client-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/common-3.6.200-v20130402-1505.jar:' + GUMTREE_HOME + '/lib/commons-codec-1.10.jar:' + GUMTREE_HOME + '/lib/commons-io-2.0.1.jar:' + GUMTREE_HOME + '/lib/commons-lang3-3.1.jar:' + GUMTREE_HOME + '/lib/commons-logging-1.2.jar:' + GUMTREE_HOME + '/lib/contenttype-3.4.200-v20140207-1251.jar:' + GUMTREE_HOME + '/lib/core-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.antlr3-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.antlr3-antlr-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.antlr3-json-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.antlr3-php-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.antlr3-r-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.antlr3-xml-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.c-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.css-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.jdt-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.js-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.ruby-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gen.srcml-2.1.0-SNAPSHOT.jar:' + GUMTREE_HOME + '/lib/gson-2.4.jar:' + GUMTREE_HOME + '/lib/guava-18.0.jar:' + GUMTREE_HOME + '/lib/guice-3.0.jar:' + GUMTREE_HOME + '/lib/javassist-3.18.2-GA.jar:' + GUMTREE_HOME + '/lib/javax.inject-1.jar:' + GUMTREE_HOME + '/lib/javax.servlet-api-3.1.0.jar:' + GUMTREE_HOME + '/lib/jetty-http-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jetty-io-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jetty-security-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jetty-server-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jetty-servlet-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jetty-util-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jetty-webapp-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jetty-xml-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/jobs-3.6.0-v20140424-0053.jar:' + GUMTREE_HOME + '/lib/jrubyparser-0.5.3.jar:' + GUMTREE_HOME + '/lib/jsr305-3.0.1.jar:' + GUMTREE_HOME + '/lib/jtidy-r938.jar:' + GUMTREE_HOME + '/lib/junit-4.8.2.jar:' + GUMTREE_HOME + '/lib/org.eclipse.core.resources-3.10.0.v20150423-0755.jar:' + GUMTREE_HOME + '/lib/org.eclipse.jdt.core-3.11.0.v20150602-1242.jar:' + GUMTREE_HOME + '/lib/osgi-3.10.0-v20140606-1445.jar:' + GUMTREE_HOME + '/lib/ph-commons-8.3.0.jar:' + GUMTREE_HOME + '/lib/ph-css-5.0.1.jar:' + GUMTREE_HOME + '/lib/preferences-3.5.200-v20140224-1527.jar:' + GUMTREE_HOME + '/lib/reflections-0.9.10.jar:' + GUMTREE_HOME + '/lib/registry-3.5.400-v20140428-1507.jar:' + GUMTREE_HOME + '/lib/rendersnake-1.9.0.jar:' + GUMTREE_HOME + '/lib/rhino-1.7.7.jar:' + GUMTREE_HOME + '/lib/runtime-3.10.0-v20140318-2214.jar:' + GUMTREE_HOME + '/lib/simmetrics-core-3.2.3.jar:' + GUMTREE_HOME + '/lib/slf4j-api-1.7.21.jar:' + GUMTREE_HOME + '/lib/spark-core-2.5.2.jar:' + GUMTREE_HOME + '/lib/spring-aop-4.1.6.RELEASE.jar:' + GUMTREE_HOME + '/lib/spring-beans-4.1.6.RELEASE.jar:' + GUMTREE_HOME + '/lib/spring-context-4.1.6.RELEASE.jar:' + GUMTREE_HOME + '/lib/spring-core-4.1.6.RELEASE.jar:' + GUMTREE_HOME + '/lib/spring-expression-4.1.6.RELEASE.jar:' + GUMTREE_HOME + '/lib/spring-web-4.1.6.RELEASE.jar:' + GUMTREE_HOME + '/lib/spring-webmvc-4.1.6.RELEASE.jar:' + GUMTREE_HOME + '/lib/ST4-4.0.8.jar:' + GUMTREE_HOME + '/lib/trove4j-3.0.3.jar:' + GUMTREE_HOME + '/lib/websocket-api-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/websocket-client-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/websocket-common-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/websocket-server-9.3.6.v20151106.jar:' + GUMTREE_HOME + '/lib/websocket-servlet-9.3.6.v20151106.jar'


"""
fetch hunk file title and index
"""
FETCH_HUNK_TITLE = ['patch_file', 'old_file', 'new_file', 'patch_hunk_file','old_hunk_file', 'new_hunk_file', \
    'old_hunk_loc', 'new_hunk_loc', 'old_log_loc', 'new_log_loc']
FETCH_HUNK_OLD_HUNK_LOC = FETCH_HUNK_TITLE.index('old_hunk_loc')
FETCH_HUNK_NEW_HUNK_LOC = FETCH_HUNK_TITLE.index('new_hunk_loc')
FETCH_HUNK_OLD_LOG_LOC = FETCH_HUNK_TITLE.index('old_log_loc')
FETCH_HUNK_NEW_LOG_LOC = FETCH_HUNK_TITLE.index('new_log_loc')
FETCH_HUNK_OLD_HUNK_FILE = FETCH_HUNK_TITLE.index('old_hunk_file')
FETCH_HUNK_NEW_HUNK_FILE = FETCH_HUNK_TITLE.index('new_hunk_file')

"""
fetch log file title and index
"""
FETCH_LOG_TITLE = ['patch_file', 'old_file', 'new_file', 'patch_hunk_file', 'old_hunk_file', 'new_hunk_file', \
  'old_hunk_loc', 'new_hunk_loc', 'old_loc', 'new_loc', 'old_log', 'new_log', 'action_type']
FETCH_LOG_OLD_LOC = FETCH_LOG_TITLE.index('old_loc')
FETCH_LOG_NEW_LOC = FETCH_LOG_TITLE.index('new_loc')
FETCH_LOG_OLD_LOG = FETCH_LOG_TITLE.index('old_log')
FETCH_LOG_NEW_LOG = FETCH_LOG_TITLE.index('new_log')
FETCH_LOG_OLD_FILE = FETCH_LOG_TITLE.index('old_file')
FETCH_LOG_NEW_FILE = FETCH_LOG_TITLE.index('new_file')
FETCH_LOG_OLD_HUNK_FILE = FETCH_LOG_TITLE.index('old_hunk_file')
FETCH_LOG_ACTION_TYPE = FETCH_LOG_TITLE.index('action_type')

"""
analyze old new title and index
"""
# 'old_block', 'old_block_file', 'old_block_feature',
ANALYZE_OLD_NEW_GUMTREE_TITLE = FETCH_LOG_TITLE + ['old_function', 'old_function_loc', 'new_function', 'new_function_loc', 'edit_types', 'syntactical_edits', 'semantical_edits', 'edit_word', 'edit_feature']

ANALYZE_EDIT_TYPE = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('edit_types')
ANALYZE_SYNTACTICAL_EDIT = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('syntactical_edits')
ANALYZE_SEMANTICAL_EDIT = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('semantical_edits')
ANALYZE_EDIT_WORD = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('edit_word')
ANALYZE_EDIT_FEATURE = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('edit_feature')

ANALYZE_OLD_FUNCTION = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('old_function')
ANALYZE_OLD_FUNCTION_LOC = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('old_function_loc')
ANALYZE_NEW_FUNCTION = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('new_function')
ANALYZE_NEW_FUNCTION_LOC = ANALYZE_OLD_NEW_GUMTREE_TITLE.index('new_function_loc')

ANALYZE_OLD_NEW_LLVM_TITLE = ANALYZE_OLD_NEW_GUMTREE_TITLE + ['check', 'variable', 'ddg_codes', 'ddg_locs']
ANALYZE_CHECK = ANALYZE_OLD_NEW_LLVM_TITLE.index('check')
ANALYZE_VARIABLE = ANALYZE_OLD_NEW_LLVM_TITLE.index('variable')
# cluster and class
CLUSTER_OLD_NEW_TITLE = ANALYZE_OLD_NEW_LLVM_TITLE + ['cluster']
ANALYZE_CLUSTER = CLUSTER_OLD_NEW_TITLE.index('cluster')
CLASS_OLD_NEW_TITLE = ['class', 'class_size', 'patch_file', 'patch_hunk_file', 'new_file', 'old_loc', 'new_loc', 'old_log', 'new_log', 'old_function', 'old_function_loc', 'new_function', 'new_function_loc', 'check', 'variable', 'semantical_edits', 'edit_word']
CLASS_OLD_NEW_PATCH_FILE_NAME = CLASS_OLD_NEW_TITLE.index('patch_file')
CLASS_OLD_NEW_NEW_FILE_NAME = CLASS_OLD_NEW_TITLE.index('new_file')
CLASS_OLD_NEW_NEW_LOC = CLASS_OLD_NEW_TITLE.index('new_loc')
CLASS_OLD_NEW_OLD_LOC = CLASS_OLD_NEW_TITLE.index('old_loc')
CLASS_OLD_NEW_OLD_LOG = CLASS_OLD_NEW_TITLE.index('old_log')
CLASS_OLD_NEW_NEW_LOG = CLASS_OLD_NEW_TITLE.index('new_log')
CLASS_OLD_NEW_CHECK = CLASS_OLD_NEW_TITLE.index('check')
CLASS_OLD_NEW_VARIABLE = CLASS_OLD_NEW_TITLE.index('variable')
CLASS_OLD_NEW_EDIT_WORD = CLASS_OLD_NEW_TITLE.index('edit_word')
CLASS_OLD_NEW_NEW_FUNCTION = CLASS_OLD_NEW_TITLE.index('new_function')
CLASS_OLD_NEW_NEW_FUNCTION_LOC = CLASS_OLD_NEW_TITLE.index('new_function_loc')

"""
analyze repos log title and index
"""
#'block', 'block_file', 'block_feature',
ANALYZE_REPOS_LOG_TITLE = ['file', 'function', \
                             'loc','log', 'check', 'variable']
ANALYZE_REPOS_LOG_FUNCTION = ANALYZE_REPOS_LOG_TITLE.index('function')
ANALYZE_REPOS_LOG_LOC = ANALYZE_REPOS_LOG_TITLE.index('loc')
ANALYZE_REPOS_LOG_LOG = ANALYZE_REPOS_LOG_TITLE.index('log')
ANALYZE_REPOS_LOG_CHECK = ANALYZE_REPOS_LOG_TITLE.index('check')
ANALYZE_REPOS_LOG_VARIABLE = ANALYZE_REPOS_LOG_TITLE.index('variable')

"""
analyze repos function title and index
"""
ANALYZE_REPOS_FUNCTION_TITLE =['file', 'function','calls', 'types']
ANALYZE_REPOS_FUNCTION_FUNCTION_NAME = ANALYZE_REPOS_FUNCTION_TITLE.index('function')
ANALYZE_REPOS_FUNCTION_CALLS = ANALYZE_REPOS_FUNCTION_TITLE.index('calls')
ANALYZE_REPOS_FUNCTION_TYPES = ANALYZE_REPOS_FUNCTION_TITLE.index('types')
# cluster and class
CLUSTER_REPOS_LOG_TITLE = ANALYZE_REPOS_LOG_TITLE + ['cluster']
ANALYZE_REPOS_LOG_CLUSTER = CLUSTER_REPOS_LOG_TITLE.index('cluster')
CLASS_REPOS_LOG_TITLE = ['class', 'class_size', 'check', 'variable']
CLASS_REPOS_LOG_CHECK = CLASS_REPOS_LOG_TITLE.index('check')
CLASS_REPOS_LOG_VARIABLE = CLASS_REPOS_LOG_TITLE.index('variable')

"""
several postfix
"""
LAST_REPOS='_last_repos'
FIRST_REPOS='_first_repos'
REPOS_NAME = '_last_repos'

"""
analyze clone title
"""
ANALYZE_CLONE_LOG_TITLE = CLASS_OLD_NEW_TITLE + ANALYZE_REPOS_LOG_TITLE + ['recommended_edit_scripts', 'necessity']
ANALYZE_CLONE_LOG_FUNCTION_LOC = ANALYZE_CLONE_LOG_TITLE.index('loc')
ANALYZE_CLONE_LOG_FUNCTION_LOG = ANALYZE_CLONE_LOG_TITLE.index('log')
ANALYZE_CLONE_FUNCTION_TITLE = CLASS_OLD_NEW_TITLE + ANALYZE_REPOS_FUNCTION_TITLE + ['recommended_edit_scripts', 'necessity']
ANALYZE_CLONE_FUNCTION_FUNCTION = ANALYZE_CLONE_FUNCTION_TITLE.index('function')

CLONE_LOG_TITLE = CLUSTER_OLD_NEW_TITLE + ANALYZE_REPOS_LOG_TITLE + ['recommended_edit_scripts', 'necessity']
CLONE_FUNCTION_TITLE = CLUSTER_OLD_NEW_TITLE + ANALYZE_REPOS_FUNCTION_TITLE + ['recommended_edit_scripts', 'necessity']

CALL_LOG_TIMES_TITLE = ['function', 'call_times', 'log_times']
"""
flag type && log type
"""
LOG_FEATURE_MODIFY = 4
LOG_OTHER_LOG_FEATURE_MODIFY = 6
LOG_OTHER_LOG_MODIFY = 2
LOG_NO_MODIFY = 0
LOG_DELETE_CHECK = 9
LOG_DDG_MODIFY = 10
LOG_LOG_MODIFY = 3
LOG_LOG_FEATURE_MODIFY = 7

"""
log edit type info
"""
LOG_EDIT_TYPES = ["addLog", "removeLog", "moveLog", "updateLog", "addVariable", "removeVariable",\
          "updateVariable", "moveVariable", "addContent", "removeContent",\
          "updateContent", "moveContent"]

"""
ast node type for deckard(8)
"""
DECKARD_AST_NODE_TYPES = ["call", "argument", "literal", "name", "decl", "operator", "modifier", "specifier"]

"""
data dependence type
"""
# level 1
VAR_FUNC_RETURN = 0
FlAG_FUNC_RETURN = '_ret'
# level 2
VAR_FUNC_ARG_RETURN = 1
FlAG_FUNC_ARG_RETURN = '_arg_ret'
# level 3
VAR_FUNC_ARG = 3
FlAG_FUNC_ARG = '_arg'
# level 4
VAR_TYPE = 4
FlAG_TYPE = ''

"""
split string for statement to get tokens
"""
SPLIT_STR = r'[\W\s_]'
SPLIT_ALGORITHM = r'[+-\*/%=]'
SPLIT_LOG = r'[^\w%&/\[\]\*\\]'

CPP_FILE_FORMAT = r'\.(c|cpp|cc|cxx|h)$'
UNSRCML_FILE_FORMAT = r'\.(h|c|cc|cxx)$'

"max clone counter"
MAX_FUNCTION_CLONE = 100
MAX_LOG_IN_HUNK = 100

"must log functions"
LOG_MUST = ['debug']
"log function related but not log function"
LOG_VAGUE = ['_', 'strerror']
def update_middle_files():
    """
    @ param nothing\n
    @ return nothing \n
    @ involve update gumtree dir, caused by update of gumtree dir or repos\n
    """
    # hunk
    global DOWNLOAD_PATCH_HUNK
    DOWNLOAD_PATCH_HUNK = GUMTREE_DIR + REPOS + '_patch_hunk_'
    global DOWNLOAD_OLD_HUNK
    DOWNLOAD_OLD_HUNK = GUMTREE_DIR + REPOS + '_old_hunk_'
    global DOWNLOAD_NEW_HUNK
    DOWNLOAD_NEW_HUNK = GUMTREE_DIR + REPOS + '_new_hunk_'
    # log
    global SAVE_OLD_LOG
    SAVE_OLD_LOG = GUMTREE_DIR + REPOS + '_old_log_'
    global SAVE_NEW_LOG
    SAVE_NEW_LOG = GUMTREE_DIR + REPOS + '_new_log_'
    # function
    global SAVE_OLD_FUNCTION
    SAVE_OLD_FUNCTION = GUMTREE_DIR + REPOS + '_old_function_'
    global SAVE_NEW_FUNCTION
    SAVE_NEW_FUNCTION = GUMTREE_DIR + REPOS + '_new_function_'
    global SAVE_REPOS_FUNCTION
    SAVE_REPOS_FUNCTION = GUMTREE_DIR + REPOS + '_repos_function_'

def update_apply_related_file():
    """
    @ param nothing\n
    @ return nothing \n
    @ involve update apply related file, caused by update of log revision rules and repos\n
    """
    # clone
    global ANALYZE_CLONE_LOG_FILE_NAME
    ANALYZE_CLONE_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_log_seek_clone.csv'
    global ANALYZE_CLONE_FUNCTION_FILE_NAME
    ANALYZE_CLONE_FUNCTION_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_function_seek_clone.csv'
    global CLONE_FILE_NAME
    CLONE_FILE_NAME = LOG_REVISION_DIR + REPOS + '_clone.xlsx'
    # repos
    global CLUSTER_REPOS_FILE_NAME
    CLUSTER_REPOS_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_cluster.csv'
    global ANALYZE_REPOS_FUNCTION_FILE_NAME
    ANALYZE_REPOS_FUNCTION_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_call.csv'
    global ANALYZE_REPOS_LOG_FILE_NAME
    ANALYZE_REPOS_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_log.csv'
    global CLUSTER_REPOS_LOG_FILE_NAME
    CLUSTER_REPOS_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_cluster_log.csv'
    global CLASS_REPOS_LOG_FILE_NAME
    CLASS_REPOS_LOG_FILE_NAME = LOG_REVISION_DIR + REPOS + '_repos_class_log.csv'
    global CALL_LOG_TIMES_FILE_NAME
    CALL_LOG_TIMES_FILE_NAME = LOG_REVISION_DIR + REPOS + '_call_log_times.csv'

def update_generate_related_file():
    """
    @ param nothing\n
    @ return nothing \n
    @ involve update generate related file, caused by update of rule dir and repos\n
    """
    global FUNC_SIMILAIRTY_FILE_NAME
    FUNC_SIMILAIRTY_FILE_NAME = RULES_DIR + REPOS + '_func_similarity.csv'
    global FETCH_HUNK_FILE_NAME
    FETCH_HUNK_FILE_NAME = RULES_DIR + REPOS + '_hunk_fetch.csv'
    global FETCH_LOG_FILE_NAME
    FETCH_LOG_FILE_NAME = RULES_DIR + REPOS + '_log_fetch.csv'
    global ANALYZE_OLD_NEW_GUMTREE_FILE_NAME
    ANALYZE_OLD_NEW_GUMTREE_FILE_NAME = RULES_DIR + REPOS + '_old_new_gumtree_analyze.csv'
    global ANALYZE_OLD_NEW_LLVM_FILE_NAME
    ANALYZE_OLD_NEW_LLVM_FILE_NAME = RULES_DIR + REPOS + '_old_new_llvm_analyze.csv'
    global CLUSTER_FEATURE_OLD_NEW_FILE_NAME
    CLUSTER_FEATURE_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_feature.csv'
    global CLUSTER_EDITION_OLD_NEW_FILE_NAME
    CLUSTER_EDITION_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_edition.csv'
    global CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME
    CLUSTER_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_edition_and_feature.csv'
    global CLUSTER_EDITION_AND_FEATURE_WITHOUT_CONTENT_OLD_NEW_FILE_NAME
    CLUSTER_EDITION_AND_FEATURE_WITHOUT_CONTENT_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_cluster_edition_and_feature_without_content.csv'
    global CLUSTER_FILE_NAME
    CLUSTER_FILE_NAME = RULES_DIR + REPOS + '_cluster.xlsx'
    global CLASS_FILE_NAME
    CLASS_FILE_NAME = RULES_DIR + REPOS + '_class.xlsx'
    global CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME
    CLASS_EDITION_AND_FEATURE_OLD_NEW_FILE_NAME = RULES_DIR + REPOS + '_old_new_class_edition_and_feature.csv'

def reset_generate_input(new_repos_dir):
    """
    @ param input of generate rules, version dir\n
    @ return nothing \n
    @ involve update version dir, that is patch dir\n
    """
    global REPOS_DIR
    REPOS_DIR = new_repos_dir + '/'

def reset_generate_output(new_rules_dir):
    """
    @ param output of generate rules, rules dir\n
    @ return nothing \n
    @ involve update rules dir\n
    """
    # rules dir
    """
    file name
    """
    global RULES_DIR
    RULES_DIR = new_rules_dir + '/'
    update_generate_related_file()

    # patch dir and gumtree dir
    global PATCH_DIR
    PATCH_DIR = RULES_DIR + 'patch/'
    global GUMTREE_DIR
    GUMTREE_DIR = RULES_DIR + 'gumtree/'
    update_middle_files()

def reset_apply_input(new_apply_version_name):
    """
    @ param input of apply rules, applied repos dir\n
    @ return nothing \n
    @ involve update applied repos dir\n
    """
    global REPOS_NAME
    REPOS_NAME = new_apply_version_name

def reset_apply_output(new_log_revision_dir):
    """
    @ param output of apply rules, log revision dir\n
    @ return nothing \n
    @ involve update log revision dir\n
    """
    global LOG_REVISION_DIR
    LOG_REVISION_DIR = new_log_revision_dir + '/'
    update_apply_related_file()

def reset_logstatement_dir(new_log_statement_dir):
    """
    @ param new log statement dir\n
    @ return nothing \n
    @ involve reset log statement dir\n
    """
    global LOG_STATMENT_DIR
    LOG_STATMENT_DIR = new_log_statement_dir
    global LOG_CALL_FILE_NAME
    LOG_CALL_FILE_NAME = LOG_STATMENT_DIR + '/'+ REPOS + '_logging_statement.csv'
    print "reset log statement file to %s" %LOG_CALL_FILE_NAME

def reset_repos(new_repos):
    """
    @ param new repository\n
    @ return nothing \n
    @ involve reset my_constant repos variable and related variable\n
    """
    global REPOS
    REPOS = new_repos

    """
    log statement file name
    """
    global LOG_CALL_FILE_NAME
    LOG_CALL_FILE_NAME = LOG_STATMENT_DIR+ '/' + REPOS + '_logging_statement.csv'

    """
    generate and apply related files
    """
    update_generate_related_file()
    update_apply_related_file()

    """
    stroed file name prefix
    """
    update_middle_files()

def reset_repos_series(new_repos):
    """
    @ param new repository\n
    @ return nothing \n
    @ involve reset my_constant repos variable and generate and apply relate variables\n
    """
    global REPOS
    REPOS = new_repos
    """
    log statement file name
    """
    reset_logstatement_dir('second/sample/' + REPOS)
    reset_generate_input('second/sample/' + REPOS + '/versions/')
    reset_generate_output('second/sample/' + REPOS + '/generate/')
    reset_apply_output('second/sample/' + REPOS + '/generate/')