#!/usr/bin/env python
#-*- coding: utf8 -*-
from __future__ import division
import numpy as np
import os
import datetime
import support
from svm.lib_svm.svmutil import *

class Indicator:
	def __init__(self, values):
		[self.stock_index, self.amount, self.tendency, self.MACD, self.KDJK, self.KDJD, self.KDJJ] = values
		self.normalize(10)

	def normalize(self, coefficient):
		self.stock_index = str(int(float(self.stock_index) / coefficient))
		self.amount = str(int(float(self.amount) / coefficient))
		self.tendency = str(int(float(self.tendency) * coefficient))
		self.MACD = str(int(float(self.MACD) / coefficient))
		self.KDJK = str(int(float(self.KDJK) / coefficient))
		self.KDJD = str(int(float(self.KDJD) / coefficient))
		self.KDJJ = str(int(float(self.KDJJ) / coefficient))

	def to_list(self):
		return ["stockindex:" + self.stock_index, "amount" + self.amount, "tendency" + self.tendency, "MACD" + self.MACD, "KDJK" + self.KDJK, "KDJD" + self.KDJD, "KDJJ" + self.KDJJ]

class Sentiment:
	def __init__(self, values):
		[self.lex_positive, self.lex_negative, self.lex_calm, self.SVM_positve, self.SVM_negative] = values

	def to_list(self):
		return ["lexpos" + str(self.lex_positive), "lexneg" + str(self.lex_negative), "lexcalm" + str(self.lex_calm), "svmpos" + str(self.SVM_positve), "svmneg" + str(self.SVM_negative)]

	def display(self):
		print self.lex_positive, self.lex_negative, self.lex_calm, self.SVM_positve, self.SVM_negative

class DataPair:
	def __init__(self, features, stock_index):
		self.stock_index = stock_index
		self.features = features

def create_matrix(root_dir, input_file_name, real_file_name):
	# root_dir:	root_dir
	# file_name: source file
	# rtype: matrix of input data

	matrix = {}
	with open(root_dir + '/' + input_file_name, 'r') as input_file, \
		open(root_dir + '/' + real_file_name, 'r') as real_file:
		
		for line in real_file:
			key, value = line.rstrip().split(':')
			values = map(float, value.split())
			matrix[key] = [[values[0]]]
			
		for line in input_file:
			key, value = line.rstrip().split(':')
			date = datetime.datetime.strptime(key, "%Y-%m-%d")
			date += datetime.timedelta(days=1)
			date_str = date.strftime("%Y-%m-%d")
			if date_str in matrix:
				matrix[date_str] += [map(float, value.split())]
	input_matrix = [matrix[key][1] for key in sorted(matrix)]
	output_matrix = [matrix[key][0] for key in sorted(matrix)]
	
	return input_matrix, output_matrix

def get_coeffient(input_matrix, output_matrix):
	# input_matrix: X
	# output_matrix: Y
	# y = f(x)
	# rtype: coeffient

	x = np.matrix(input_matrix, dtype=np.float64)
	y = np.matrix(output_matrix, dtype=np.float64)
	coeffient = (x.T * x).I * x.T * y
	e = y - x * coeffient
	mean_e = e.sum() / e.size
	coeffient = np.vstack((coeffient, [mean_e]))
	return coeffient

def predicate(coeffient, input_matrix):
	# coeffient: a
	# input_matrix: x
	# y = ax
	# rtype: predicate value 

	x = np.matrix(input_matrix, dtype=np.float64)
	y = x * coeffient[:-1] + coeffient[-1]
	return y

def linear_regression(root_dir, input_file, output_file, train_sample_length):
	# root_dir: root_dir
	# input_file: file contains x
	# output_file: file contains y
	# train_sample_length: how many sample to train
	# rtype: return predicate value

	input_matrix, output_matrix = create_matrix(root_dir, input_file, output_file)
	coeffient = get_coeffient(input_matrix[:train_sample_length], output_matrix[:train_sample_length])
	return predicate(coeffient, input_matrix[train_sample_length:])

def generate_top_k_words(root_dir, target_file_name, num_words):
	# root_dir: root_dir
	# target_file_name: source file
	# num_words: top k

	directories = support.get_subdirs(root_dir)
	word_count = {}
	for directory in directories:
		with open(directory + '/' + target_file_name, 'r') as file:
			for line in file:
				words = line.strip().split()
				for word in words:
					word_count[word] = word_count.get(word, 0) + 1

	return set(sorted(word_count, key=word_count.get)[:num_words])

def generate_sentiment_words(sentiment_lexicon_file):
	# sentiment_lexicon_file: setiment_file_path

	with open(sentiment_lexicon_file, 'r') as file:
		return [line.strip().split()[0] for line in file]

def generate_tech_feature(root_dir, tech_file_name, group_window_length):
	# root_dir: root
	# tech_file_name: tech_file_path
	# group_window_length: group the tech figures

	original_tech_feature = {}
	with open(root_dir + '/' + tech_file_name, 'r') as real_file:
		for line in real_file:
			key, value = line.rstrip().split(':')
			values = map(float, value.split())
			tech = Indicator(values)
			original_tech_feature[key] = tech.to_list()
	tech_feature = {}
	orginal_keys = sorted(original_tech_feature.keys())
	for index, date in enumerate(orginal_keys[group_window_length-1:]):
		tech_feature[date] = [str(index+1) + value for index, key in enumerate(orginal_keys[index:index+group_window_length]) for value in original_tech_feature[key] ]
	return tech_feature

def generate_sentiment_feature(root_dir, sentiment_result_file):
	# root_dir: root_dir
	# sentiment_result_file: sentiment results

	sentiment_feature = {}
	with open(root_dir + '/' + sentiment_result_file, 'r') as sentiment_file:
		for line in sentiment_file:
			date, values = line.rstrip().split(':')
			sentiment_feature[date] = Sentiment(map(float, values.split())).to_list()
	return sentiment_feature

def generate_sentiment_word_feature(root_dir, target_file_name):
	# root_dir: root_dir
	# target_file_name: text content file

	sentiment_words = generate_sentiment_words("./lexicon/dictionary.txt")
	directories = support.get_subdirs(root_dir)
	
	sentiment_word_feature = {}
	for directory in directories:
		key = directory.split('/')[-1]
		date = key[:4] + '-' + key[4:6] + '-' + key[6:8]
		with open(directory + '/' + target_file_name, 'r') as file:
			raw_words = set(map(str.rstrip, file.read().split()))
			words = [word for word in raw_words if word in sentiment_words]
		sentiment_word_feature[date] = words

	return sentiment_word_feature

def generate_word_feature(root_dir, target_file_name, num_words):
	# root_dir: root
	# target_file_name: content txt file
	# num_words: top K words

	frequent_words = generate_top_k_words(root_dir, target_file_name, num_words)
	directories = support.get_subdirs(root_dir)
	
	word_feature = {}
	for directory in directories:
		key = directory.split('/')[-1]
		date = key[:4] + '-' + key[4:6] + '-' + key[6:8]
		with open(directory + '/' + target_file_name, 'r') as file:
			raw_words = set(map(str.rstrip, file.read().split()))
			words = [word for word in raw_words if word in frequent_words]
		word_feature[date] = words

	return word_feature

def assign_weight(feature, weight):
	# feature: feature
	# weight: weight of feature

	weighted_form = {}
	for key in feature:
		weighted_form[key] = {value:weight for value in feature[key]}
	return weighted_form

def merge_feature(tech_feature, features):
	# tech_feature: base feature to create dict
	# feature: other features map to tech_feature

	new_feature = dict(tech_feature.items())
	for feature in features:
		for key in feature:
			if key in new_feature:
				new_feature[key] = dict(new_feature[key].items() + feature[key].items())
	return new_feature

def generate_features(root_dir, sentiment_result_file, tech_file_name, target_file_name, num_words):
	# root_dir: root_dir
	# sentiment_result_file: sentiment analysis result 
	# tech_file_name: tech indicator file
	# target_file_name: content text file
	# num_words: top k words

	tech_feature = generate_tech_feature(root_dir, tech_file_name, 3)
	tech_feature_weighted = assign_weight(tech_feature, 9)

	sentiment_feature = generate_sentiment_feature(root_dir, sentiment_result_file)
	sentiment_feature_weighted = assign_weight(sentiment_feature, 9)
	
	word_feature = generate_word_feature(root_dir, target_file_name, num_words)
	word_feature_weighted = assign_weight(word_feature, 1)
	
	sentiment_word_feature = generate_sentiment_word_feature(root_dir, target_file_name)
	sentiment_word_feature_weighted = assign_weight(sentiment_word_feature, 1)

	return merge_feature(tech_feature_weighted, [sentiment_feature_weighted, word_feature_weighted, sentiment_word_feature_weighted])	

def generate_stock_index(root_dir, tech_file_name):
	# root_dir: root
	# tech_file_name: tech indicator

	stock_index = {}
	with open(root_dir + '/' + tech_file_name, 'r') as real_file:
		for line in real_file:
			key, value = line.rstrip().split(':')
			values = map(float, value.split())
			stock_index[key] = values[0]
	return stock_index

def generate_data_pairs(features, root_dir, tech_file_name, train_sample_length):
	# features: features
	# root_dir: root
	# tech_file_name: tech files
	# train_sample_length: top k

	stock_index = generate_stock_index(root_dir, tech_file_name)
	y_values = [stock_index[key] for key in sorted(stock_index.keys())]
	x_values = [features[key] for key in sorted(features.keys())]
	data_pairs = [DataPair(x, y) for x,y in zip(x_values, y_values)]
	return data_pairs

def convert_to_svm_input(data_pairs):
	# data_pairs: Data pair

	features = []
	for data_pair in data_pairs:
		features += data_pair.features.keys()
	features=set(features)

	lexicon={}
	for index, feature in enumerate(features):
		lexicon[feature] = index + 1

	x, y = [], []
	for data_pair in data_pairs:
		pairs = dict([(lexicon[feature], data_pair.features[feature]) for feature in data_pair.features.keys() if feature in lexicon])
		x.append(pairs)
		y.append(data_pair.stock_index)
	return [x, y]

def svm_regression(root_dir, sentiment_result_file, tech_file_name, stock_index_file_name, target_file_name, num_words, train_sample_length):
	# root_dir: root
	# sentiment_result_file: sentimen analysis file
	# tech_file_name: tech indicator file
	# stock_index_file_name: stock index
	# target_file_name: content text file
	# num_words: top k
	# train_sample_length: num of train samples
	
	features = generate_features(root_dir, sentiment_result_file, tech_file_name, target_file_name, num_words)
	data_pairs = generate_data_pairs(features, root_dir, stock_index_file_name, train_sample_length)

	x, y = convert_to_svm_input(data_pairs)
	train_samples = [x[:train_sample_length], y[:train_sample_length]]
	test_samples = [x[train_sample_length:], y[train_sample_length:]]

	prob = svm_problem(train_samples[1], train_samples[0])
	param = svm_parameter('-s 3 -t 0')
	model = svm_train(prob, param)
	svm_save_model('./models/svr.model',model)
	p_labels, p_acc, p_vals = svm_predict(test_samples[1], test_samples[0], model)
	values =  [round(value, 2) for value in p_labels]
	return values
