# LogTracker Entry:
src/logTracker.py

# General introduction: 
LogTracker is a tool for automatically mine and learn log revision rules from software evolution history. 
The input includes a dir which store all the released versions.

Example usage including:
* python logTracker.py -r bftpd -p PATH_TO_BFTPD -g //generate rules
* python logTracker.py -r bftpd -p PATH_TO_BFTPD -a -v VERSION_NAME //apply rules

And a logging statement which is generated by Smartlog.

You can contact me or raise an issue if you have some questions.
# Tool dependence(some are in my repository)
	smartlog
	gumtree
	srcml
# Explain:
* fetch data:
	fetch_version... : for crawl version file from given web address
	fetch_hunk: create hunk from versions
	fetch_log: analyze hunk and generate log records
  
* analyze data:
	analyze_...: analyze context
	cluster_...: cluster context and edit feature
