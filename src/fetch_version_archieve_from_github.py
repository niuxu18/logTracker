from pygithub3 import Github
import csv
import sys
import re
import base64
import my_util
import os
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

def download_file(file_url, file_name):
    """
    @ param file url and file name\n
    @ return true if success\n
    @ involve download tar.gz from given url\n
    """
    file_content = urllib2.urlopen(file_url)
    # do not download file downloaded
    store_file_name = 'second/sample/mysql/versions/' + file_name + '.tar.gz'
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

    return True

def fetch_releases():
    """
    @ param  and writer\n
    @ return new counter\n
    @ involve retrive record info of commit [url, date, title, changes, file_name]\n
    """
    # initiate Github with given user and repos 
    gh = Github(login='993273596@qq.com', password='nx153156')
    target_name_pattern = r'(mysql-[0-9\.]*$)'
    tag_pages = gh.repos.list_tags(user='mysql', repo='mysql-server')
    for tag_page in tag_pages:
        for tag in tag_page:
            is_target = re.search(target_name_pattern, tag.name, re.I)
            if is_target:
                print "now start downloading %s" %(tag.name)
                download_file(tag.tarball_url, tag.name)

    # fetch all the commits of given repos
    # commits = gh.repos.commits.list(sha=start_commit)
    # for commit in commits.iterator():
    #     # invoke the deal_commit function
    #     total_counter, counter = analyze_commit(gh, commit.sha, total_counter, counter, writer)
    #     if total_counter % 5 == 0:
    #         print 'now have cawled %d commit, find %d log commit' %(total_counter, counter)


"""
main function
"""
if __name__ == "__main__":
    fetch_releases()