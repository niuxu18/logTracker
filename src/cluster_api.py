#-*-coding: utf-8 -*-
import csv
import sys
import re
import commands
import json
from itertools import islice
import analyze_control_clone
import my_util
import my_constant


class mycluster:
    def __init__(self, vec=None, children=None, similarity=0.0, id=None):
        """
        @param vec, children, similarity, id\n
        @return new cluster\n
        @involve cluster class with children and similarity between children\n
        """
        # for drawing picture of clusters
        self.children = children
        # feature vector
        self.vec = vec
        #  id label for locating label
        self.id = id
        self.similarity = similarity

def compute_equality(vec_a, vec_b):
    """
    @ param vector a and b for comparing, z3 api\n
    @ return true if equal\n
    @ involve compute equality between vectors, use z3 or just ==\n
    """
    return vec_a == vec_b

def compute_similarity_for_cluster(cluster_a, cluster_b, similarity_dic, similarity=1):
    """
    @ param cluster a and b for comparing, similarity_dic, current min similarity(1)\n
    @ return similarity value\n
    @ involve compute similarity between clusters (the least similar pairs)\n
    """
    #  if has record in dictory, then use dictory
    if similarity_dic.get((cluster_a.id, cluster_b.id)) is not None:
        return min(similarity_dic.get((cluster_a.id, cluster_b.id)), similarity)

    # compare cdg_list of entity
    if cluster_a.id >= 0 and cluster_b.id >= 0:
        similarity = min(my_util.compute_similarity(cluster_a.vec, cluster_b.vec), similarity)
        return similarity

    # first cluster (children)
    if cluster_a.id < 0:
        # traverse children
        for child in cluster_a.children:
            similarity = min(compute_similarity_for_cluster(child, cluster_b, similarity_dic, similarity), similarity)
        return similarity

    # second cluster (children)
    if cluster_b.id < 0:
        # traverse children
        for child in cluster_b.children:
            similarity = min(compute_similarity_for_cluster(cluster_a, child, similarity_dic, similarity), similarity)
        return similarity

def cluster_record_with_similarity(feature_lists, cluster_similarity=0.95):
    """
    @param: feature lists(entiry vectors), miniest similarity to cluster(0.95)\n
    @return cluster index for each entity(same order as feature list)\n
    @involve: cluster entities based on similarity threshold\n
    """
    # initialize the custers to consist of each entity
    myclusters = [mycluster(children=[], vec=feature_lists[i], id=i) for i in range(len(feature_lists))]
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
                        compute_similarity_for_cluster(myclusters[i], myclusters[j], similarity_dic)
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
        mycluster1, mycluster2 = myclusters[flag[0]], myclusters[flag[1]]
        # create new bicluster(cluster id is minus number)
        new_mycluster = mycluster(children=[], id=currentclusted)
        # children is basic level
        if mycluster1.id >= 0:
            new_mycluster.children.append(mycluster1)
        else:
            new_mycluster.children.extend(mycluster1.children)
        if  mycluster2.id >= 0:
            new_mycluster.children.append(mycluster2)
        else:
            new_mycluster.children.extend(mycluster2.children)
        currentclusted -= 1
        # remove old cluster from the clusters
        del myclusters[flag[1]]
        del myclusters[flag[0]]
        myclusters.append(new_mycluster)
        print len(myclusters)

    # compute cluster_lists based on clusters and cluster number
    cluster_lists = [0 for i in range(len(feature_lists))]
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

def compute_equality_for_cluster(cluster_a, cluster_b, similarity_dic):
    """
    @ param cluster a and b for comparing, similarity_dic\n
    @ return true if equal\n
    @ involve compute equality between clusters (equality of any sub entity)\n
    """
    #  if has record in dictory, then use dictory
    if similarity_dic.get((cluster_a.id, cluster_b.id)) is not None:
        return similarity_dic.get((cluster_a.id, cluster_b.id))

    # compare cdg_list of entity
    if cluster_a.id >= 0 and cluster_b.id >= 0:
        return compute_equality(cluster_a.vec, cluster_b.vec)


    # first cluster (children)
    if cluster_a.id < 0:
        # first child
        return compute_equality_for_cluster(cluster_a.children[0], cluster_b, similarity_dic)

    # second cluster (children)
    if cluster_b.id < 0:
        # first child
        return compute_equality_for_cluster(cluster_a, cluster_b.children[0], similarity_dic)

def cluster_record_with_equality(feature_lists):
    """
    @param: feature lists\n
    @return cluster index for each entity\n
    @involve: cluster entities based on equality(true/false)\n
    """
    # initialize the custers to consist of each entity
    myclusters = [mycluster(children=[], vec=feature_lists[i], id=i) for i in range(len(feature_lists))]
    flag = None
    currentclusted = -1
    similarity_dic = {}

    # stop clustering based on culster number ( == 1)
    while len(myclusters) > 1:

        # traverse cluster a and cluster b in clusters
        myclusters_len = len(myclusters)
        for i in range(myclusters_len - 1):
            for j in range(i + 1, myclusters_len):

                # compute similaritys if no record in dictory of similaritys
                if similarity_dic.get((myclusters[i].id, myclusters[j].id)) is None:

                    # compute similaritys by calling computeSim on (vector a, vector b)
                    similarity_dic[(myclusters[i].id, myclusters[j].id)] =\
                        compute_equality_for_cluster(myclusters[i], myclusters[j], similarity_dic)
                    # record symmetrical record
                    similarity_dic[(myclusters[j].id, myclusters[i].id)] =\
                                similarity_dic[(myclusters[i].id, myclusters[j].id)]

                #  fetch the similarity
                similarity = similarity_dic[(myclusters[i].id, myclusters[j].id)]
                # find cluster pair with maxest similarity and flag them
                if similarity:
                    flag = (i, j)
                    break
            if similarity:
                break
        if not similarity:
            break
        # combine the two clusters
        mycluster1, mycluster2 = myclusters[flag[0]], myclusters[flag[1]]
        # create new bicluster(cluster id is minus number)
        new_mycluster = mycluster(children=[], id=currentclusted)
        # children is basic level
        if mycluster1.id >= 0:
            new_mycluster.children.append(mycluster1)
        else:
            new_mycluster.children.extend(mycluster1.children)
        if  mycluster2.id >= 0:
            new_mycluster.children.append(mycluster2)
        else:
            new_mycluster.children.extend(mycluster2.children)
        currentclusted -= 1
        # remove unused dict
        for sub_cluster1 in mycluster1.children:
            for sub_cluster2 in mycluster2.children:
                similarity_dic.pop(sub_cluster1.id, sub_cluster2.id)
                similarity_dic.pop(sub_cluster2.id, sub_cluster1.id)
        similarity_dic.pop(mycluster1.id, mycluster2.id)
        similarity_dic.pop(mycluster2.id, mycluster1.id)
        # remove old cluster from the clusters
        del myclusters[flag[1]]
        del myclusters[flag[0]]
        myclusters.append(new_mycluster)
        print len(myclusters)

    # compute cluster_lists based on clusters and cluster number
    cluster_lists = [0 for i in range(len(feature_lists))]
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


def cluster_record_with_equality_mine(feature_lists):
    """
    @param: feature lists\n
    @return cluster index for each entity\n
    @involve: split feature lists into equivalent cluster\n
    """
    num_item = len(feature_lists)
    past_item = []
    clusters = []
    for i in range(num_item - 1):
        # equality is transitive
        if i in past_item:
            continue
        # add i to this cluster
        clusters.append([i])
        print 'now processing item %d/%d' %(len(past_item), num_item)
        past_item.append(i)
        for j in range(i + 1, num_item):
            # equality is transitive
            if j in past_item:
                continue
            # find new euqivilent element, then add to this cluster
            if feature_lists[i] == feature_lists[j]:
                clusters[-1].append(j)
                past_item.append(j)

    # deal with last element
    i = num_item - 1
    if i not in past_item:
        clusters.append([i])
        past_item.append(i)
    
    # sort clusters by size -> largest size with largest index number
    clusters.sort(key=lambda x:len(x))
    # compute cluster_indexes based on clusters and cluster number
    cluster_indexes = [0 for i in range(len(feature_lists))]
    index = 0
    for cluster in clusters:
        for item in cluster:
            cluster_indexes[item] = index
        index += 1
    return cluster_indexes

def generate_class_from_cluster(cluster_file_name, class_file_name, cluster_title, class_title, min_frequence=2):
    """
    @param: cluster file name and class file name, cluster and class title, min occurrence time\n
    @return nothing\n
    @involve: generate class(repos)/rule(patch) from cluster, keep one records for repeted cluster\n
    """
    # decrease min frequence, since tell before record
    min_frequence -= 1
    # initiate csv file
    cluster_file = file(cluster_file_name, 'rb')
    records = csv.reader(cluster_file)
    class_file = file(class_file_name,'wb')
    writer = csv.writer(class_file)
    writer.writerow(class_title)
    # traverse records to build class
    cluster_size = {}
    class_records = []
    for record in islice(records, 1, None):
        # last column is cluster index
        cluster_index = record[-1]
        # initialize cluster frequence item
        if not cluster_size.has_key(cluster_index):
            cluster_size[cluster_index] = 0
        # tell whether this occurence satisfies min frequence
        if cluster_size[cluster_index] == min_frequence:
            # retrieve feature from feature index list
            feature_records = []
            for feature_title in class_title[2:]:
                feature_records.append(record[cluster_title.index(feature_title)])
            # build and store class record
            class_record = [cluster_index] + feature_records
            class_records.append(class_record)
            # record this occurence
            cluster_size[cluster_index] += 1
        # record this occurence
        else:
            cluster_size[cluster_index] += 1

    for class_record in class_records:
        cluster_index = class_record[0]
        # insert class size
        class_record.insert(1, cluster_size[cluster_index])
        writer.writerow(class_record)

    # close file
    cluster_file.close()
    class_file.close()


def generate_records_for_class(cluster_file_name, class_index):
    """
    @param: cluster file name and class index\n
    @return records\n
    @involve: generate records for given class index(query cluster file)\n
    """
    results = []
    # initiate csv file
    cluster_file = file(cluster_file_name, 'rb')
    records = csv.reader(cluster_file)
    for record in islice(records, 1, None):
        cluster_index = record[-1]
        if cluster_index == class_index:
            results.append(record)

    cluster_file.close()
    return results

"""
main function
"""
if __name__ == "__main__":

    cluster_record_with_similarity([])
