
import urllib2
import os
import re
import my_constant
import commands

def download_file(main_url, file_name):
    """
    @ param main url and file name\n
    @ return true if success\n
    @ involve download tar.gz from given url\n
    """
    # # dir url
    # dir_url = main_url + file_name
    # dir_page = urllib2.urlopen(dir_url)
    # dir_html = dir_page.read().split('\n')
    # for line in dir_html:
    #     is_target = re.search(r'(postgre[a-zA-Z0-9]*postgre[a-zA-Z0-9]*-[0-9\.]*\.tar\.gz)', line, re.I)
    #     if is_target:
    #         file_name = is_target.group(1)

    # if 'v' in file_name:
    #     return False
    # file url
    file_url = main_url + file_name
    file_content = urllib2.urlopen(file_url)
    # do not download file downloaded
    store_file_name = 'second/sample/opendds/versions/' + file_name
    if os.path.isfile(store_file_name):
        print 'already downloaded %s' %store_file_name
        return True
    download_tar_file = open(store_file_name, 'wb')
    block_size = 8192
    while True:
        cache = file_content.read(block_size)
        if not cache:
            break
        download_tar_file.write(cache)
    download_tar_file.close()
    print 'tar zvxf second/sample/opendds/versions/'+ file_name
    print commands.getoutput('tar zxf second/sample/opendds/versions/'+ file_name)
    print 'mv DDS second/sample/opendds/versions/' + file_name.replace(".tar.gz", '')
    print commands.getoutput('mv DDS second/sample/opendds/versions/'+ file_name.replace(".tar.gz", ''))

    return True

def analyze_html(url):
    """
    @ param url\n
    @ return nothing\n
    @ involve fetch html of given url and deal with each href to download tar.gz\n
    """
    # fetch html
    response = urllib2.urlopen(url)
    html = response.read()
    html = html.split("\n")
    target_href_pattern = r'(?:href|HREF)="(OpenDDS-3\.[1-9][0-9]*\.tar\.gz)">'
    # target_href_pattern = r'href="(postfix-\d*\.\d*\.\d*\.tar.gz)"'
    count = 0
    # check html content against git-2.*.tar.gz
    for line in html:
        is_target = re.search(target_href_pattern, line, re.I)
        if is_target:
            file_name = is_target.group(1)
            print 'now downloading %s' %(file_name)
            if download_file(url, file_name):
                count += 1
                print "have downloaded %d:%s" %(count, file_name)

"""
main function
"""
if __name__ == "__main__":
    analyze_html("http://download.ociweb.com/OpenDDS/previous-releases/")
