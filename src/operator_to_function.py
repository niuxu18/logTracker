#-*-coding: utf-8 -*-
import os
import commands
import lxml
import srcml_api
import my_util

def transform_operator(input_dir):
    """
    @ param input dir\n
    @ return nothing\n
    @ involve traverse each cpp like file and transform the << to function call\n
    """
    filenames = []
    # traverse directory for all cpp like while not test like file
    for item in os.walk(input_dir):
        for filename in item[2]:
            # filter by cpp like and not test like
            if my_util.filter_file(filename):
                # concate and store file
                filename = os.path.join(item[0], filename)
                filenames.append(filename)
    
    srcml = srcml_api.SrcmlApi()
    # transform Trace out; out << "a"; out << "c"; to Trace("a", "b")
    index = 0
    total_counts = len(filenames)
    for filename in filenames:
        index += 1
        print "now processing %d / %d, file: %s" %(index, total_counts, filename)
        commands.getoutput("srcml " + filename + " -o test/temp_input.xml" + " > null")
        srcml.parse_xml("test/temp_input.xml")
        srcml.transform_operator()
        # transform source code from temp output file
        commands.getoutput("srcml " + "test/temp_output.xml -S > " + filename + " > null")


def deal_versions(input_dir):
    """
    @ param input dir\n
    @ return nothing\n
    @ involve traverse each cpp like file and transform the << to function call\n
    """
    # traverse directory for all cpp like while not test like file
    for item in os.walk(input_dir):
        for sub_dir in item[1]:
            print 'now processing directory: %s' %sub_dir
            transform_operator(os.path.join(item[0], sub_dir))
        break # only deal with first layer

"""
main function
"""
if __name__ == "__main__":
    deal_versions("second/sample/ice/versions")
