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
import datetime
import zhon.hanzi
import string

def data_preprocess(root_dir, name_file, content_file, date_file, remove_model, similarity_percentage, target_date):
	# root_dir: 	file folder
	# name_file:	file contains bolg names
	# content_file:	file contains 
	# date_file:	file contains the bolg date
	# remove_model:	remove all or part
	# similarity_percentage: how to compare and remove

	# PK: blog and content and date N: name C: content D: date
	
	intermediate_file_name = "pk_NC.txt"
	pk_file_name = "pk_NCD.txt"

	base_date_file = "basetime.txt"

	related_file_names = [name_file, content_file, date_file]
	remove_punctuation_emojis(root_dir, content_file)
	#remove_first_char(root_dir, content_file)
	print "target_date:", target_date

	date_filter(root_dir, date_file, target_date, related_file_names)

	pk_date_file_name = generate_pk_date(root_dir, date_file)

	merge_file(root_dir, name_file, content_file, intermediate_file_name)
	merge_file(root_dir, pk_date_file_name, intermediate_file_name, pk_file_name)
	
	remove_noise(root_dir, content_file, related_file_names)
	deduplicates(root_dir, pk_file_name, related_file_names, remove_model, similarity_percentage)
	
	os.remove(root_dir + '/' + intermediate_file_name)
	os.remove(root_dir + '/' + pk_date_file_name)
	os.remove(root_dir + '/' + pk_file_name)
	return pk_file_name

def generate_noise_list(root_dir, noise_file_name):
	# root_dir: root
	# noise_file_name: noise file name
	
	with open(root_dir + '/' + noise_file_name, 'r') as file:
		return [line.rstrip() for line in file]

def remove_noise(root_dir, content_file, related_file_names):
	# root_dir: root_dir
	# content_file: content_file
	# related_file_names:	related files

	noise_list = generate_noise_list('./lexicon','noise.txt')
	patterns = [re.compile(word) for word in noise_list]
	content_file_path = root_dir + '/' + content_file

	input_length = 0
	indexes = []
	with open(content_file_path, 'r') as file:
		for index, line in enumerate(file):
			has_found = False
			for pattern in patterns:
				if pattern.search(line):
					has_found = True
					break
			if not has_found:
				indexes.append(index)
			input_length = index
	
	print "remove noise"
	print "Input Items: ", input_length
	print "Reoved Noisy Items: ", input_length - len(indexes)
	print "remaining:",	len(indexes)
	print "-------------------------"

	if indexes:
		for related_file_name in related_file_names:
			update_file_by_indexes(indexes, root_dir, related_file_name)
	return indexes

def generate_pk_date(root_dir, date_file):
	# root_dir:		root_dir
	# date_file:	date_file
	
	date_file_path = root_dir + '/' + date_file
	pk_date_file_name = "pk_date.txt"
	pk_date_file_path = root_dir + '/' + pk_date_file_name
	with open(date_file_path, "r") as file, open(pk_date_file_path, "w") as pk_date_file:
		for line in file:
			date = line.split(" ")[0]
			pk_date_file.write(date.rstrip() + '\n')
	return pk_date_file_name
 
def date_filter(root_dir, date_file, target_date, related_file_names):
	# root_dir:		root_dir
	# date_file:	date_file
	# target_date:	the selected time
	
	date_file_path = root_dir + '/' + date_file
	filtered_date_file_path = root_dir + '/' + "filtered_" + date_file
	target_date_time = datetime.datetime.strptime(target_date, "%Y-%m-%d")
	lower_bound = target_date_time.replace(hour=15, minute=0, second=0)
	upper_bound = (target_date_time + datetime.timedelta(days=1)).replace(hour=9, minute=0, second=0)

	indexes = []
	length = 0

	with open(date_file_path, "r") as file, open(filtered_date_file_path, "w") as new_file:
		for index, line in enumerate(file):
			length = index
			date_time_str = line.rstrip()
			date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

			if lower_bound < date_time < upper_bound:
				new_file.write(line)
				indexes.append(index)

	print "selected date"
	print "input size:", length
	print "removed:", length - len(indexes)
	print "remain:", len(indexes)
	print "----------------------------"

	if indexes:
		for related_file_name in related_file_names:
			update_file_by_indexes(indexes, root_dir, related_file_name)

	os.remove(date_file_path)
	os.rename(filtered_date_file_path, date_file_path)

def remove_punctuation_emojis(root_dir, file_name):
	# root_dir: directory
	# file_name: content file name
	
	new_file_name = "temp.txt"
	new_file_path = root_dir + '/' + new_file_name
	file_path = root_dir + '/' + file_name
	emoji_pattern = re.compile(
		u"(\ud83d[\ude00-\ude4f])|"  # emoticons
		u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
		u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
		u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
		u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
		"+", flags=re.UNICODE)

	with open(new_file_path, "w") as new_file, \
		open(file_path, "r") as file:
			for line in file:
				temp = line.decode("utf8")
				punctuation = zhon.hanzi.punctuation + string.punctuation
				new_line = re.sub(ur"[%s]+" % punctuation, "", line.decode("utf-8"))
				new_line = emoji_pattern.sub("".decode('utf8'), new_line)
				new_line = re.sub("\w+".decode('utf8'), "".decode('utf8'), new_line)
				new_file.write(new_line.encode("utf8"))
	os.remove(file_path)
	os.rename(new_file_path, file_path)

def remove_first_char(root_dir, file_name):
	# root_dir: directory
	# file_name: content file name
	
	new_file_name = "temp.txt"
	new_file_path = root_dir + '/' + new_file_name
	file_path = root_dir + '/' + file_name
	
	with open(new_file_path, "w") as new_file, \
		open(file_path, "r") as file:
			for line in file:
				if line.startswith(':'):
					new_file.write(line[1:])
				else:
					new_file.write(line)
	os.remove(file_path)
	os.rename(new_file_path, file_path)

def merge_file(root_dir, file_name_1, file_name_2, merged_file_name):
	with open(root_dir + '/' + merged_file_name ,"w") as merged_file, \
		open(root_dir + '/' + file_name_1, "r") as file1, \
		open(root_dir + '/' + file_name_2, "r") as file2:
		
		for line_in_file_1, line_in_file_2 in zip(file1, file2):
			merged_file.write(line_in_file_1.rstrip() + "\t" + line_in_file_2)

def normalize_date(root_dir, date_file, base_date_file):
	# root_dir:		root_dir
	# date_file:	date_file
	# base_date:	base_date
	# remove unwanted char and backward the time
	
	pk_date_file_name = "pk_date.txt"
	date_file_path = root_dir + '/' + date_file
	new_file_path  = root_dir + '/' + "new_" + date_file
	base_date_path = root_dir + '/' + base_date_file
	
	with open(base_date_path, "r") as base_file:
		base_time = base_file.readline().rstrip()
	base_datetime = datetime.datetime.strptime(base_time, "%Y-%m-%d %H:%M")

	pattern_1 = re.compile("今天 \d\d?:\d\d?")
	pattern_2 = re.compile("\d\d?月\d\d?日 \d\d?:\d\d?")
	pattern_3 = re.compile("\d\d?分钟前")
	pattern_4 = re.compile("\d{4}-\d\d-\d\d \d\d:\d\d")

	with open(date_file_path, "r") as file, open(new_file_path, "w") as new_file:
		for line in file:
			new_datetime = base_datetime
			new_line = pattern_1.search(line)
			if new_line:
				res = new_line.group()
				[hour, minute] = map(int, re.findall("\d\d?", res))
				new_datetime = base_datetime.replace(hour=hour, minute=minute)
			else:
				new_line = pattern_2.search(line)
				if new_line:
					res = new_line.group()
					[month, day, hour, minute] = map(int, re.findall("\d\d?", res))
					new_datetime = base_datetime.replace(month=month, day=day, hour=hour, minute=minute)
				else:
					new_line = pattern_3.search(line)
					if new_line:
						res = new_line.group()
						minutes = map(int, re.findall("\d\d?", res))[0]
						new_datetime = base_datetime + datetime.timedelta(minutes=-minutes)
					else:
						new_line = pattern_4.search(line)
						if new_line:
							new_file.write(new_line.group() + '\n')
							continue
			new_date = new_datetime.strftime("%Y-%m-%d %H:%M")
			new_file.write(new_date+ '\n')

	os.remove(date_file_path)
	os.rename(new_file_path, date_file_path)

def remove_by_percentage(root_dir, file_name, similarity_percentage):
	# root_dir: 	file folder
	# file_name:	source file
	# similarity_percentage: how to compare and remove
	# rtype:		indexes for deduplicate contents

	file_path = root_dir + '/' + file_name
	new_file_path = root_dir + '/' + "new_" + file_name

	indexes, data_buffer = [], []
	length = 0

	with open(file_path, "r") as src_file, open(new_file_path, "w") as new_file:
		for index, content in enumerate(src_file):
			length = index
			pos = int(len(content) * similarity_percentage)
			key = content[:pos]
			if content not in data_buffer:	
				data_buffer.append(content)
				indexes.append(index)
				new_file.write(content)
	
	print "deduplicates:"
	print "input datasize: ", length
	print "duplicates: ", length - len(indexes)
	print "remaining: ", len(indexes)
	print "----------------------------"

	os.remove(file_path)
	os.rename(new_file_path, file_path)
	return indexes

def deduplicates(root_dir, pk_file, related_file_names, remove_model, similarity_percentage):
	# root_dir:	root_dir
	# pk_file:	pk_file
	# remove_model:	remove all or part
	# similarity_percentage: how to compare and remove

	if remove_model =='A':
		pass
		indexes = remove_by_percentage(root_dir, pk_file, 1)
	else:
		print "remove model", remove_model, similarity_percentage
		indexes = remove_by_percentage(root_dir, pk_file, similarity_percentage)
	if indexes:
		for related_file_name in related_file_names:
			update_file_by_indexes(indexes, root_dir, related_file_name)

def update_file_by_indexes(indexes, root_dir, file_name):
	# indexes:	deduplicated content indexes
	# root_dir:	root_dir
	# file_name: file_name

	file_path = root_dir + '/' + file_name
	new_path = root_dir + '/' + "new_" + file_name

	with open(new_path, "w") as new_file, open(file_path, "r") as file:
		i = 0
		length = len(indexes)
		for index, line in enumerate(file):
			if i >= length:
				break
			if index == indexes[i]:
				new_file.write(line)
				i += 1
	os.remove(file_path)
	os.rename(new_path, file_path)
