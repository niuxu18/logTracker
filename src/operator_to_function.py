import srcml_api
import os
import my_util
import commands
import lxml

def transfrom_operator(input_dir):
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
    for filename in filenames:
        commands.getoutput("srcml " + filename + " -o test/temp_input.xml")
        srcml.parse_xml("test/temp_input.xml")
        srcml.transform_operator()
        # transform source code from temp output file
        commands.getoutput("srcml " + "test/temp_output.xml -S " + filename)

"""
main function
"""
if __name__ == "__main__":
    transfrom_operator("second/sample/ice/versions/test/")