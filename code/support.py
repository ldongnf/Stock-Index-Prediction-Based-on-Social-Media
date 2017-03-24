#!/usr/bin/env python
#-*- coding: utf8 -*-
"""
module_name, package_name, ClassName, method_name, 
ExceptionName, function_name, GLOBAL_CONSTANT_NAME, 
global_var_name, instance_var_name, 
function_parameter_name, local_var_name
"""
import os
import re

def summery_parser_file(src_file_path, dst_file_path):
	# src_file_path: source file
	# dst_file_path: destination

	with open(dst_file_path, "a") as dst_file, \
		open(src_file_path, "r") as src_file:
		for line in src_file:
			dst_file.write(line)
	
def get_subdirs(root_dir):
	# root_dir:	root_dir
	# rtype:	subdirs of root_dir
	
	return [root_dir + '/' +direct for direct in os.listdir(root_dir) if os.path.isdir(root_dir + '/' + direct)]

def get_directories(root_dir, target_file_name):
	# root_dir:	root_dir
	# target_file_name:	target
	# rtype: all path from root_dir contains target

	paths = []
	for root, dirs, files in os.walk(root_dir, topdown=True):
		if not files:
			continue
		else:
			pattern = re.compile(target_file_name)
			for name in files:
				res = pattern.search(name)
				if res: 
					paths.append(root)
					break
	return paths

def clear_up(root_dir, target_files):
	# root_dir: root
	# target_files: files need to remove
	
	for root, dirs, files in os.walk(root_dir, topdown = True):
		for file in files:
			if file in target_files:
				os.remove(root + '/'+file)
				print root + '/' + file + ' removed'

def log_result(root_dir, sentiment_analysis_result):
	# root_dir: root
	# sentiment_analysis_result: sentiment analysis result

	with open(root_dir + '/' + 'result.txt', 'w') as file:
		for key in sorted(sentiment_analysis_result.keys()):
			file.write(key + ':' + ' '.join(map(str, sentiment_analysis_result[key])) + '\n')
