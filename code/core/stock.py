#!/usr/bin/env python
#-*- coding: utf8 -*-
import DataPreprocess
import SentimentAnalysis
import SelectDate
import time
import SegFile
import ML
nameFileName = 'name.txt'
contentFileName = 'content.txt'
dateFileName = 'date.txt'
#rootDir = r'E:\Data'
predicateDate =' '
#dictionaryPath =r"dictionary\org.txt"
#dictionaryPath =r"dictionary\new.txt"
dictionaryPath =r"dictionary\mix.txt"

rootDir = raw_input()
predicateDate = raw_input()
#predicateDate = '2016-03-10'
start = time.clock()
dataFile = DataPreprocess.DataEngine(rootDir,nameFileName,contentFileName,dateFileName,"ADD")
dataFile = 'NCD.txt'
end_DP = time.clock()
resFileName = 'content_all.txt'
resFileName = SelectDate.SetDate(rootDir,dataFile,predicateDate)
segFileName = 'segres.txt'
SegFile.FileSegement(rootDir,resFileName,segFileName)
#ML.test('stocks')
ML.AnalysisByMachineLearning("stocks",rootDir,segFileName)

if SentimentAnalysis.AnalysisByDictionary(dictionaryPath,rootDir,resFileName):
	print 'success'
else:
	print 'date out of range'
end_SA = time.clock()
print "DPtime: %f s" % (end_DP - start)
print "SAtime: %f s" % (end_SA - end_DP)