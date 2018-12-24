package gumtree;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

import com.github.gumtreediff.actions.ActionGenerator;
import com.github.gumtreediff.actions.model.Action;
import com.github.gumtreediff.actions.model.Addition;
import com.github.gumtreediff.actions.model.Delete;
import com.github.gumtreediff.actions.model.Insert;
import com.github.gumtreediff.actions.model.Move;
import com.github.gumtreediff.actions.model.Update;
import com.github.gumtreediff.client.Run;
import com.github.gumtreediff.gen.Generators;
import com.github.gumtreediff.matchers.Mapping;
import com.github.gumtreediff.matchers.MappingStore;
import com.github.gumtreediff.matchers.Matcher;
import com.github.gumtreediff.matchers.Matchers;
import com.github.gumtreediff.tree.ITree;
import com.github.gumtreediff.tree.TreeContext;

import java.io.LineNumberReader;

public class GumTreeApi {
	private String oldFile, newFile;
	private TreeContext oldTreeContext, newTreeContext;
	private ITree oldTree, newTree;
	private Matcher matcher;
	private ActionGenerator actionGenerator;
	private MappingStore mappings;
	private List<Action> actions;
	// application specific info for compare two file
	private int oldLoc, newLoc;
	private ITree oldLogNode, newLogNode;
	private List<ITree> oldLogs, newLogs, mappedOldLogs, ddgNodes;
	private boolean ddgFlag;
//	have not modify this log
	final int IS_LOG = 1;
	final int IS_LOGS = 2;
	final int IS_FEATURE = 4;
//	final String COMMENT_TYPE = "comment";
//	final String BLOCK_TYPE = "block";
	final String IF_TYPE = "if";
	final String NEW_MARK = "%%";
	final String OLD_MARK = "@@";
	// application specific info for " analyze file "
	private int loc;
	private int functionLoc;
	private ITree tree;
	private ITree logNode;
	private TreeContext treeContext;
	private String filename;
	// application specific info for " match old and repos according to old and new"
	private List<ITree> editedNodes;
	

	public void setOldAndNewFile(String oldFile, String newFile) {
		Run.initGenerators();
		try {
			this.oldFile = oldFile;
			this.newFile = newFile;
			// initialize treeContext and iTree
			oldTreeContext = Generators.getInstance().getTree(this.oldFile);
			newTreeContext = Generators.getInstance().getTree(this.newFile);
			oldTree = oldTreeContext.getRoot();
			newTree = newTreeContext.getRoot();
			// initialize matcher and actions
			this.getActions();
			// initialize application specific info
			oldLogs = new ArrayList<ITree>();
			newLogs = new ArrayList<ITree>();
			mappedOldLogs = new ArrayList<ITree>();
			ddgNodes = new ArrayList<ITree>();
			editedNodes = new ArrayList<ITree>(); 
		} catch (Exception e) {
			// e.printStackTrace();
			System.out.println(e.toString());
			System.out.printf("oldFile: %s, newFile: %s \n", oldFile, newFile);
		}
	}

	public void setOldAndNewFile() {
		String oldFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/gumtree/c/old.cpp";
		String newFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/gumtree/c/new.cpp";
		this.setOldAndNewFile(oldFile, newFile);
	}

	public static void main(String args[]) {
		// System.out.println("hello I am gumtree api");
		
//		 String counter = "1059";
//		 String oldFile =
//		 "/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/CMake/CMake-old-new/CMake-old-new-joern/Kitware_CMake_old_new_old_function_" + counter + ".cpp";
//		 String newFile =
//		 "/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/CMake/CMake-old-new/CMake-old-new-joern/Kitware_CMake_old_new_new_function_" + counter + ".cpp";
//		 GumTreeApi g = new GumTreeApi();
//		 g.setOldAndNewFile(newFile, oldFile);
//		 g.addDDGNode(304);
//		 g.addDDGNode(301);
//		 g.addDDGNode(302);
//		 g.addDDGNode(303);
//		 g.addDDGNode(5);
//		 g.addDDGNode(6);
//		 System.out.println(g.isDDGModified());
//		 Iterator<String[]> iter = g.getWordEdit().iterator();
//		 while(iter.hasNext())
//		 {
//			 String edit_element[] = iter.next();
//			 System.out.printf("(%s, %s)\n", edit_element[0], edit_element[1]);
//		 }
		
//		String filename = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/git/repos/git-2.9.5/config.c";
//		String filename = "/usr/info/code/cpp/LogMonitor/LogMonitor/clang/hello.cpp";
//					
//		String oldFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/git/repos/git-2.0.0/builtin/blame.c";
//		String newFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/git/repos/git-2.0.1/builtin/blame.c";
//		GumTreeApi g = new GumTreeApi();
//		g.setOldAndNewFile(oldFile, newFile);
//		g.setFile(filename);
//		g.setLoc(73);
//		System.out.println(g.getLog());
//		g.printSpliter();
//		System.out.println(g.getBlock());
//		g.printSpliter();
//		System.out.println(g.getControl());
//		g.printSpliter();
//		System.out.println(g.getFunction());
//		g.printSpliter();
//		System.out.println(g.getFunctionLoc());
		
//		String oldFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/httpd/gumtree/httpd_old_hunk_57.cpp";
//		String newFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/download/httpd/gumtree/httpd_new_hunk_57.cpp";
//		GumTreeApi g = new GumTreeApi();
//		g.setOldAndNewFile(oldFile, newFile);
//		g.addNewLogNode(5);		
//		g.addNewLogNode(31);
//		g.addOldLogNode(5);
//		g.setOldLoc(119);
//		System.out.println(g.getNewLoc());
//		g.setNewLoc(5);
//		System.out.println(g.getOldLog());
//		System.out.println(g.getActionType());
		
//		
		GumTreeApi g = new GumTreeApi();
//		String fileName = "/usr/info/code/cpp/LogMonitor/LogMonitor/"
//				+ "second/sample/wget/generate/gumtree/temp.cpp";
//		g.setFile(fileName);
//		if(g.setLoc(449))
//		{
//			System.out.println(g.getLog());
//			System.out.println(g.getFunction());
//		}
//		String oldFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/gumtree/c/old.cpp";
//		String newFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/gumtree/c/new.cpp";
		String oldFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/ice/generate/gumtree/ice_old_hunk_1.cpp";
		String newFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/sample/ice/generate/gumtree/ice_new_hunk_1.cpp";
//		String candidateFile = "/usr/info/code/cpp/LogMonitor/LogMonitor/second/gumtree/c/candidate.cpp";
		g.setOldAndNewFile(oldFile, newFile);
		g.setDDGFlag(true);
		g.addDDGNode(-1);
		g.addDDGNode(14);
		System.out.println(g.isDDGModified());
		//g.recommendSyntacticalEdit(oldFile, newFile, candidateFile);
		
//		g.addOldLogNode(2);
////		g.addNewLogNode(2);
//		g.setOldLoc(2);
//		System.out.println(g.getOldLog());
//		System.out.println(g.getNewLog());	
//		System.out.println(g.getActionType());
//		System.out.println(g.isOldLogEdited());
//		System.out.println(g.isLogCheckDeleted());
//		Set<String> edits = g.getLogEditType();
//		// show result
//		g.printSpliter();
//		Iterator<String> editIter = edits.iterator();
//		while(editIter.hasNext())
//		{
//			System.out.println(editIter.next());
//		}
	}

	public boolean setOldLoc(int oldLoc) {
		this.oldLoc = oldLoc;
		this.oldLogNode = getLogNodeOfLine(this.oldLoc, this.oldTree, this.oldTreeContext, this.oldFile);
		// commented line
		if (oldLogNode == null) {
			System.out.printf("line: %d in file: %s no node found\n", this.oldLoc, this.oldFile);
			return false;
		}
		
//		printNode(this.oldLogNode, this.oldTreeContext, this.oldFile);
		this.newLogNode = mappings.getDst(this.oldLogNode);
		return true;
	}
	
	public boolean setNewLoc(int newLoc) {
		this.newLoc = newLoc;
		this.newLogNode = getLogNodeOfLine(this.newLoc, this.newTree, this.newTreeContext, this.newFile);
		// commented line
		if (newLogNode == null) {
			System.out.printf("line: %d in file: %s no node found\n", this.newLoc, this.newFile);
			return false;
		}
		
		return true;
//		printNode(this.oldLogNode, this.oldTreeContext, this.oldFile);
//		this.oldLogNode = mappings.getDst(this.newLogNode);
//		return true;
	}

//	get inserted old loc for the inserted log node
	public int getOldLoc() {
		Iterator<Action> actionIter = this.actions.iterator();
		Action currAction;
		while(actionIter.hasNext())
		{
			currAction = actionIter.next();
			if(currAction.getName().equals("INS") && this.isChildrenOf(this.newLogNode, currAction.getNode()))
			{
//				pos: 0 -> size ==> 0 -> size - 1
				ITree parentNode = ((Insert)currAction).getParent();
				if(this.isChildrenOf(parentNode, this.oldTree))
				{
					int pos = ((Insert)currAction).getPosition();
//					System.out.println(getValue(parentNode, this.oldFile));
//					System.out.println(pos);
					int maxPos = parentNode.getChildren().size() - 1;
					if(maxPos == -1)
					{
						continue;
					}
					pos = pos > maxPos ? maxPos : pos;
					ITree oldNode = parentNode.getChild(pos);

					return this.getLineNumber(oldNode, this.oldFile, true) - 1;
				}
			}
			
		}
		
		return -1;
	}
	

	// get mapping new log loc for old loc
	public int getNewLoc() {
		// delete
		if (this.newLogNode == null)
			return -1;
		else
			return getLineNumber(this.newLogNode, this.newFile, true) - 1;
	}


	public String getOldLog() {
		return getValue(this.oldLogNode, this.oldFile);
	}

	public String getNewLog() {
		if (this.newLogNode == null)
			return null;
		else
			return getValue(this.newLogNode, this.newFile);
	}
	
	public void addOldLogNode(int line) {
		ITree logNode = this.getLogNodeOfLine(line, this.oldTree, this.oldTreeContext, this.oldFile);
		if (logNode != null)
			this.oldLogs.add(logNode);
	}
	
	public void addNewLogNode(int line) {
		ITree logNode = this.getLogNodeOfLine(line, this.newTree, this.newTreeContext, this.newFile);
		if (logNode != null)
		{
			this.newLogs.add(logNode);
			ITree mappedLogNode = this.mappings.getSrc(logNode);
			if(mappedLogNode != null)
				this.mappedOldLogs.add(mappedLogNode);
		}
	}
	
	public void setDDGFlag(boolean isNewHunk)
	{
		// true if is in new hunk
		this.ddgFlag = isNewHunk;
		// if new hunk, swap the old and new file
		if(this.ddgFlag)
		{
			this.setOldAndNewFile(this.newFile, this.oldFile);
		}
	}

	public void addDDGNode(int line) {
		ITree ddgNode;
		ddgNode = this.getDDGNodeOfLine(line, this.oldTree, this.oldTreeContext, this.oldFile);
		if (ddgNode != null)
			this.ddgNodes.add(ddgNode);
	}
	
	// judge edition type based on ddg locations
	public boolean isDDGModified() {
		// no need to check for null ddgs
		if(this.ddgNodes.size() == 0)
			return false;
	
		Iterator<Action> actionIter = actions.iterator();
		Action action;
		ITree tempNode;
		while (actionIter.hasNext()) {
			action = actionIter.next();
			// do not deal with comment modification
			if(this.isActionOfComment(action))
			{
				continue;
			}
			// do not analyze move
			String actionType = action.getName();
			if(actionType.equals("MOV"))
			{
				continue;
			}
		 	// judge if leaf edition is edition of logs
			tempNode = actionType.equals("INS") ? ((Insert)action).getParent() : action.getNode();
			// decide whether is edition on ddgs in(old file[new function]) delete/update
			Iterator<ITree> ddgIter = this.ddgNodes.iterator();
			while (ddgIter.hasNext()) {
				// edited part is children of ddgNodes
				if (isChildrenOf(tempNode, ddgIter.next())) {
					return true;
				}
			}
		}
		return false;
	}
	
	// decide whether check of old log is modified
	public boolean isLogCheckDeleted()
	{
		// get check of old log
		ITree controlNode = this.getControl(this.oldLogNode, this.oldTreeContext);
		// tell whether check is deleted
		if(controlNode != null && this.isNodeDelete(controlNode))
		{
			return true;
		}
		return false;
	}
	
	// decide whether check of new log is modified
	public boolean isLogCheckInserted()
	{
		// get check of old log
		ITree conditionNode = this.getCondition(this.newLogNode, this.newTreeContext);
		// tell whether check is deleted
		if(conditionNode != null && this.isNodeInsert(conditionNode))
		{
			return true;
		}
		return false;
	}
	
	public int isOldLogEdited()
	{
		Iterator<Action> actionIter = this.actions.iterator();
		Action currAction;
		ITree oldNode;
		while(actionIter.hasNext())
		{
			currAction = actionIter.next();
			if(!this.isActionOfComment(currAction))
			{
				oldNode = currAction.getName().equals("INS") ? ((Insert)currAction).getParent() : currAction.getNode();
				if(this.isChildrenOf(oldNode, this.oldLogNode))
				{
					return this.IS_LOG;
				}
			}
		}
		
		return 0;
	}
	
	// judge edition type based on oldLogs and newLogs(mapped old logs)
	public int getActionType() {
		int isLogs = 0;
		int isFeature = 0;
		
		Iterator<Action> actionIter = actions.iterator();
		Action action;
		ITree tempNode;
		boolean isIdentified;
//			printNode(this.oldLogNode, this.oldTreeContext, this.oldFile);
		while (actionIter.hasNext() && (isFeature == 0 || isLogs == 0)) {
			action = actionIter.next();
			// do not deal with comment modification
			if(this.isActionOfComment(action))
			{
				continue;
			}
//	 		judge if leaf edition is edition of logs
			tempNode = action.getName().equals("INS") ? ((Insert)action).getParent() : action.getNode();
			isIdentified = false;
//			decide whether is edition on old logs
			Iterator<ITree> logIter = this.oldLogs.iterator();
			while (logIter.hasNext()) {
				if (isChildrenOf(tempNode, logIter.next())) {
					isLogs = this.IS_LOGS;
					isIdentified = true;
					break;
				}
			}
//			decide whether insertion of new logs
			if(!isIdentified && (isFeature == 0 || isLogs == 0))
			{

//				decide whether is edition on false recognized new log
				logIter = this.mappedOldLogs.iterator();
				while (logIter.hasNext()) {
					if (isChildrenOf(tempNode, logIter.next())) {
						isLogs = this.IS_LOGS;
						isIdentified = true;
						break;
					}
				}
				if(this.isInsertionOfLog(action))
				{
					isLogs = this.IS_LOGS;
					isIdentified = true;
				}
//				then feature if neither edition on old logs nor insertion of new logs 
				else
				{
					isFeature = this.IS_FEATURE;
				}
			} 
		}
		
		return (isLogs + isFeature);
	}


	public void setFile(String filename) {
		Run.initGenerators();
		try {
			this.filename = filename;
			// initialize treeContext and iTree
			this.treeContext = Generators.getInstance().getTree(this.filename);
			this.tree = this.treeContext.getRoot();
		} catch (Exception e) {
			// e.printStackTrace();
			System.out.println(e.toString());
			System.out.printf("filename: %s\n", filename);

		}
	}

	public boolean setLoc(int line) {
		this.loc = line;
		this.logNode = getLogNodeOfLine(this.loc, this.tree, this.treeContext, this.filename);
		// commented line
		if (this.logNode == null) {
			System.out.printf("line: %d in file: %s no node found\n", this.loc, this.filename);
			return false;
		}
		
		return true;
	}

	public String getLog() {
		return getValue(this.logNode, this.filename);
	}

	protected String getBlock(){
		// first parent that contains block type
		ITree parentNode = this.logNode.getParent();
		while(parentNode != null)
		{
//			printNode(parentNode, this.treeContext, this.filename);
			if(!this.isBlock(parentNode, this.treeContext, this.filename))
			{
				parentNode = parentNode.getParent();
			}
			else
			{
				return getValue(parentNode, this.filename);
			}
		}
		
		return "";
	}
	
	// get check of givne node
	protected ITree getControl(ITree node, TreeContext treeContext){
		// first parent that contains block type
		ITree parentNode = node.getParent();
		ITree controlNode = null;
		while(parentNode != null)
		{
			if(this.isControl(parentNode, treeContext))
			{
				controlNode = parentNode;
				break;
			}
			parentNode = parentNode.getParent();
		}
		return controlNode;
	}
	
	// get condition of given node( first child of control node)
	protected ITree getCondition(ITree node, TreeContext treeContext){
		ITree controlNode = getControl(node, treeContext);
		return controlNode.getChild(0);
	}
	
	public String getFunction(){
		// parent that has function type
		ITree parentNode = this.logNode.getParent();
		while(parentNode != null)
		{
			if(!this.isFunction(parentNode, this.treeContext, this.filename))
			{
				parentNode = parentNode.getParent();
			}
			else
			{
				this.functionLoc = getLineNumber(parentNode.getChild(1), this.filename, true) - 1;
//				System.out.println(this.getValue(parentNode.getChild(1), this.filename));
				return getValue(parentNode, this.filename);
			}
		}
		
		System.out.printf("WARN: can not get function for node in file: %s, line %d\n", this.filename, this.loc);
		this.functionLoc = -1;
		return "";
	}
	
	public int getFunctionLoc(){
		// log loc - function loc = log loc in function [index from 0]
//		System.out.println(this.functionLoc);
		return this.loc - this.functionLoc;
	}
	
	private final List<String> AST_TYPE = Arrays.asList(
			"if",
			"while",
			"for",
			"do",
			"break",
			"continue",
			"return",
			"switch",
			"case",
			"default",
			"block",
			"label",
			"goto",
			"empty_stmt",
			"specifier",
			"name",
			"extern",
			"friend",
			"decl_stmt",
			"decl",
			"function_decl",
			"function",
			"init",
			"literal",
			"lambda",
			"namespace",
			"using",
			"typedef",
			"modifier",
			"range",
			"call",
			"class",
			"class_decl",
			"super",
			"public",
			"private",
			"protected",
			"constructor",
			"constructor_decl",
			"destructor",
			"destructor_decl",
			"struct_decl",
			"struct",
			"union_decl",
			"union",
			"enum",
			"operator",
			"ternary",
			"expr",
			"cast",
			"assert",
			"sizeof",
			"typeid",
			"noexcept",
			"alignof",
			"alignas",
			"decltype",
			"attribute",
			"asm",
			"template",
			"parameter_list",
			"typename",
			"throw",
			"try",
			"catch",
			"type",
			"capture",
			"index",
			"member_list",
			"condition",
			"then",
			"else",
			"operator",
			"argument_list",
			"parameter",
			"param",
			"expr_stmt",
			"elseif",
			"argument",
			"directive",
			"incr",
			"value",
			"macro",
			"control",
			"value");
	private final List<String> AST_EXCEPT_TYPE = Arrays.asList
			("endif",
			"ifdef",
			"elif",
			"comment",
			"warning",
			"file",
			"include",
			"ifndef",
			"define");
	
	// syntax feature of block file 
	protected String getBlockFeature()
	{
		int ast_type_num = this.AST_TYPE.size();
		Integer[] frequence = new Integer[ast_type_num];
		for(int i = 0; i < ast_type_num; i++)
		{
			frequence[i] = 0;
		}
		// traverse all nodes to count frequence vector
		Iterator<ITree> allNodesIter = this.tree.getDescendants().iterator();
		String tempType;
		int index;
		while(allNodesIter.hasNext())
		{
			tempType = getType(allNodesIter.next(), this.treeContext);
//			System.out.printf("type: %s\n", tempType);

			index = this.AST_TYPE.indexOf(tempType);
			if(index != -1)
			{
				frequence[index] += 1;
			}
			else if(this.AST_EXCEPT_TYPE.indexOf(tempType) == -1)
			{
				System.out.printf("type: %s can not be found\n", tempType);
			}
		}
		
		return Arrays.asList(frequence).toString();
	}
	
	protected String getBlockType()
	{
		String type = "";
		Iterator<ITree> allNodesIter = this.tree.postOrder().iterator();
		ITree currNode;
		while(allNodesIter.hasNext())
		{
			currNode = allNodesIter.next();
			type += getType(currNode, this.treeContext);
			if(this.treeContext.getTypeLabel(currNode).equals("argument"))
			{
				type += "\n";
			}
			else
			{
				type += "****";
			}
		}
		
		return type;
	}

	// old file: old log file(mainly)
	// new file: new log file(mainly)
	// candidate file: candidate log file
	// edit: add/insert/delete/remove
	public String recommendSyntacticalEdit(String oldLogFile, String newLogFile, String candidateLogFile)
	{
		// save actions between old and new log file
		this.setOldAndNewFile(oldLogFile, newLogFile);
		List<Action> historyActions = new ArrayList<Action>();
		for(int i = 0; i < this.actions.size(); i++)
		{
			historyActions.add(this.actions.get(i));
		}
		MappingStore historyMap = this.mappings.copy();
		TreeContext historyTreeContext = this.newTreeContext;
		// generate maps between old and candidate log file
		this.setNewFile(candidateLogFile);
		
		// recommend syntactical edits for candidate log file
		Iterator<Action> actionIter = historyActions.iterator();
		Action currAction;
		ITree currNode;
		String output = "";
		while(actionIter.hasNext())
		{
			// mov, del and update: old tree context and old file
			currAction = actionIter.next();
			// just deal with leaf node
			currNode = currAction.getNode();
			if(isActionOfComment(currAction, historyTreeContext, newLogFile))
				continue;
			if(!currNode.isLeaf() && currAction.getName() != "MOV")
			{
				continue;
			}
			// action type -> prefix
			switch(currAction.getName())
			{
			case "INS":
				Insert insertAction = (Insert)currAction;
				output += "add\t" + NEW_MARK;
//				new node
				output += this.getPrettyString(insertAction.getNode(), historyTreeContext, newLogFile);
				output += NEW_MARK + "\tin\t";
//				old node
				ITree parentNode = insertAction.getParent();
				ITree oldNode = historyMap.getSrc(parentNode);
				while(parentNode != null && oldNode == null)
				{
					parentNode = parentNode.getParent();
					oldNode = historyMap.getSrc(parentNode);
				}
				output += this.getPrettyString(this.mappings.getDst(oldNode), this.newTreeContext, this.newFile);
				break;
			case "DEL":
				output += "remove\t";
				Delete deleteAction = (Delete)currAction;
				// old node
				output += this.getPrettyString(this.mappings.getDst(deleteAction.getNode()), this.newTreeContext, this.newFile);
				output += "\tfrom\t";
				// parent
				output += this.getPrettyString(this.mappings.getDst(deleteAction.getNode().getParent()), this.newTreeContext, this.newFile);
				break;
			case "UPD":
				output += "update\t";
				Update updateAction = (Update)currAction;
				// old node
				boolean a = this.mappings.hasSrc(updateAction.getNode());
				output += this.getPrettyString(this.mappings.getDst(updateAction.getNode()), this.newTreeContext, this.newFile);
				// new value
				output += "\tto\t" + NEW_MARK;
				output += this.getType(updateAction.getNode(), this.oldTreeContext);
				output += ": ";
				output += updateAction.getValue().replace("\n", "") + NEW_MARK;
				break;
			case "MO3156"
					+ "V":
				output += "move\t";
				Move moveAction = (Move)currAction;
				// old node
				output += this.getPrettyString(this.mappings.getDst(moveAction.getNode()), this.newTreeContext, this.newFile);
				// old parent
				output += "\tfrom\t";
				output += this.getPrettyString(this.mappings.getDst(moveAction.getParent()), this.newTreeContext, this.newFile);
//				System.out.printf("WARN: DO NOT DEAL WITH MOVE in %s: %d\n", this.oldFile, this.oldLoc);
				break;
			}
			
			output += "\n";
		}
		
//		System.out.printf("%s", output);
		return output;
	}
	
	// old file: old log file(mainly)
	// new file: new log file(mainly)
	// edit: add/insert/delete/remove
	public String getSyntacticalEditWithSymbol()
	{
		MappingStore historyMap = this.mappings.copy();
		
		// recommend syntactical edits for candidate log file
		Iterator<Action> actionIter = this.actions.iterator();
		Action currAction;
		ITree currNode;
		String output = "";
		while(actionIter.hasNext())
		{
			// mov, del and update: old tree context and old file
			currAction = actionIter.next();
			// just deal with leaf node
			currNode = currAction.getNode();
			if(isActionOfComment(currAction))
				continue;
			if(!currNode.isLeaf() && currAction.getName() != "MOV")
			{
				continue;
			}
			// action type -> prefix
			switch(currAction.getName())
			{
			case "INS":
				Insert insertAction = (Insert)currAction;
				output += "add\t" + NEW_MARK;
//					new node
				output += this.getPrettyString(insertAction.getNode(), this.newTreeContext, this.newFile);
				output += NEW_MARK + "\tin\t" + OLD_MARK;
//					old node
				ITree parentNode = insertAction.getParent();
				ITree oldNode = this.mappings.getSrc(parentNode);
				while(parentNode != null && oldNode == null)
				{
					parentNode = parentNode.getParent();
					oldNode = historyMap.getSrc(parentNode);
				}
				output += this.getPrettyString(oldNode, this.oldTreeContext, this.oldFile) + OLD_MARK;
				break;
			case "DEL":
				output += "remove\t" + OLD_MARK;
				Delete deleteAction = (Delete)currAction;
				// old node
				output += this.getPrettyString(deleteAction.getNode(), this.oldTreeContext, this.oldFile);
				output += OLD_MARK + "\tfrom\t" + OLD_MARK;
				// parent
				output += this.getPrettyString(deleteAction.getNode().getParent(), this.oldTreeContext, this.oldFile) + OLD_MARK;
				break;
			case "UPD":
				output += "update\t" + OLD_MARK;
				Update updateAction = (Update)currAction;
				// old node
				output += this.getPrettyString(updateAction.getNode(), this.oldTreeContext, this.oldFile);
				// new value
				output += OLD_MARK + "\tto\t" + NEW_MARK;
				output += this.getType(updateAction.getNode(), this.oldTreeContext);
				output += ": ";
				output += updateAction.getValue().replace("\n", "") + NEW_MARK;
				break;
			case "MOV":
				output += "move\t" + OLD_MARK;
				Move moveAction = (Move)currAction;
				// old node
				output += this.getPrettyString(moveAction.getNode(), this.oldTreeContext, this.oldFile);
				// old parent
				output += OLD_MARK + "\tfrom\t" + OLD_MARK;
				output += this.getPrettyString(moveAction.getParent(), this.oldTreeContext, this.oldFile) + OLD_MARK;
//					System.out.printf("WARN: DO NOT DEAL WITH MOVE in %s: %d\n", this.oldFile, this.oldLoc);
				break;
			}
			
			output += "\n";
		}
		
//			System.out.printf("%s", output);
		return output;
	}
		
	// old file: old log file(mainly)
	// new file: new log file(mainly)
	// edit: add/insert/delete/remove
	public String getSyntacticalEdit()
	{
		// judge its action type
		Action currAction;
		ITree currNode;
		Iterator<Action> actionIter = this.actions.iterator();
		String output = "";
		while(actionIter.hasNext())
		{
			// mov, del and update: old tree context and old file
			currAction = actionIter.next();
			// just deal with leaf node
			currNode = currAction.getNode();
			if(isActionOfComment(currAction))
				continue;
			if(!currNode.isLeaf() && currAction.getName() != "MOV")
			{
				continue;
			}
			// action type -> prefix
			switch(currAction.getName())
			{
			case "INS":
				Insert insertAction = (Insert)currAction;
				output += "add\t";
//				new node
				output += this.getPrettyString(insertAction.getNode(), this.newTreeContext, this.newFile);
				output += "\tin\t";
//				old node
				ITree parentNode = insertAction.getParent();
				ITree oldNode = this.mappings.getSrc(parentNode);
				while(oldNode == null && parentNode != null)
				{
					parentNode = parentNode.getParent();
					oldNode = this.mappings.getSrc(parentNode);
				}
				output += this.getPrettyString(oldNode, this.oldTreeContext, this.oldFile);
				break;
			case "DEL":
				output += "remove\t";
				Delete deleteAction = (Delete)currAction;
				// old node
				output += this.getPrettyString(deleteAction.getNode(), this.oldTreeContext, this.oldFile);
				output += "\tfrom\t";
				// parent
				output += this.getPrettyString(deleteAction.getNode().getParent(), this.oldTreeContext, this.oldFile);
				break;
			case "UPD":
				output += "update\t";
				Update updateAction = (Update)currAction;
				// old node
				output += this.getPrettyString(updateAction.getNode(), this.oldTreeContext, this.oldFile);
				// new value
				output += "\tto\t";
				output += this.getType(updateAction.getNode(), this.oldTreeContext);
				output += ": ";
				output += updateAction.getValue().replace("\n", "");
				break;
			case "MOV":
				output += "move\t";
				Move moveAction = (Move)currAction;
				// old node
				output += this.getPrettyString(moveAction.getNode(), this.oldTreeContext, this.oldFile);
				// old parent
				output += "\tfrom\t";
				output += this.getPrettyString(moveAction.getParent(), this.oldTreeContext, this.oldFile);
//				System.out.printf("WARN: DO NOT DEAL WITH MOVE in %s: %d\n", this.oldFile, this.oldLoc);
				break;
			}
			
			output += "\n";
		}
		
//		System.out.printf("%s", output);
		return output;
	
	}
	
	// old file: old log file
	// new file: new log file
	// edit type: content/ variable [add, remove, update]
	public Set<String> getLogEditType()
	{
		Set<String> editType = new HashSet<String>();
		// judge its action type
		String prefix; String postfix; Action currAction;
		ITree currNode; TreeContext treeContext; String filename;
		Iterator<Action> actionIter = this.actions.iterator();
		while(actionIter.hasNext())
		{
			prefix = null;
			postfix = null;
			// mov, del and update: old tree context and old file
			treeContext = this.oldTreeContext;
			filename = this.oldFile;
			currAction = actionIter.next();
			// just deal with nulleaf node
			currNode = currAction.getNode();
			if(!currNode.isLeaf())
			{
				continue;
			}
			// action type -> prefix
			switch(currAction.getName())
			{
			case "INS":
				prefix = "add";
				// insert: new tree context and new file
				treeContext = this.newTreeContext;
				filename = this.newFile;
				break;
			case "DEL":
				prefix = "remove";
				break;
			case "UPD":
				prefix = "update";
				break;
			case "MOV":
				prefix = "move";
				System.out.printf("WARN: DO NOT DEAL WITH MOVE in %s: %d\n", this.oldFile, this.oldLoc);
				break;
			}
			// node type -> postfix
			// constant -> content
			if(this.isConstant(currNode, treeContext, filename))
			{
				postfix = "Content";
			}
			// name -> argument -> variable
			else if(this.isChildOfArgument(currNode, treeContext, filename))
			{
				postfix = "Variable";
			}
			// name -> non-argument -> log
			else
			{
				postfix = "Log";
			}
			
			// add to result set
//			System.out.println(prefix + postfix);
			editType.add(prefix + postfix);
		}
		
		return editType;
	
	}
	protected void getEditedNodes()
	{
//		System.out.println(actions.size());
		Iterator<Action> actionIter = actions.iterator();
		Action action;
		while(actionIter.hasNext())
		{
			action = actionIter.next();
			if(!isActionOfComment(action))
			{
//				System.out.println(action.getName());
				ITree tempNode = action.getName().equals("INS") ? ((Insert)action).getParent() : action.getNode();
				if(isChildrenOf(tempNode, this.oldTree))
				{
					this.editedNodes.add(tempNode);
				}
//				printNode(action.getName().equals("INS") ? ((Insert)action).getParent() : action.getNode(), this.oldTreeContext, this.oldFile);
			}
		}
	}
	
	protected LinkedList<String[]> getWordEdit()
	{
//		System.out.println(actions.size());
		Iterator<Action> actionIter = actions.iterator();
		LinkedList<String[]> editElements = new LinkedList<String[]>();
		Action action;
		String newElement = "";
		String oldElement = "";

		ITree currNode;
//		LinkedList<ITree> edit_nodes = new LinkedList<ITree>();
//		ITree historyNode;
//		boolean isNew;
		while(actionIter.hasNext())
		{
			action = actionIter.next();
			if(!isActionOfComment(action))
			{
				currNode = action.getNode();
//				System.out.println(this.getValue(currNode, this.oldFile));
//				isNew = true;
//				for(int i = 0; i < edit_nodes.size(); i++)
//				{
//					historyNode = edit_nodes.get(i);
//					// currNode is children -> ignore
//					if(this.isChildrenOf(currNode, historyNode))
//					{
//						isNew = false;
//						break;
//					}
//					// historyNode is children -> remove children, keep parent
//					if(this.isChildrenOf(historyNode, currNode))
//					{
//						int index = edit_nodes.indexOf(historyNode);
//						edit_nodes.remove(historyNode);
//						i--;
//						editElements.remove(index);
//					}
//				}
				if(currNode.isLeaf())
				{
//					System.out.println(this.getType(currNode, this.oldTreeContext));
//					edit_nodes.add(currNode);
					switch(action.getName())
					{
					case "INS":
						oldElement = "";
						newElement = this.getValue(action.getNode(), this.newFile);
						break;
					case "DEL":
						oldElement = this.getValue(action.getNode(), this.oldFile);
						newElement = "";
						break;
					case "UPD":
						oldElement = this.getValue(action.getNode(), this.oldFile);
						newElement = ((Update)action).getValue();
						break;
					}
					String edit_element[] = {oldElement, newElement};
					editElements.add(edit_element);
				}				
			}
		}
		
		return editElements;
	}
	
	protected boolean isMatchWithEdit(String reposFile)
	{
		this.setNewFile(reposFile);
		Iterator<Action> actionIter = actions.iterator();
		while (actionIter.hasNext()) {
			if (!isAcceptableAction(actionIter.next())) {
				return false;
			}
		}
		return true;
	}
	
//	judge match by allowing update actions
	protected boolean isMatch() {
		Iterator<Action> actionIter = actions.iterator();
		Action action;
		while (actionIter.hasNext()) {
			action = actionIter.next();
			if (!isActionOfComment(action) && !action.getName().equals("UPD")) {
				return false;
			}
		}
		return true;
	}
	
	private boolean isNodeDelete(ITree node)
	{
		Iterator<Action> actionIter = actions.iterator();
		while(actionIter.hasNext())
		{
			Action action = actionIter.next();
			// delete of given node
			if(action.getName().equals("DEL") && action.getNode().equals(node))
				return true;
		}
		
		return false;
	}
	
	private boolean isNodeInsert(ITree node)
	{
		Iterator<Action> actionIter = actions.iterator();
		while(actionIter.hasNext())
		{
			Action action = actionIter.next();
			// delete of given node
			if(action.getName().equals("INS") && action.getNode().equals(node))
				return true;
		}
		
		return false;
	}
	
	private boolean isAcceptableAction(Action action)
	{
		if(!isActionOfComment(action))
		{
			String changeType = action.getName();
			// non comment, non update
			if(!changeType.equals("UPD"))
			{
				return false;
			}
			ITree actionNode = action.getNode();
			Iterator<ITree> editedIter = editedNodes.iterator();
			while(editedIter.hasNext())
			{
				// non comment, update, edited
				if(editedIter.next().equals(actionNode))
				{
					return false;
				}
			}
		}
		//comment || non comment, update, non edited
		return true;
	}
	
	private void setNewFile(String newFile)
	{
		try {
			this.newFile = newFile;
			this.newTreeContext = Generators.getInstance().getTree(newFile);
			this.newTree = this.newTreeContext.getRoot();
			this.getActions();
		} catch (Exception e) {
			// e.printStackTrace();
			System.out.println(e.toString());
			System.out.printf("update newFile:%s \n", newFile);
		}
		
	}
	
	// old file, new file
	private void getActions()
	{
		// initialize matcher
		matcher = Matchers.getInstance().getMatcher(this.oldTree, this.newTree);
		matcher.match();
		mappings = matcher.getMappings();
		// initialize action generator
		actionGenerator = new ActionGenerator(oldTree, newTree, matcher.getMappings());
		actionGenerator.generate();
		actions =  actionGenerator.getActions();

	}
	
	// judge whether an action is about comment
	private boolean isActionOfComment(Action action)
	{
		boolean isComment;
		ITree operatedNode = action.getNode();
		switch(action.getName())
		{
		case "INS":
			isComment = this.isComment(operatedNode, this.newTreeContext, this.newFile);
			break;
		default:
			isComment = this.isComment(operatedNode, this.oldTreeContext, this.oldFile);
			break;
		}
		return isComment;
	}
	
	// judge whether an action is about comment
	private boolean isActionOfComment(Action action, TreeContext newTreeContext, String newFile)
	{
		boolean isComment;
		ITree operatedNode = action.getNode();
		switch(action.getName())
		{
		case "INS":
			isComment = this.isComment(operatedNode, newTreeContext, newFile);
			break;
		default:
			isComment = this.isComment(operatedNode, this.oldTreeContext, this.oldFile);
			break;
		}
		return isComment;
	}
	
	
	// judge whether an action is about comment
	private boolean isInsertionOfLog(Action action)
	{
		if(action.getName().equals("INS"))
		{
			ITree newNode = action.getNode();
			Iterator<ITree> newLogsIter = this.newLogs.iterator();
			while(newLogsIter.hasNext())
			{	
//				this.isChildrenOf(this.newLogNode, currAction.getNode()
//				inserted node is children of log
				if(this.isChildrenOf(newNode, newLogsIter.next()))
				{
					return true;
				}
			}
		}
		return false;
	}
	
	// one line to src node
	private ITree getLogNodeOfLine(int line, ITree rootNode, TreeContext treeContext, String filename) {
		// ITree topNode = isOld ? oldTree : newTree;
		line = line + 1;
//		Iterator<ITree> allNodesIter = rootNode.getDescendants().iterator();
		// bread first, so the first one from this line is top one from this line
		Iterator<ITree> allNodesIter = rootNode.breadthFirst().iterator();
//		ignore the toppest level
		allNodesIter.next();
		ITree tempNode, largestNode = null;

		while (allNodesIter.hasNext()) {
			tempNode = allNodesIter.next();
			// the node with most children in given line [!block fault!]
			if (getLineNumber(tempNode, filename, true) == line){
				//TODO call with given name and loc
				if(this.isCall(tempNode, treeContext, filename)) {
					largestNode = tempNode;
					break;
				}
			}
		}

		// printNode(largestNode, isOld);
		return largestNode;
	}
	
	// one line to src node, may be parameter
	private ITree getDDGNodeOfLine(int line, ITree rootNode, TreeContext treeContext, String filename) {
		// start from 0
		if(line <= 0)
			return null;
		line = line + 1;
//		Iterator<ITree> allNodesIter = rootNode.getDescendants().iterator();
		// bread first, so the first one from this line is top one from this line
		Iterator<ITree> allNodesIter = rootNode.breadthFirst().iterator();
//		ignore the toppest level
		allNodesIter.next();
		ITree tempNode, largestNode = null;

		while (allNodesIter.hasNext()) {
			tempNode = allNodesIter.next();
			// the node with most children in given line [!block fault!]
			if (getLineNumber(tempNode, filename, true) == line && 
//					!this.isBlock(tempNode, treeContext, filename)){
					this.isDDG(tempNode, treeContext, filename)) {
				largestNode = tempNode;
				break;
			}
		}

		// printNode(largestNode, isOld);
		return largestNode;
	}

	
	// first argument: child node
	// second argument: parent node
	private boolean isChildrenOf(ITree child, ITree parentNode) {
		//	children size must less than parent
		if(child.getSize() > parentNode.getSize())
		{
			return false;
		}
		//	traverse all ancestors to validate whether parent node is a "real parent"
		boolean isChildren = parentNode.equals(child);
		Iterator<ITree> parents = child.getParents().iterator();
		ITree tempNode;
		while (!isChildren && parents.hasNext()) {
			tempNode = parents.next();
			if (tempNode.equals(parentNode)) {
				isChildren = true;
			}
		}

		return isChildren;
	}
	// is parentNode is one of the parents of node[include node itself]
	private boolean isChildOfArgument(ITree child, TreeContext treeContext, String filename) {
		//	traverse ancestors to validate whether has a parent whose type is argument
		boolean isArgument = this.isArgument(child, treeContext, filename);
		Iterator<ITree> parents = child.getParents().iterator();
		ITree tempNode;
		while (!isArgument && parents.hasNext()) {
			tempNode = parents.next();
			if (this.isArgument(tempNode, treeContext, filename)) {
				isArgument = true;
			}
		}

			return isArgument;
		}
		

	// print node
	private void printNode(ITree node, TreeContext treeContext, String filename) {
		System.out.printf("node value: %s, type:%s, line: %d, size: %d \n", getValue(node, filename),
				getType(node, treeContext), getLineNumber(node, filename, true), node.getSize());

	}
	
	// get text value of given node
	private String getType(ITree node, TreeContext treeContext) {
		return treeContext.getTypeLabel(node.getType());
	}
	
	private String getPrettyString(ITree node, TreeContext treeContext, String filename) {
		String result = "";
		if(node == null)
			return "null";
		if(this.isConstant(node, treeContext, filename))
			return "literal: " + getValue(node, filename).replace("\n","");
		result += node.toPrettyString(treeContext);
		if(node.isLeaf())
			return result;
		
		result += ": ";
		result += getValue(node, filename).replace("\n","");;

		return result;
	}
	// get text value of given node
	private String getValue(ITree node, String filename) {
		int beginPos = node.getPos();
		int endPos = node.getEndPos();
		// System.out.printf("beginPos: %d, endPos: %d\n", beginPos, endPos);
		if(beginPos == -1)
			return "";
		// String filename = isOld ? oldFile : newFile;
		try {
			FileReader fileReader;
			fileReader = new FileReader(filename);
			fileReader.skip(beginPos);

			char[] value = new char[endPos - beginPos];
			fileReader.read(value, 0, endPos - beginPos);
			fileReader.close();

			return String.valueOf(value).trim();
		} catch (Exception e) {
			// e.printStackTrace();
			System.out.println(e.toString());
			System.out.printf("filename: %s, beginPos: %d, endPos:%d \n", filename, beginPos, endPos);
			return "";
		}
	}

	// get start line number of given node
	private int getLineNumber(ITree node, String filename, boolean isStart) {
		// String filename = isOld ? oldFile : newFile;
		int characterPos = isStart ? node.getPos() : node.getEndPos() + 1;
		if(characterPos == -1)
			return -1;
		LineNumberReader lineReader;
		int lineNumber = -1;
		try {
			lineReader = new LineNumberReader(new FileReader(filename));
			lineReader.skip(characterPos);

			lineNumber = lineReader.getLineNumber() + 1;
			lineReader.close();
		} catch (Exception e) {
			// e.printStackTrace();
			System.out.println(e.toString());
			System.out.printf("filename: %s, beginPos: %d \n", filename, characterPos);
			return -1;
		}

		return lineNumber;
	}
	
	private boolean isBlock(ITree node, TreeContext treeContext, String filename)
	{
		String block = filename.endsWith(".cpp") ? "block" : "Compound";
		boolean isBlockFlag = getType(node, treeContext).equals(block);
		if(!isBlockFlag)
		{
			Iterator<ITree> children = node.breadthFirst().iterator();
			while(children.hasNext())
			{
				if(getType(children.next(), treeContext).equals(block))
				{
					isBlockFlag = true;
					break;
				}
			}
		}
		
		return isBlockFlag;
	}
	
	private boolean isControl(ITree node, TreeContext treeContext)
	{		
		String type = getType(node, treeContext);
		return type.equals("if") || type.equals("switch") ;
	}
	
	private boolean isCondition(ITree node, TreeContext treeContext)
	{		
		String type = getType(node, treeContext);
		return type.equals("condition");
	}
	
	private boolean isFunction(ITree node, TreeContext treeContext, String filename)
	{
		String function = filename.endsWith(".cpp") ? "function" : "Definition";
		String type = getType(node, treeContext);
		return type.equals(function);
	}
	
	private boolean isCall(ITree node, TreeContext treeContext, String filename)
	{
		String call = filename.endsWith(".cpp") ? "call" : "FunCall";
		String type = getType(node, treeContext);
		if(type.equals(call))
			return true;
		else
			return false;
	}
	
	private boolean isConstant(ITree node, TreeContext treeContext, String filename)
	{
		String constant = filename.endsWith(".cpp") ? "literal" : "Constant";
		String type = getType(node, treeContext);
		if(type.equals(constant))
			return true;
		else
			return false;
	}
	
	private boolean isArgument(ITree node, TreeContext treeContext, String filename)
	{
		String argument = filename.endsWith(".cpp") ? "argument" : "Argument";
		String type = getType(node, treeContext);
		if(type.equals(argument))
			return true;
		else
			return false;
	}
	
	private boolean isStatement(ITree node, TreeContext treeContext, String filename)
	{
		String statement = filename.endsWith(".cpp") ? "stmt" : "Statement";
		String type = getType(node, treeContext);
		if(type.endsWith(statement) || type.equals("expr"))
			return true;
		else
			return false;
	}
	
	private boolean isDDG(ITree node, TreeContext treeContext, String filename)
	{
		return true;
	}
	
	private boolean isComment(ITree node, TreeContext treeContext, String filename)
	{
		if(filename.endsWith(".cpp"))
		{
			return getType(node, treeContext).equals("comment");
		}
		else
		{
//			c/h file do not analyze comment
			return false;
		}
	}
	
	protected void getDeltaBlockfeature()
	{
		List<Integer> oldBlockFeature = getBlockFeature(this.oldTree, this.oldTreeContext);
		List<Integer> newBlockFeature = getBlockFeature(this.newTree, this.newTreeContext);
		System.out.println(oldBlockFeature.toString());
		System.out.println(newBlockFeature.toString());
 	}
	
	
	// syntax feature of block file 
	private List<Integer> getBlockFeature(ITree blockNode, TreeContext treeContext)
	{
		int ast_type_num = this.AST_TYPE.size();
		Integer[] frequence = new Integer[ast_type_num];
		for(int i = 0; i < ast_type_num; i++)
		{
			frequence[i] = 0;
		}
		// traverse all nodes to count frequence vector
		Iterator<ITree> allNodesIter = blockNode.getDescendants().iterator();
		String tempType;
		int index;
		while(allNodesIter.hasNext())
		{
			tempType = getType(allNodesIter.next(), treeContext);
//			System.out.printf("type: %s\n", tempType);

			index = this.AST_TYPE.indexOf(tempType);
			if(index != -1)
			{
				frequence[index] += 1;
			}
			else if(this.AST_EXCEPT_TYPE.indexOf(tempType) == -1)
			{
				System.out.printf("type: %s can not be found\n", tempType);
			}
		}
		
		return Arrays.asList(frequence);
	}

	public void printSpliter()
	{
		System.out.println("----------------------------------------");
	}
	/*
	 * public void getMapping(String oldFile, String newFile) {
	 * Run.initGenerators(); try {// parse to get tree info TreeContext
	 * oldTreeContext = Generators.getInstance().getTree(oldFile); TreeContext
	 * newTreeContext = Generators.getInstance().getTree(newFile); ITree oldTree =
	 * oldTreeContext.getRoot(); ITree newTree = newTreeContext.getRoot(); // match
	 * two trees Matcher m = Matchers.getInstance().getMatcher(oldTree, newTree);
	 * m.match(); Iterator<Mapping> mappingIter = m.getMappings().iterator(); ITree
	 * srcNode, dstNode; while(mappingIter.hasNext()) { Mapping mapping =
	 * mappingIter.next(); srcNode = mapping.getFirst(); dstNode =
	 * mapping.getSecond();
	 * System.out.printf("1) src info. type:%s, value:%s, line:%d \n",
	 * oldTreeContext.getTypeLabel(srcNode), getValue(srcNode, oldFile),
	 * getLineNumber(srcNode, oldFile, true));
	 * System.out.printf("2) dst info. type:%s, value:%s, line:%d \n",
	 * newTreeContext.getTypeLabel(dstNode), getValue(dstNode, newFile)
	 * dstNode.getLabel(), getLineNumber(dstNode, newFile, true)); } // generate
	 * actions ActionGenerator actionGenerator = new ActionGenerator(oldTree,
	 * newTree, m.getMappings()); actionGenerator.generate(); List<Action> actions =
	 * actionGenerator.getActions();
	 * System.out.printf("3) element edit distance: %d \n", actions.size()); }
	 * catch(UnsupportedOperationException | IOException e) { e.printStackTrace(); }
	 * }
	 * 
	 * 
	 * public void getAction(String oldFile, String newFile) { Run.initGenerators();
	 * try { // parse to get tree info TreeContext oldTreeContext =
	 * Generators.getInstance().getTree(oldFile); TreeContext newTreeContext =
	 * Generators.getInstance().getTree(newFile); ITree oldTree =
	 * oldTreeContext.getRoot(); ITree newTree = newTreeContext.getRoot(); // match
	 * two trees Matcher m = Matchers.getInstance().getMatcher(oldTree, newTree);
	 * m.match(); m.getMappings(); // generate actions ActionGenerator
	 * actionGenerator = new ActionGenerator(oldTree, newTree, m.getMappings());
	 * actionGenerator.generate(); List<Action> actions =
	 * actionGenerator.getActions(); // parse actions according to type Action
	 * action; ITree tempNode; for(Iterator<Action> iter = actions.iterator();
	 * iter.hasNext(); ) { action = iter.next(); // change type String changeType =
	 * action.getName(); System.out.printf("1) change info. change type: %s \n",
	 * changeType); // value and loc info String oldValue = ""; String newValue =
	 * ""; int oldLoc = -1; int newLoc = -1; switch(changeType) { // INSERT: new
	 * value, new loc case "INS": tempNode = action.getNode(); newValue =
	 * tempNode.getLabel(); newLoc = getLineNumber(tempNode, newFile, true); break;
	 * // UPDATE: old / new value; old loc[old value and old loc by default] case
	 * "UPD": newValue = ((Update)action).getValue(); // MOVE/DELETE: old value, old
	 * loc default: tempNode = action.getNode(); oldValue = tempNode.getLabel();
	 * oldLoc = getLineNumber(tempNode, oldFile, true); break; }
	 * System.out.printf("2) old info. value: %s, line: %d \n", oldValue, oldLoc);
	 * System.out.printf("3) new info. value:%s, line:%d \n", newValue, newLoc); } }
	 * catch (UnsupportedOperationException | IOException e) { e.printStackTrace();
	 * } } // get start line number of given node int getLineNumber(ITree node,
	 * String filename, boolean isStart) { int characterPos = isStart ?
	 * node.getPos() : node.getEndPos(); LineNumberReader lineReader; int lineNumber
	 * = -1; try { lineReader = new LineNumberReader(new FileReader(filename));
	 * lineReader.skip(characterPos);
	 * 
	 * lineNumber = lineReader.getLineNumber() + 1; //
	 * System.out.println(lineReader.readLine()); lineReader.close(); } catch
	 * (IOException e) { e.printStackTrace(); }
	 * 
	 * return lineNumber; }
	 * 
	 * // get text value of given tree node String getValue(ITree node, String
	 * filename) { int beginPos = node.getPos(); int endPos = node.getEndPos(); try
	 * { FileReader fileReader; fileReader = new FileReader(filename);
	 * fileReader.skip(beginPos);
	 * 
	 * char[] value = new char[100]; fileReader.read(value, 0, endPos - beginPos);
	 * fileReader.close();
	 * 
	 * return String.valueOf(value).trim(); } catch (IOException e) {
	 * e.printStackTrace(); return ""; } }
	 */
	
//	if(action.getName().equals("INS"))
//	{
//		printNode(action.getNode(), this.newTreeContext, this.newFile);
//		printNode(((Insert)action).getParent(), this.oldTreeContext, this.oldFile);
//	}
//	else
//	{
//		printNode(action.getNode(), this.oldTreeContext, this.oldFile);
//	}
	/*
	// one line to action type NO, OVER, ..
	public int getActionType() {
		int isLog = 0;
		int isLogs = 0;
		int isFeature = 0;
		
		Iterator<Action> actionIter = actions.iterator();
		Action action;
		ITree tempNode;
		boolean isIdentified;
//		printNode(this.oldLogNode, this.oldTreeContext, this.oldFile);
		while (actionIter.hasNext()) {
			action = actionIter.next();
			// do not deal with comment modification
			if(this.isActionOfComment(action))
			{
				continue;
			}
// 			judge if leaf edition is edition of logs
			tempNode = action.getName().equals("INS") ? ((Insert)action).getParent() : action.getNode();
			isIdentified = false;
//			System.out.println(action.toString());
			if(isFeature == 0 || isLog == 0 || isLogs == 0)
			{
//				edition of old tree
				if(!isChildrenOf(tempNode, this.oldTree))
				{
//					System.out.println(action.toString());
					continue;
				}
//				decide whether is log
				if(isChildrenOf(tempNode, this.oldLogNode))
				{
//					System.out.println(action.getName());
//					printNode(tempNode, this.oldTreeContext, this.oldFile);
					isLog = 1;
					isIdentified = true;
					isLogs = 2;
					continue;
				}
//				decide whether is logs if not this log
				Iterator<ITree> logIter = this.oldLogs.iterator();
				while (logIter.hasNext()) {
					if (isChildrenOf(tempNode, logIter.next())) {
						isLogs = 2;
						isIdentified = true;
						break;
					}
				}
//				decide whether features if not logs
				if(!isIdentified && isFeature == 0)
				{
					isFeature = 4;
				}
			}
			else
			{
				break;
			}
		}
		
		return (isLog + isLogs + isFeature);
	}
*/	
	
}
