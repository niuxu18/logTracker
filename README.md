# General introduction: 
LogTracker is a tool which automatically mine log revision rules from software evolution history. It can detect missed log revisions by applying rules.

Entry file is src/logTracker.py.  

Example usage including:  
1 Generating rules  
* python src/logTracker.py -r bftpd -p PATH_TO_BFTPD -g //generate rules  
* `python src/logTracker.py -r bftpd -p demo -g //generate rules`  

2 Applying rules  
* python src/logTracker.py -r bftpd -p PATH_TO_BFTPD -a -v VERSION_NAME //apply rules  
* `python src/logTracker.py -r bftpd -p demo -a -v bftpd-4.9 //apply rules`

# Input and Outputs
1 Output of of this tool is stored in PATH_TO_BFTPD/generate/ and test/ folder.  
The main result files consist of the rule file and the guided log revisions. 

2 Input of LogTracker concludes followings:
* historical versions of the analyzed software: stored in PATH_TO_BFTPD/versions/
* log statements: stored in PATH_TO_BFTPD/, generated by [SMARTLOG](https://github.com/ZhouyangJia/SmartLog)

# Dependency of LogTracker:
1 [GumTree](https://github.com/GumTreeDiff/gumtree) : used to generate syntactical edit scripts (edit scripts of AST), our interface is shown in _gumtree_api.py_.  
Please update the GUMTREE_HOME and JAVA_CLASS_PATH macros in my_constant.py.  
In addition, our java version of gumtree file should be compiled to generate correponding class file. (You may contact us for compiled versions of these libs, our os is ubuntu 14.0).

2 [SrcML](https://www.srcml.org/) : used to analyze the AST of incomplete code snippet, our interface is shown in _srcml_api.py_.  
Please make this command accessable throught command line, you may do this by setting link to the bin file in /usr/bin/.

_Feel free to contact us or leave issues if you have any problems._
