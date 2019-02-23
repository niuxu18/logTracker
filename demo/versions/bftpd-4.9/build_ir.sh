#!/bin/bash



###This bash script is automatically produced by "extract_command.pl compile_commands.json", DO NOT CHANGE!###

total=0;
succ=0;
check(){
	if [ $? -eq 0 ]
	then
		succ=`expr $succ + 1`;
	fi
	total=`expr $total + 1`;
}

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/bftpdutmp.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/bftpdutmp.c.bc
check
echo "1 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/bftpdutmp.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/commands.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/commands.c.bc
check
echo "2 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/commands.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/commands_admin.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/commands_admin.c.bc
check
echo "3 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/commands_admin.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/cwd.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/cwd.c.bc
check
echo "4 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/cwd.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/dirlist.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/dirlist.c.bc
check
echo "5 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/dirlist.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/list.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/list.c.bc
check
echo "6 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/list.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/login.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/login.c.bc
check
echo "7 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/login.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/logging.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/logging.c.bc
check
echo "8 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/logging.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/main.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/main.c.bc
check
echo "9 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/main.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/mystring.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/mystring.c.bc
check
echo "10 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/mystring.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/options.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/options.c.bc
check
echo "11 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/options.c to bc" >&2

cd /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9
clang -g -emit-llvm -DHAVE_CONFIG_H -I/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9 -DVERSION=\"4.9\" -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -DPREFIX=\"/usr\" -c /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/md5.c -o /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/md5.c.bc
check
echo "12 /usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/bftpd/versions/bftpd-4.9/md5.c to bc" >&2
echo "Total ir $total" >&2
echo "Succ ir $succ" >&2
