#!/usr/bin/env python
#-*- coding: utf8 -*-
import os
import time
import re
import FileManage
import DateUnification
def RemoveDuplicates(fileDir,nameFileName,contentFileName,dateFileName,removeModel,similarityPercentage):
	NCFile = 'NC.txt'
	NCDFile = 'NCD.txt'
	
	ncFileTemp = 'nc_temp.txt'
	ncdFileTemp = 'ncd_temp.txt'
	dFileTemp = 'd_temp.txt'
	RemoveFirstCharacter(fileDir,contentFileName)
	FileManage.MergeFile(fileDir,nameFileName,contentFileName,ncFileTemp)
	
	DateUnification.TimeBackward(fileDir,dateFileName)
	DateUnification.DateSeparate(fileDir,dateFileName,dFileTemp)
	
	FileManage.MergeFile(fileDir,dFileTemp,ncFileTemp,ncdFileTemp)
	indexCollection = RemoveInPKFile(fileDir,ncdFileTemp,removeModel,similarityPercentage)

	RemoveByIndex(indexCollection,fileDir,nameFileName)
	RemoveByIndex(indexCollection,fileDir,contentFileName)
	RemoveByIndex(indexCollection,fileDir,dateFileName)
	
	
	FileManage.MergeFile(fileDir,nameFileName,contentFileName,NCFile)
	FileManage.MergeFile(fileDir,dateFileName,NCFile,NCDFile)
	
	os.remove(fileDir + '\\' + ncFileTemp)
	os.remove(fileDir + '\\' + ncdFileTemp)
	os.remove(fileDir + '\\' + dFileTemp)
	os.remove(fileDir + '\\' + NCFile)
	
	return NCDFile

def RemoveFirstCharacter(fileDir,nameFileName):
	filePath = fileDir+'\\'+nameFileName
	file = open(filePath)
	tempFileName = 'RFN.txt'
	tempFilePath = fileDir + '\\' + tempFileName
	tempFile = open(tempFilePath,'w')
	for line in file:
		res =  line.find(':')
		if res == 0:
			tempFile.write(line[1:])
		else:
			tempFile.write(line)
	tempFile.close()
	file.close()
	os.remove(filePath)
	os.rename(tempFilePath,filePath)
def RemoveInPKFile(fileDir,fileName,removeModel,similarityPercentage):
	print "removeModel",removeModel
	if removeModel =='A':
		print 'A'
		return RemoveAll(fileDir,fileName)
	else:
		print similarityPercentage
		return RemoveByPercentage(fileDir,fileName,similarityPercentage)
def RemoveByPercentage(fileDir,fileName,similarityPercentage):
	buff = []
	compareBuff = []
	filePath = fileDir + '//'+fileName
	file=open(filePath,"r")
	indexCollection = []
	index = 0
	pos = 0
	res = -1
	for content in file:
		pos = int(len(content)* similarityPercentage)
		keySentence = content[:pos]+'\n'
		if keySentence in compareBuff:
			index = index + 1
			continue
		else:
			indexCollection.append(index)
			compareBuff.append(keySentence)
			buff.append(content)
			index = index + 1
	print "Input Items: ",str(index)
	print "Reoved Items: ",str(index - len(indexCollection))
	tempFilePath = fileDir + "//pkIMP.txt"
	tempFile = open(tempFilePath,"w")
	tempFile.writelines(buff)
	tempFile.close()
	file.close()
	os.remove(filePath)
	os.rename(tempFilePath,filePath)
	return indexCollection

def RemoveAll(fileDir,fileName):
	buff=[]
	filePath = fileDir + '//'+fileName
	file=open(filePath,"r")
	indexCollection = []
	index = 0
	for content in file:
		if content in buff:
			index = index + 1
			continue
		else:
			indexCollection.append(index)
			buff.append(content)
			index = index + 1
	print "Input Items: ",str(index)
	print "Reoved Items: ",str(index - len(indexCollection))
	tempFilePath = fileDir + "//pka.txt"
	tempFile = open(tempFilePath,"w")
	tempFile.writelines(buff)
	tempFile.close()
	file.close()
	os.remove(filePath)
	os.rename(tempFilePath,filePath)
	return indexCollection
def RemoveByIndex(indexCollection,fileDir,fileName):
	#indexCollection 序号列表 
	#fileDir 文件路径
	#fileName 文件名
	if len(indexCollection) == 0:
		return
	buff = []
	filePath = fileDir + '//' + fileName;
	file = open(filePath, "r")
	index = 0
	j = 0
	for date in file:
		if index == indexCollection[j]:
			buff.append(date)
			j = j + 1
		index = index + 1
		if len(indexCollection) == j:
			break

	tempFilePath = fileDir + "//other.txt"
	tempFile = open(tempFilePath,"w")
	tempFile.writelines(buff)
	tempFile.close()
	file.close()
	os.remove(filePath)
	os.rename(tempFilePath,filePath)

def RemoveNoise(rootDir,resFileName):
	#noiseList = [r'一盘面',r'桌面',r'博文',r'转载',r'壳子','新表',r'手表',r'棋盘','象棋',r'围棋',r'钟面','料酒','面粉',r'联赛','外观',r'非农',r'问卷',r'饺子',r'饿',r'基金',r'豆油',r'白银',r'原油',r'期货',r'盐',r'大盘鸡',r'投票',r'好吃',r'一大盘',r'视频',r'删除',r'转发',r'文章',r'QQ群',r'微信']#
	noiseList = []
	noiseList = GenerateNoiseList(r'.\Noise','noise.txt')
	patterns = []
	index = 0
	indexCollection = []
	tempFilename = 'noise.txt'
	res = False
	for words in noiseList:
		patterns.append(re.compile(words))
	sourceFilePath = rootDir+'//'+resFileName
	tempFilePath = rootDir+'//'+tempFilename
	sourceFile = open(sourceFilePath)
	tempFile = open(tempFilePath,"w")
	for line in sourceFile:
		for keyWord in patterns:
			res = keyWord.search(line)
			if res:
				break;
		if not res:
			indexCollection.append(index)
			tempFile.write(line)
		index = index + 1
	print "Input Items: ",str(index)
	print "Reoved Noisy Items: ",str(index - len(indexCollection))
	tempFile.close()
	sourceFile.close()
	os.remove(sourceFilePath)
	os.rename(tempFilePath,sourceFilePath)
	return indexCollection
def GenerateNoiseList(fileDir,fileName):
	noiseList = []
	file = open(fileDir + '\\' + fileName)
	for lines in file:
		noiseList.append(lines[:-1])
	return noiseList
def SingleStockFilter(rootDir,saveDir,FilterValue):
	for root,dirs,files in os.walk(rootDir,topdown = True):
		resfileNames = files
		break
	ResUnit = []
	
	for fileName in resfileNames:
		file = open(rootDir + '\\' + fileName)
		savefile = open(saveDir + '\\' + fileName,"w")
		content = file.readlines()
		
		savefile.write(fileName[:-4]+'\n')
		savefile.write("stock"+'\n')
		savefile.write("DIC(dataSize,positive,negative,calm)"+'\n')
		savefile.write("ML(dataSize,positive,negative)"+'\n')
		
		Filter = []
		for i in range(1,(len(content)-4)/4+1):
			ResUnit.append(content[4*i])
			ResUnit.append(content[4*i+1])
			ResUnit.append(content[4*i+2])
			ResUnit.append(content[4*i+3])
			
			
			if content[4*i] in Filter:
				ResUnit = []
				continue
			
			Filter.append(content[4*i])
			size,postive = ResUnit[1].split(',',1)
			
			if int(size) < FilterValue:
				ResUnit = []
				continue
			
			for items in ResUnit:
				savefile.write(items)
				ResUnit = []
		Filter = []
def ChangeToPercentageVersion(rootDir,saveDir):
	for root,dirs,files in os.walk(rootDir,topdown = True):
		resfileNames = files
		break
	
	ResUnit = []
	ResList = []
	ResAll = []
	for fileName in resfileNames:
		file = open(rootDir + '\\' + fileName)
		savefile = open(saveDir + '\\' + fileName,"w")
		content = file.readlines()

		for i in range(1,(len(content)-4)/4+1):
			ResUnit.append(content[4*i])
			ResUnit.append(content[4*i+1])
			ResUnit.append(content[4*i+2])
			ResUnit.append(content[4*i+3])
			
			
			size,postive = ResUnit[1].split(',',1)
			

			dicSize,dicPos,dicNeg,dicCalm = ResUnit[1].split(',')
			dicCalm = dicCalm[:-1]
			
			dicPosPercent = int(dicPos)*1.0/int(dicSize)*100
			dicNegPercent = int(dicNeg)*1.0/int(dicSize)*100
			dicCalmPercent = int(dicCalm)*1.0/int(dicSize)*100
			
			mlSize,mlPos,mlNeg = ResUnit[2].split(',')
			mlNeg = mlNeg[:-1]
			
			mlPosPercent = int(mlPos)*1.0/int(mlSize)*100
			mlNegPercent = int(mlNeg)*1.0/int(mlSize)*100
			
			mixSize,mixPos,mixNeg,mixCalm = ResUnit[3].split(',')
			mixCalm = mixCalm[:-1]
			
			mixPosPercent = int(mixPos)*1.0/int(mixSize)*100
			mixNegPercent = int(mixNeg)*1.0/int(mixSize)*100
			mixCalmPercent = int(mixCalm)*1.0/int(mixSize)*100

			savefile.write(ResUnit[0][:-1]+','+str(size)+'\n')
			savefile.write("%.2f,%.2f,%.2f\n"%(dicPosPercent,dicNegPercent,dicCalmPercent))
			savefile.write("%.2f,%.2f\n"%(mlPosPercent,mlNegPercent))
			savefile.write("%.2f,%.2f,%.2f\n"%(mixPosPercent,mixNegPercent,mixCalmPercent))
			
			ResList.append(ResUnit)
			ResUnit = []
		
		ResAll.append(ResList)
		ResList = []
	return ResList
if __name__ == "__main__":
	fileDir = 'E://test//2'
	fileName = "resfile.txt"
	similarityPercentage = 1
	#RemoveByPercentage(fileDir,fileName,0.5)
	#print GenerateNoiseList(r'.\Noise','noise.txt')
	#RemoveDuplicates(fileDir,"name_all.txt","content_all.txt","date_all.txt",'B',0.5)
	#RemoveNoise(fileDir,fileName)
	#RemoveFirstCharacter(fileDir,'content_all.txt')
	#SeparateFile(fileDir,fileName,'name_all.txt','content_all.txt','date_all.txt')
	SingleStockFilter(r'E:\stock\Result\SAFile',r'E:\stock\Result\FilteredByValue',20)
	ChangeToPercentageVersion(r'E:\stock\Result\FilteredByValue',r'E:\stock\Result\LinerRegression')

