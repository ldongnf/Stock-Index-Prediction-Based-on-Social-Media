#! /usr/bin/env python
#coding=utf-8
from __future__ import division
from document import createDomain,readFromFile
from svmclassify import svm_classify 

def test(area):
	domain=createDomain(area)
	trains=domain[0][200:]+domain[1][200:]
	tests=domain[0][:200]+domain[1][:200]
	svm_classify(trains,tests)

def AnalysisByMachineLearning(area,fileDir,fileName):
	filePath = fileDir + '\\' + fileName
	domain=createDomain(area)
	trains=domain[0][:700]+domain[1][:700]
	tests=readFromFile(filePath,True)
	return svm_classify(trains,tests)

if __name__ == "__main__":
	rootDir = 'E://Data'
	segFileName = 'segres.txt'
	filePath = rootDir + '\\' +segFileName
	AnalysisByMachineLearning('stocks',rootDir,segFileName)
	