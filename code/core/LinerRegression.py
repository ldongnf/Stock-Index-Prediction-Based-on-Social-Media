#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import numpy as np
import os
import datetime
def PrepareLinerRegression(rootDir,dirName,saveFileName,realFileName):
	SumUpSAFiles(rootDir,dirName,saveFileName)
	MatchWithRealFile(rootDir,saveFileName,realFileName)
def MatchWithRealFile(rootDir,fileName,realFileName):
	realFile = open(rootDir + '\\' + realFileName)
	file = open(rootDir + '\\'+ fileName)
	tempfile = open(rootDir + '\\' + 'temp.txt','w')
	dateBuff = []

	for lines in realFile:
		year = int(lines[0:4])
		month = int(lines[4:6])
		day = int(lines[6:9])
		time = datetime.datetime(year, month, day) - datetime.timedelta(1)
		timestring = datetime.datetime.strftime(time,'%Y%m%d')
		dateBuff.append(timestring)
	print dateBuff
	
	for content in file:
		resDic,resML,date = content.split(' ')
		date = date[:-1]
		print date
		if date in dateBuff:
			tempfile.write(content)
	realFile.close()
	file.close()
	tempfile.close()
	os.remove(rootDir + '\\' + fileName)
	os.rename(rootDir + '\\' + 'temp.txt',rootDir + '\\'+ fileName)

	
def SumUpSAFiles(rootDir,dirName,saveFileName):
	for root,dirs,files in os.walk(rootDir+'\\'+dirName,topdown = True):
		fileNames = files
		break
	sortList = []
	for items in fileNames:
		sortList.append(int(items[:-4]))
	sortList.sort()
	print sortList
	
	saveFile = open(rootDir+'\\'+saveFileName,'w')
	for names in sortList:
		fileName = str(names)+'.txt'
		file  = open(rootDir+'\\'+dirName+'\\'+fileName)
		
		content = file.readlines()
		if len(content)<3:
			continue
		saveFile.write(content[1][:-1] + ' ' +content[2][:-1] + ' '+str(names) +'\n')
def CreateMatrix(rootDir,fileName):
	dicMatrix = []
	mlMatrix = []
	unit = []
	file = open(rootDir + '\\' + fileName)
	content = file.readlines()
	for item in content:
		dic,ml,date = item.split(' ')
		dicPos,dicNeg,dicCalm = dic.split(',')
		unit.append(float(dicPos))
		unit.append(float(dicNeg))
		unit.append(float(dicCalm))
		dicMatrix.append(unit)
		unit =  []
		
		mlPos,mlNeg= ml.split(',')
		unit.append(float(mlPos))
		unit.append(float(mlNeg))
		mlMatrix.append(unit)
		unit = []
	return dicMatrix,mlMatrix

def GetCoeffientMatrix(MatrixCollection,MatrixReal):
	x =np.matrix(MatrixCollection,dtype=np.float64)
	y =np.matrix(MatrixReal,dtype=np.float64).T
	b=(x.T*x).I*x.T*y
	print u"参数项矩阵为\n{0}".format(b)
	i=0
	cb=[]
	while  i<len(MatrixCollection[0]):
		cb.append(b[i,0])
		i+=1
	temp_e=y-x*b
	mye=temp_e.sum()/temp_e.size
	e=np.matrix([mye,mye,mye]).T
	cb.append(mye)
	return cb

def MergeMatrix(dicMatrix,mlMatrix,realMatrix):
	unit = []
	dicMLMatrix = []
	for i in range(0,len(realMatrix)):
		unit.append(dicMatrix[i][0])
		unit.append(dicMatrix[i][1])
		unit.append(dicMatrix[i][2])
		unit.append(mlMatrix[i][0])
		unit.append(mlMatrix[i][1])
		dicMLMatrix.append(unit)
		unit = []
	return dicMLMatrix


def CreatPredicateValue(dicCoeffient,mlCoeffient,dicMLCoeffient,dicMatrix,mlMatrix,dicMLMatrix,realMatrix,dates,saveFilePath):
	file = open(saveFilePath,'w')
	for i in range(0,len(realMatrix)):
		mlPredicateValue = mlCoeffient[0]*mlMatrix[i][0]+mlCoeffient[1]*mlMatrix[i][1]+mlCoeffient[2]
		dicPredicateValue = dicCoeffient[0]*dicMatrix[i][0]+dicCoeffient[1]*dicMatrix[i][1]+dicCoeffient[2]*dicMatrix[i][2]+dicCoeffient[3]
		mldicPredicateValue = dicMLCoeffient[0]*dicMLMatrix[i][0]+dicMLCoeffient[1]*dicMLMatrix[i][1]+dicMLCoeffient[2]*dicMLMatrix[i][2]+dicMLCoeffient[3]*dicMLMatrix[i][3]+dicMLCoeffient[4]*dicMLMatrix[i][4]+dicMLCoeffient[5]
		file.write(str(realMatrix[i])+ ' '+'%.2f'%mlPredicateValue + ' ' + '%.2f'%dicPredicateValue +' '  +'%.2f'%mldicPredicateValue+' ' +dates[i])
	file.close()

def CreateRealMatrix(rootDir,fileName):
	realMatrix = []
	dates = []
	file = open(rootDir + '\\' + fileName)
	content = file.readlines()
	for lines in content:
		date,realStockValue = lines.split(' ')
		dates.append(date+'\n')
		realStockValue = realStockValue[:-1]
		realMatrix.append(float(realStockValue))
	return realMatrix,dates
def LingerRegressionPredicate(rootDir,sumFileName,realFileName,saveFilePath,trainSampleLength):
	dicMatrix,mlMatrix = CreateMatrix(rootDir,sumFileName)
	realMatrix,dates = CreateRealMatrix(rootDir,realFileName)
	dicMLMatrix = MergeMatrix(dicMatrix,mlMatrix,realMatrix)
	mlCoeffient = GetCoeffientMatrix(mlMatrix[:trainSampleLength],realMatrix[:trainSampleLength])
	dicCoeffient = GetCoeffientMatrix(dicMatrix[:trainSampleLength],realMatrix[:trainSampleLength])
	dicMLCoeffient = GetCoeffientMatrix(dicMLMatrix[:trainSampleLength],realMatrix[:trainSampleLength])
	CreatPredicateValue(dicCoeffient,mlCoeffient,dicMLCoeffient,dicMatrix,mlMatrix,dicMLMatrix,realMatrix,dates,saveFilePath)
	print dicCoeffient
	print mlCoeffient
	print dicMLCoeffient


if __name__ == "__main__":
	
	PrepareLinerRegression(r'E:\stock\Result',r'LinerRegression','sum.txt','real.txt')
	LingerRegressionPredicate(r'E:\stock\Result','sum.txt','real.txt',r'E:\stock\Result\res2.txt',-2)
	#SumUpSAFiles(r'E:\stock\Result',r'LinerRegression','sum.txt')
	#MatchWithRealFile(r'E:\stock\Result','sum.txt','real.txt')
