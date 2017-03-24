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
import lxml.html

def html_parser_lxml(file_path, html_tag, html_tag_attribute ,parser_mode, res_file_path):
	# file_path: source file
	# html_tag, html_tag_attribute:	source
	# parser_mode: ADD or NEW
	# res_file_path: output parser info 

	with open(file_path,"r") as html_file:
		html = html_file.read()

	tree = lxml.html.fromstring(html)
	links_lxml = tree.xpath('//%s[@class="%s"]' % (html_tag, html_tag_attribute))

	with open(res_file_path, "a") as save_file:
		for element in links_lxml:
			save_file.write(element.text_content().encode('utf-8') + '\n')

def multiple_parser(file_path, html_tag_attribute_pairs, parser_mode, res_file_dir):
	# file_path: source file
	# html_tag_attribute_pairs:	source
	# parser_mode: ADD or NEW
	# res_file_dir: result dir

	name_maps = {'nk' : 'name', 'ctt' : 'content', 'ct' : 'date'}
	for tag in html_tag_attribute_pairs:
		for attr in html_tag_attribute_pairs[tag]:
			html_parser_lxml(file_path, tag, attr, parser_mode, res_file_dir + '/' + name_maps[attr] + ".txt")

def dir_parser(root_dir, file_name_pattern, html_tag_attribute_pairs, parser_mode, res_file_dir):
	# root_dir: source file root
	# file_name_pattern: file pattern
	# html_tag_attribute_pairs: source
	# parser_mode: ADD or NEW
	# res_file_dir: result dir

	for root, dirs, files in os.walk(root_dir, topdown = True):
		if os.path.exists(root + '/' + "content.txt"):
			continue
		pattern = re.compile(file_name_pattern)
		for file in files:
			if pattern.search(file):		
				multiple_parser(root + '/' + file, html_tag_attribute_pairs, parser_mode, res_file_dir)
