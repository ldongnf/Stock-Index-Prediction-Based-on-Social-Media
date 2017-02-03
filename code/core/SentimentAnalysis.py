#!/usr/bin/env python
#-*- coding: utf8 -*-
import jieba
import os
import FileManage
import DateUnification
import SegFile
import ML
def SentimentAnalysisAndCreatResult(rootDir,dictionaryPath,sourceFileName,AnalysisMode):
	dictionary = GenerateDictionary(dictionaryPath)
	segFileName = 'segres.txt'
	saveFileName = 'res.txt'
	for root,dirs,files in os.walk(rootDir,topdown = True):
		dirNamedByDate = dirs
		break
	print dirNamedByDate
	for dirDates in dirNamedByDate:
		dirPath = rootDir+'\\'+dirDates
		if AnalysisMode == "ADD":
			if os.path.exists(dirPath+'\\'+saveFileName):
				print dirPath + '	'+saveFileName + " existed"
				continue
		
		saveFile = open(dirPath+'\\'+saveFileName,"w")
		
		dirs = []
		dirs = FileManage.GetDirPathsForGenerall(dirPath,r'generall_res')
		dirs += FileManage.GetDirPathsForSingle(dirPath,r'\d')
		
		saveFile.write(dirDates+'\n')
		saveFile.write("stock"+'\n')
		saveFile.write("DIC(dataSize,positive,negative,calm)"+'\n')
		saveFile.write("ML(dataSize,positive,negative)"+'\n')
		for dir in dirs:
			for root,dirs,files in os.walk(dir,topdown = True):
				names = dirs
				break
			resDic = AnalysisByDictionary(dictionary,dir,sourceFileName)
			SegFile.FileSegement(dir,sourceFileName,segFileName)
			resML =  ML.AnalysisByMachineLearning("stocks",dir,segFileName)
			
			SegFile.FileSegement(dir,'Pos.txt','Posseg.txt')
			resMLPos = ML.AnalysisByMachineLearning("stocks",dir,'Posseg.txt')
			SegFile.FileSegement(dir,'Neg.txt','Negseg.txt')
			resMLNeg = ML.AnalysisByMachineLearning("stocks",dir,'Negseg.txt')
			
			dataSize = int(resML[0])
			postiveSize = int(resMLPos[1])
			negativeSize = int(resMLNeg[2])
			calmSize = dataSize - postiveSize - negativeSize
			allRes = str(dataSize) + ',' + str(postiveSize) + ','+str(negativeSize)+','+str(calmSize)
			
			saveFile.write(names[0].decode('GBK').encode('utf-8')+'\n')
			dicRes = ""
			for figure in resDic:
				dicRes += str(figure) + ','
			dicRes = dicRes[:-1]
			mlRes=""
			for figure in resML:
				mlRes += str(figure) + ','
			mlRes = mlRes[:-1]
			saveFile.write(dicRes+'\n')
			saveFile.write(mlRes+'\n')
			saveFile.write(allRes+'\n')
		saveFile.close()
	return saveFileName

def AnalysisByDictionary(dictionary,fileDir,fileName):
	contentFile = open(fileDir +'\\'+ fileName,'r')
	calm = 0
	positive = 0
	negative = 0
	count = 0
	NegFileName = 'Neg.txt'
	PosFileName = 'Pos.txt'
	CalmFileName = 'Cal.txt'
	negFile = open(fileDir + '\\' + NegFileName,'w')
	posFile = open(fileDir + '\\' + PosFileName,'w')
	calFile = open(fileDir + '\\' + CalmFileName,'w')
	for line in contentFile:
		sentiment = SegAnalysis(line,dictionary,False)
		count = count + 1
		if sentiment == 0:
			calFile.write(line)
			calm = calm + 1
		if sentiment > 0:
			posFile.write(line)
			positive = positive + 1
		if sentiment < 0:
			negFile.write(line)
			negative = negative + 1
		#print '#',count
	if count == 0:
		return count,positive,negative,calm
	percentage_p = positive * 1.0/count
	percentage_n = negative *1.0/count
	percentage_c = calm *1.0/count
	negFile.close()
	posFile.close()
	calFile.close()
	
	contentFile.close()
	print 'Size: ',count
	print 'Positive: ',positive,percentage_p
	print 'Negative: ',negative,percentage_n
	print 'Calm:     ' ,calm,percentage_c
	return count,positive,negative,calm

def SegAnalysis(dataContent,sentimentDictionary,segModel):
	res = 0
	segList = jieba.cut(dataContent, cut_all = segModel)
	for words in segList:
		res = res + SearchDictionary(sentimentDictionary,words)
	return res

def GenerateDictionary(dictionaryPath):
	dictionary = {}
	dictionaryFile = open(dictionaryPath,'r')
	for line in dictionaryFile:
		if line:
			if line == '\n':
				continue
			words,sentiment = line.split('	')
			words = words.decode('utf-8')
			dictionary[words] = sentiment
	dictionaryFile.close()
	return dictionary
	
def SearchDictionary(sentimentDictionary, keyWord):
	if keyWord in sentimentDictionary:
		res = sentimentDictionary[keyWord]
		if res == 'P\n':
			return 1
		if res == 'N\n':
			return -1
	return 0
	
if __name__ == "__main__":
	#dictionaryPath ="E://testpack//org.txt"
	#dictionaryPath ="E://testpack//new.txt"
	dictionaryPath =r"E:\stock\code\dic\Dictionary\mix.txt"
	nameFileName = 'name.txt'
	contentFileName = 'content.txt'
	dateFileName = 'date.txt'
	#rootDir = 'E://Datas'
	predicateDate ='2016-03-08'

	fileDir="E://Datas"
	#fileName="NCD.txt"
	#predicateDate ='2016-03-04'
	#SetPredicateDate(fileDir,fileName,predicateDate)
	dictionary = GenerateDictionary(dictionaryPath)
	AnalysisByDictionary(dictionary,r'D:\stock\Data\20160328\generall','content_all.txt')
	#GenerateDictionary(dictionaryPath)