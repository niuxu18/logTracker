#-*-coding: utf-8 -*-
import csv
import sys
import re
import commands
import json
import my_util
import my_constant
from itertools import islice
from itertools import islice
from joern.all import JoernSteps


"""
@ param  string to split words
@ return sub word list
@ callee ...
@ caller maxCommonWord ..
@ involve split string into subwords collection with regrex
@ involve spilter( capital + noncapital / _ / erase word before::)
"""
def splitWordsRe(string):

    word_list = set()

    pattern_name = '[~]?([a-z0-9]*)?([A-Z0-9]*)?((?:[A-Z_][a-z|A-Z]*[0-9]*)*)'
    words = re.match(pattern_name, string)
    if words:
        # upper case and lower case
        for i in range(1, 3):
            word = words.group(i).strip()
            if word != '':
                word_list.add(word.lower())
        # sub string with spliter
        word = words.group(3).strip()
        subwords = re.findall('[A-Z_][a-z]{1,}[0-9]*', word)
        for subword in subwords:
            word_list.add(subword.lower())
        subwords = re.findall('[A-Z_][A-Z]{1,}[0-9]*', word)
        for subword in subwords:
            word_list.add(subword.lower())
    else:
        print "can not anlyze " + string
    if len(word_list) == 0:
        print string

    return word_list

"""
@ param  string to split words
@ return sub word list
@ callee ...
@ caller maxCommonWord ..
@ involve split string into subwords collection with regrex
@ involve spilter( capital or _)
"""
def splitWords(function_name):

    len_str = len(function_name)
    word_list = set()
    start = 0
    # function name that start with _
    if function_name[0] == '_':
        start = 1
    if function_name[0] == '~':
        word_list.add('~')
        start = 1
    for i in range(1, len_str - 1):
        # _
        if function_name[i] == '_':
            # do not add _
            word_list.add(function_name[start:i].lower())
            start = i + 1
            continue
        # capital letter
        if function_name[i] >= 'A' and function_name[i] <= 'Z':
            if (function_name[i + 1] < 'A' or function_name[i + 1] > 'Z') \
            or (function_name[i - 1] < 'A' or function_name[i - 1] > 'Z'):
                word_list.add(function_name[start:i].lower())
                start = i
    # the end
    word_list.add(function_name[start:len_str].lower())
    if '_' in word_list:
        word_list.remove('_')
    if '' in word_list:
        word_list.remove('')

    return word_list

"""
@ param  string a and b to compute
@ return lenth of common subWord / min length
@ callee ...
@ caller computeSim ..
@ involve split string into subwords and compare two word list
"""
def maxCommonWord(string_a, string_b, word_list_dict):
    # split word (collection) <- capital word, _,
    # use dictionary
    if word_list_dict.has_key(string_a):
        word_list_a = word_list_dict.get(string_a)
    else:
        word_list_a = splitWords(string_a)
        word_list_dict[string_a] = word_list_a

    if word_list_dict.has_key(string_b):
        word_list_b = word_list_dict.get(string_b)
    else:
        word_list_b = splitWords(string_b)
        word_list_dict[string_b] = word_list_b

    # get intersection of word_list_a and word_list_b
    len_common = len(word_list_a.intersection(word_list_b))
    if len(word_list_a) == 0 or len(word_list_b) == 0:
        print string_a + "\t," + string_b

    # simlarity value with common length / min length (0, 1)
    # return float(len_common)/min(len(word_list_a), len(word_list_b))
    return float(len_common)*2/(len(word_list_a) + len(word_list_b)), word_list_dict




"""
@ param function a and function b for comparing
@ return similarity value
@ callee maxCommonWord
@ caller getFunctionSimilarity ..
@ involve compute similarity between two function
@ involve function info is list of function name etc.
"""
def computeSim(func_a, func_b, word_list_dict):

    # fetch function name: index 0
    func_name_a = func_a[0]
    func_name_b = func_b[0]

    # similarity between a and b
    return maxCommonWord(func_name_a, func_name_b, word_list_dict)


"""
@ param user, repos
@ return similarity value
@ callee longestCommonStr, maxCommonWord
@ caller computeSimForCluster ..
@ involve compute similarity between two function
@ involve function info is list of function name etc.
"""
def getFunctionSimilarity():

    # initialize write file
    analysis = file(my_constant.FUNC_SIMILAIRTY_FILE_NAME, 'wb')
    analyze_writer = csv.writer(analysis)
    analyze_writer.writerow(['func_a', 'func_b', 'similarity'])

    # initialize python-joern instance
    joern_instance = JoernSteps()
    joern_instance.addStepsDir("/data/joern-code/query/")
    joern_instance.setGraphDbURL("http://localhost:7474/db/data/")
    # connect to database
    joern_instance.connectToDatabase()

    # fetch all function info
    functions_query = '_().getFunctions()'
    functions_temp = joern_instance.runGremlinQuery(functions_query)[0]
    len_func = len(functions_temp)

    # filter some operator reload functions
    functions = []
    for function in functions_temp:
        # remove namespace before::
        function = my_util.removeNamespace(function)
        if function == '':
            continue
        if not function.startswith("operator ") and [function] not in functions:
            functions.append([function])

    len_func = len(functions)
    # compute similarity and write back into file
    func_similarity_dic = {}
    word_list_dict = {}
    for i in range(len_func):
        for j in range(len_func):
            if i == j:
                continue
            similarity, word_list_dict = computeSim(functions[i], functions[j], word_list_dict)
            # store back
            if similarity > 0.5:
                analyze_writer.writerow([functions[i][0], functions[j][0], similarity])
                func_similarity_dic[(functions[i][0], functions[j][0])] = similarity

    # close files
    analysis.close()

    return func_similarity_dic

"""main function"""
if __name__ == "__main__":
    # getFunctionSimilarity( 'data/analyz_function_apple_swift.csv')
    print "main function"