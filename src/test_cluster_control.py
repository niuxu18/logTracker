#-*-coding: utf-8 -*-
import csv
import sys
import re
import commands
import json
from itertools import islice
from z3_api import Z3_api
import analyze_control_clone
import block
import my_util
import my_constant

"""
@ param cond_list a and b for comparing
@ return similarity value
@ callee longestCommonSeq
@ caller computeSimForCluster ..
@ involve compute similarity between cond_lists, unordered common element
"""
def computeSimForContext(context_list_a, context_list_b):
    return my_util.compute_similarity(context_list_a, context_list_b)
"""
@param vec, left, right, similarity, id
@return new cluster
@involve cluster class with children and similarity between children
"""
class mycluster:
    def __init__(self, vec=None, children=None, similarity=0.0, id=None):
        # for drawing picture of clusters
        self.children = children
        # feature vector
        self.vec = vec
        #  id label for locating label
        self.id = id
        self.similarity = similarity


"""
@ param cluster a and b for comparing, similarity_dic, last similarity(1)
@ return similarity value
@ callee computeSim(cond_list_a, cond_list_b); self
@ caller cluster_record ..
@ involve compute similarity between clusters (the least similar cond_list pairs)
"""
def computeSimForCluster(cluster_a, cluster_b, similarity_dic, similarity = 1):

    #  if has record in dictory, then use dictory
    if similarity_dic.get((cluster_a.id, cluster_b.id)) is not None:
        return min(similarity_dic.get((cluster_a.id, cluster_b.id)), similarity)

    # compare cdg_list of entity
    if cluster_a.id >= 0 and cluster_b.id >= 0:
        similarity = min(computeSimForContext(cluster_a.vec, cluster_b.vec), similarity)
        return similarity

    # first cluster (children)
    if cluster_a.id < 0:
        # traverse children
        for child in cluster_a.children:
            similarity = min(computeSimForCluster(child, cluster_b, similarity_dic, similarity), similarity)
        return similarity

    # second cluster (children)
    if cluster_b.id < 0:
        # traverse children
        for child in cluster_b.children:
            similarity = min(computeSimForCluster(cluster_a, child, similarity_dic, similarity), similarity)
        return similarity

"""
@param: cdg_lists(entiry vectors), cluster_similarity = 0.90
@return cluster index for each entity
@caller cluster
@callee computeSimForCluster
@involve: cluster entities based on similarity
"""
def cluster_record(context_lists, cluster_similarity = 0.95):
    # initialize the custers to consist of each entity
    myclusters = [mycluster(children=[], vec=context_lists[i], id=i) for i in range(len(context_lists))]
    flag = None
    currentclusted = -1
    similarity_dic = {}

    # stop clustering based on culster number ( == 1)
    while len(myclusters) > 1:
        # the miniest similarity to merge two cluster
        max_sim = cluster_similarity

        # traverse cluster a and cluster b in clusters
        myclusters_len = len(myclusters)
        for i in range(myclusters_len - 1):
            for j in range(i + 1, myclusters_len):

                # compute similaritys if no record in dictory of similaritys
                if similarity_dic.get((myclusters[i].id, myclusters[j].id)) is None:

                    # compute similaritys by calling computeSim on (vector a, vector b)
                    similarity_dic[(myclusters[i].id, myclusters[j].id)] =\
                        computeSimForCluster(myclusters[i], myclusters[j], similarity_dic)
                    # record symmetrical record
                    similarity_dic[(myclusters[j].id, myclusters[i].id)] =\
                                similarity_dic[(myclusters[i].id, myclusters[j].id)]

                #  fetch the similarity
                similarity = similarity_dic[(myclusters[i].id, myclusters[j].id)]
                # find cluster pair with maxest similarity and flag them
                if similarity > max_sim:
                    max_sim = similarity
                    flag = (i, j)
        # stop clusterring when similarity is too small
        if max_sim == cluster_similarity:
            break
        # combine the two clusters
        mycluster1, mycluster2 = flag
        # create new bicluster(cluster id is minus number)
        new_mycluster = mycluster(children=[], similarity=max_sim, id=currentclusted)
        # children is basic level
        if myclusters[mycluster1].id >= 0:
            new_mycluster.children.append(myclusters[mycluster1])
        else:
            new_mycluster.children.extend(myclusters[mycluster1].children)

        if  myclusters[mycluster2].id >= 0:
            new_mycluster.children.append(myclusters[mycluster2])
        else:
            new_mycluster.children.extend(myclusters[mycluster2].children)
        currentclusted -= 1
        # remove old cluster from the clusters
        # have not destroy it
        del myclusters[mycluster2]
        del myclusters[mycluster1]
        myclusters.append(new_mycluster)
        print len(myclusters)

    # compute cluster_lists based on clusters and cluster number
    cluster_lists = [0 for i in range(len(context_lists))]
    index = 0
    for now_cluster in myclusters:
        if now_cluster.id < 0:
            # traverse children
            for child in now_cluster.children:
                cluster_lists[child.id] = index
        else:
            cluster_lists[now_cluster.id] = index
        index += 1
    return cluster_lists

"""
@ param  user and repos
@ return nothing
@ caller main
@ callee cluster_record
@ involve read from and write back to files
"""
def cluster():

    # initialize read file
    analyze_control = file(my_constant.ANALYZE_REPOS_JOERN_FILE_NAME, 'rb')
    records = csv.reader(analyze_control)
    # initialize write file
    cluster_control = file(my_constant.CLUSTER_REPOS_FILE_NAME, 'wb')
    cluster_control_writer = csv.writer(cluster_control)
    cluster_control_writer.writerow(my_constant.CLUSTER_REPOS_TITLE)

    context_lists = []
    # traverse the fetch csv file to record cond_lists of each log statement to cdg_lists
    for record in islice(records, 1, None):  # remove the table title
        # store cond_lists(index 6)
        cdg_list = json.loads(record[my_constant.ANALYZE_REPOS_CDG_Z3_FEATURE])
        context_lists.append(cdg_list)

    # cluster log statement based on cdg_list and ddg_list
    # cluster_lists = context_lists
    cluster_lists = cluster_record(context_lists, 0.95)
    # record cluster index of each log statement
    analyze_control.close()
    analyze_control = file(my_constant.ANALYZE_REPOS_JOERN_FILE_NAME, 'rb')
    records = csv.reader(analyze_control)
    index = 0
    for record in islice(records, 1, None):
        record.append(cluster_lists[index])
        cluster_control_writer.writerow(record)
        index += 1

    # my_util.dumpSimilarityDic(similarity_dict)
    # close files
    cluster_control.close()
    analyze_control.close()

"""
main function
"""
if __name__ == "__main__":

    cluster()