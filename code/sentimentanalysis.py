#!/usr/bin/env python
#-*- coding: utf8 -*-
"""
module_name, package_name, ClassName, method_name, 
ExceptionName, function_name, GLOBAL_CONSTANT_NAME, 
global_var_name, instance_var_name, 
function_parameter_name, local_var_name
"""

from svm.svm_light.document import create_domain,generate_documents
from svm.svm_light.svmclassify import SVM_classify, run_SVM_classify
import jieba

def generate_sentiment_lexicon(sentiment_lexicon_path):
	# sentiment_lexicon_path: sentiment lexicon path
	
	lexicon= {}
	with open(sentiment_lexicon_path, 'r') as lexicon_file:
		for line in lexicon_file:
			word, sentiment = line.strip().split('\t')
			word = word.decode('utf-8')
			if sentiment == 'P':
				lexicon[word] = 1
			elif sentiment == 'N':
				lexicon[word] = -1
			else:
				lexicon[word] = 0
	return lexicon

def sentimental_analysis_by_lexicon(sentiment_lexicon, root_dir, content_file_name):
	# sentiment_lexicon:	lexicon
	# root_dir:				root directory
	# content_file_name: 	content.txt
	# rtype:				total sample, # postive, # negative, # calm 

	content_file_path = root_dir + '/' + content_file_name
	postive_file_path = root_dir + '/' + "positive.txt"
	negative_file_path = root_dir + '/' + "negative.txt"
	calm_file_path	=	root_dir + '/' + "calm.txt"
	seged_content_file_path = root_dir + '/seged_' + content_file_name

	with open(content_file_path, 'r') as file, 				\
		open(postive_file_path, 'w') as positive_file, 		\
		open(negative_file_path, 'w') as negative_file, 	\
		open(calm_file_path, 'w') as calm_file, 			\
		open(seged_content_file_path, 'w') as seged_content_file:
		
		positive_count 	= 0
		negative_count 	= 0
		calm_count 	= 0

		for line in file:
			words = list(jieba.cut(line, cut_all=False))
			words = [word for word in words if word != ' ']
			seged_content = " ".join(words).encode('utf-8')
			
			score = sum([sentiment_lexicon.get(word, 0) for word in words])
			
			if score > 0:
				positive_count += 1
			if score < 0:
				negative_count += 1
			if score == 0:
				calm_count += 1
			seged_content_file.write(seged_content)

		total = positive_count + negative_count + calm_count
		
		print "LEX: "
		print "size: ", total
		print "positive: %.4f" % (positive_count * 1.0 / total)
		print "negative: %.4f" % (negative_count * 1.0 / total)
		print "calm: %.4f" % (calm_count * 1.0 / total)
		print
		
		return total, positive_count, negative_count, calm_count

def init_SVM_classifier(corpus):
	# corpus:	use which corpus to classify
	# rtype:	training lexicon

	domain = create_domain(corpus)
	train_samples = domain[0][:700] + domain[1][:700]
	test_samples = domain[0][700:] + domain[1][700:]
	default_lexicon = SVM_classify(train_samples, test_samples)[1]
	return default_lexicon

def sentimental_analysis_by_SVM(corpus, root_dir, content_file_name):
	# corpus:	use which corpus to classify
	# root_dir:	file directory
	# content_file_name:	the source file name
	# rtype:	total, positive, negtaive

	file_path = root_dir + '/' + content_file_name
	default_lexicon = init_SVM_classifier(corpus)
	input_documents = generate_documents(file_path, True)
	return run_SVM_classify(default_lexicon, input_documents)

def main_analysis(sentiment_lexicon, root_dir, content_file_name, result_file_name):
	#sentiment_lexicon:	sentiment_lex
	#root_dir:			root_dir
	#content_file_name:	file_name
	
	with open(root_dir + '/' + result_file_name, 'w') as output_file:
		lex_result = sentimental_analysis_by_lexicon(sentiment_lexicon, root_dir, content_file_name)
		
		svm_result = sentimental_analysis_by_SVM("stocks", root_dir, "seged_" + content_file_name)

		output_file.write("Lex:" + ",".join(map(str, lex_result)) + '\n')
		output_file.write("SVM:" + ",".join(map(str, svm_result)) + '\n')

		lex_result_percentage = [float("%.2f" % (num * 100.0 / lex_result[0])) for num in lex_result[1:]]
		svm_result_percentage = [float("%.2f" % (num * 100.0 / svm_result[0])) for num in svm_result[1:]]

		output_file.write("Percent:" + ",".join(map(str, lex_result_percentage + svm_result_percentage)) + '\n')
		return lex_result_percentage + svm_result_percentage
		