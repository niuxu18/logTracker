#!/bin/sh
# while getopts ":repos:codeDir:smartLogDir:help:" opt
while getopts ":r:d:s:h" opt
do
    case $opt in
        r) # repos)
        REPOS=$OPTARG
        ;;
        d) #codeDir
        CODE_DIR=$OPTARG
        ;;
        s) #smartLogDir
        SMARTLOG=$OPTARG
        ;;
        h) #help
        echo "This bash file is used to call smartlog in given source code dir and generate corresponding log statement file"
        echo "./getLoggingStatement.sh -r bftpd -d ../second/sample/bftpd/versions/bftpd-4.9/ -s /opt/llvm/tools/clang/tools/SmartLog"
        echo "-r repos name"
        echo "-d directory of source code"
        echo "-s directory of smartlog tool(suggest to be defined as system variable)"
        echo "-h introductions of parameters"
        exit 1;;
        ?)
        echo "Do not support this parameter, see -h"
        exit 1;;
    esac
done

CURR_DIR=`pwd`
echo "generating compiled_files.def and call_dependence.csv";
cd ${CODE_DIR}
tmp=`${SMARTLOG}/script/extract_command_11.pl compile_commands.json`
tmp=`./build_ir.sh`
tmp=`bash ${SMARTLOG}/script/call_dependence.sh`

echo "generating logging_statement.out";
tmp=`cat compiled_files.def | xargs clang-smartlog -find-logging-behavior > tmp.txt`

echo "cp logging statement:";
tmp=`cp logging_statement.out ../../${REPOS}_logging_statement.csv`
cd ${CURR_DIR}
