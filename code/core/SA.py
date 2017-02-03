#!/usr/bin/env python
#-*- coding: utf8 -*-
import os
import DataPreprocess
import SentimentAnalysis
import SelectDate
import FileManage
import DataFilter
import LinerRegression
import time

root =r'../../'
dataDir = root + 'Data'
resultDir = root + 'Result'
print dataDir

'''
list = ['content.txt','name.txt','date.txt','resDic.txt','resML.txt','res.txt','NCD.txt','date_all.txt','name_all.txt','Neg.txt','Pos.txt','content_all.txt','Cal.txt','resfile.txt','segres.txt','Negseg.txt','Posseg.txt']
FileManage.FileCleaner(dataDir,list)

engineBatStart = time.clock()
fileName =  DataPreprocess.EngineBat(dataDir,"ADD")
engineBatEnd = time.clock()
print "EngineFinished"

fileName ='NCD.txt'

setDateStart = time.clock()
resfileName = SelectDate.SetDateSetByPredicateDate(dataDir,fileName,'ADD')
setDateEnd = time.clock()
print "SelectDateFinished"

resfileName='content_all.txt'
SAStart = time.clock()
SentimentAnalysis.SentimentAnalysisAndCreatResult(dataDir,r"dictionary\new.txt",resfileName,'ADD')
SAEnd = time.clock()
print "SentimentAnalysisFininshed"
'''

SumResStart = time.clock()
FileManage.SumResultFile(dataDir,resultDir + r'\SAFile','res.txt','re')
SumResEnd = time.clock()
print "SumResultFileFinished"

SingleFilterStart = time.clock()
DataFilter.SingleStockFilter(resultDir + r'\SAFile',resultDir+r'\FilteredByValue',20)
SingleFilterEnd = time.clock()
print "SingleFinished"

ChangeStart = time.clock()
DataFilter.ChangeToPercentageVersion(resultDir+r'\FilteredByValue',resultDir+'\LinerRegression')
ChangeEnd = time.clock()
print "VersionFinished"

PrepareStart = time.clock()
LinerRegression.PrepareLinerRegression(resultDir,r'LinerRegression','sum.txt','real.txt')
PrepareEnd = time.clock()
print "linerFished"

LinerRegressionStart = time.clock()
LinerRegression.LingerRegressionPredicate(resultDir,'sum.txt','real.txt',resultDir + r'\predicateValues.txt',-2)
LinerRegressionEnd = time.clock()
print "LinerRegressionFished"
'''
print "Eingine Time: " + str(engineBatEnd-engineBatStart)
print "SetDate Time: " + str(setDateEnd-setDateStart)

print "SA Time: " + str(SAEnd-SAStart)
print "SumRes Time: " + str(SumResEnd-SumResStart)

print "SingleFilter Time: " + str(SingleFilterEnd-SingleFilterStart)
print "ChangeVersion Time: " + str(ChangeEnd-ChangeStart)
print "Prepare Time: " + str(PrepareEnd-PrepareStart)

print "LinerRegression Time: " + str(LinerRegressionEnd-LinerRegressionStart)

'''



