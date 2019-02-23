#!/bin/sh

MYCODE_DIR="/usr/info/code/cpp/LogMonitor/LogMonitor"
SMARTLOG_DIR="/opt/llvm/tools/clang/tools/SmartLog"
REPOS="bftpd"
CODE_DIR="."

# code
echo "generating compiled_files.def and call_dependence.csv";
cd ${CODE_DIR}
tmp=`${SMARTLOG_DIR}/script/extract_command_11.pl compile_commands.json`
tmp=`./build_ir.sh`
tmp=`bash ${SMARTLOG_DIR}/script/call_dependence.sh`

echo "generating logging_statement.out";
tmp=`cat compiled_files.def | xargs clang-smartlog -find-logging-behavior > tmp.txt`

echo "cp logging statement:";
tmp=`cp ${CODE_DIR}/logging_statement.out ${MYCODE_DIR}/second/sample/${REPOS}/${REPOS}_logging_statement.csv`
# echo "run python file:";
# tmp=`python ${MYCODE_DIR}/src/cluster_context_with_function.py`;
# echo $tmp;