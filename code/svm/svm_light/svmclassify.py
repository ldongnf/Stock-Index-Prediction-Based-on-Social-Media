#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import subprocess
import math

def generate_lexicon(documents):
	# documents:	documents
	# rtype:		lexicon(word, word_index)
	words = []
	for doc in documents:
		words += doc.words.keys()
	words = set(words)
	lexicon = dict([(word, i + 1) for i, word in enumerate(words)])
	return lexicon
    
def create_SVM_text(documents, lexicon, output_path):
	# documents:	documents
	# lexicon:		lexicon
	# output_path:	output_file_path
	text=''
	for document in documents:
		if document.polarity == True:
			line = "+1 "
		else:
			line = "-1 "
		lexicon_pairs = [(lexicon[word], document.words[word]) for word in document.words if word in lexicon]
		lexicon_pairs.sort()
		for pair in lexicon_pairs:
			line += '%d:%d ' % (pair[0], pair[1])
		text += line + '\n'
	if len(text) > 0:
		with open(output_path, 'w') as output_file:
			output_file.write(text)
     
def create_results(test_samples):
	# test_samples: test_samples
	# rtype: data_size, positive, negative
	data_size = len(test_samples)
	with open('result.output','rb') as file:
		results = []
		true_classification = 0
		positive, negative = 0, 0
		if data_size == 0:
			return data_size, positive, negative
		for i, line in enumerate(file):
			score = float(line)
			if (test_samples[i].polarity == True and score > 0) or (test_samples[i].polarity == False and score < 0):
				true_classification += 1 
			distance = float(line)
			x0 = 1 / (1 + math.exp(abs(distance)))
			x1 = 1 / (1 + math.exp(-1 * abs(distance)))
			prob= x1 / (x0 + x1)
			if distance < 0:
				prob *= -1
			if prob > 0:
				positive += 1
			if prob < 0:
				negative += 1
			results.append(prob)
		accuracy = float(true_classification) / data_size
		positive_percentage = float(positive) / data_size
		negative_percentage = float(negative) / data_size
		
		print 'Size: ', data_size
		print 'Positive: %d %.4f' % (positive, positive_percentage)
		print 'Negative: %d %.4f' % (negative, negative_percentage)
		print 'accuracy is %.4f(%d/%d)' % (accuracy, true_classification, data_size)
	
	return data_size, positive, negative
    
def SVM_classify(train_samples, test_samples):
	# train_samples: 	train_samples
	# test_samples:	test_samples_samples
	# rtype:	rtype pf results: 	data_size, positive, negative
	#			lexicon:	train_sample lexicon
	
	svm_dir = "./svm/svm_light/"
	model_dir = "./models/"
	
	lexicon = generate_lexicon(train_samples)
	create_SVM_text(train_samples, lexicon, model_dir + 'svm_train.txt')
	create_SVM_text(test_samples, lexicon, model_dir + 'svm_test.txt')

	subprocess.call([svm_dir + "svm_learn", model_dir + "svm_train.txt", model_dir + "svm_train.model"], stdout=subprocess.PIPE)
	subprocess.call([svm_dir + "svm_classify", model_dir + "svm_test.txt", model_dir + "svm_train.model", "result.output"], stdout=subprocess.PIPE)
	return [create_results(test_samples), lexicon]

def run_SVM_classify(lexicon, input_documents):
	# lexicon:	trained lexicon
	# input_documents:	input docs
	# rtype: classify result

	svm_dir = "./svm/svm_light/"
	model_dir = "./models/"

	create_SVM_text(input_documents, lexicon, model_dir + 'input.txt')
	subprocess.call([svm_dir + "svm_classify", model_dir + "input.txt", model_dir + "svm_train.model", "result.output"], stdout=subprocess.PIPE)
	return create_results(input_documents)
