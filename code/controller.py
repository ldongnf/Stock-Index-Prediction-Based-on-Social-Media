#!/usr/bin/env python
#-*- coding: utf8 -*-
import dataparser
import datafilter
import sentimentanalysis
import prediction
import support
import workers
import os
import re
from Queue import *

def controll(override=False):
	root_dir = "./data"
	attrs = {'a':["nk"],'span':["ctt","ct"]}
	sentiment_lexicon_path = "./lexicon/dictionary.txt"
	name_file_name = "name.txt"
	content_file_name = "content.txt"
	date_file_name = "date.txt"
	result_file_name = "res.txt"
	base_date_file_name = "basetime.txt"
	parsered_result_file_names = [name_file_name, content_file_name, date_file_name]
	predict_length = -5

	if override:
		lists = ['content.txt','name.txt','date.txt','res.txt','seged_content.txt','negative.txt','positive.txt','calm.txt','result.txt']
		support.clear_up(root_dir,lists)
	
	sentiment_lexicon = sentimentanalysis.generate_sentiment_lexicon(sentiment_lexicon_path)
	sentiment_analysis_result = {}
	
	sub_dirs = support.get_subdirs(root_dir)

	for sub_dir in sub_dirs:
		temp = sub_dir.split('/')[-1]
		target_time = temp[:4] + '-' + temp[4:6] + '-' + temp[6:8]
		directories = support.get_directories(sub_dir, '\d.html')
		print "-------------------------"
		print "processing: ", sub_dir
		for directory in directories:
			dataparser.dir_parser(directory, "\d.html", attrs, "ADD", directory)			
			datafilter.normalize_date(directory, date_file_name, base_date_file_name)
			
			for target in parsered_result_file_names:
				support.summery_parser_file(directory + '/' + target, sub_dir + '/' + target)
		
		datafilter.data_preprocess(sub_dir, name_file_name, content_file_name, date_file_name, "B", 0.5, target_time)		
		sentiment_analysis_result[target_time] = sentimentanalysis.main_analysis(sentiment_lexicon, sub_dir, content_file_name, result_file_name)
		print "-------------------------\n"
	
	support.log_result(root_dir, sentiment_analysis_result)
	
	print prediction.linear_regression(root_dir, 'result.txt', 'real.txt', predict_length)
	print prediction.svm_regression(root_dir, "result.txt", "real2.txt", "real.txt", "seged_content.txt", 10500, predict_length)	

controll(override=False)
