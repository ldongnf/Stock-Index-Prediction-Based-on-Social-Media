#!/usr/bin/env python
#-*- coding: utf8 -*-
import DateUnification
import FileManage
import os
def SetDate(fileDir,DataFileName,predicateDate):
	dataSetTime = DateUnification.GetNewDateByDay(1,predicateDate)
	print "dataSetTime",dataSetTime
	resFileName = SetPredicateDate(fileDir,DataFileName,dataSetTime)
	nameFileName ="name_all.txt"
	contentFileName="content_all.txt"
	dateFileName="date_all.txt"
	FileManage.SeparateFile(fileDir,resFileName,nameFileName,contentFileName,dateFileName)
	DateUnification.TimeForward(fileDir,dateFileName)
	return contentFileName

def SetPredicateDate(fileDir,fileName,predicateDate,SetMode):
	dataFile = open(fileDir + '\\' + fileName,'r')
	resFileName = 'resfile.txt'
	if SetMode =="ADD":
		if os.path.exists(fileDir+'\\'+resFileName):
			print fileDir + '	'+ resFileName + " existed"
			return resFileName
	resFile = open(fileDir + '\\' + resFileName,'w')
	for line in dataFile:
		res = line.find(predicateDate)
		if res == 0:
			resFile.write(line)
	resFile.close()
	dataFile.close()
	return resFileName
def SetDateSetByPredicateDate(rootDir,DataFileName,SetMode):
	nameFileName ="name_all.txt"
	contentFileName="content_all.txt"
	dateFileName="date_all.txt"
	dates = []
	for root,dirs,files in os.walk(rootDir,topdown = True):
		dates = dirs
		break
	dirs = []
	for date in dates:
		dataSetTime = date[:4]+'-'+date[4:6]+'-'+date[6:8]
		print dataSetTime
		dirs = FileManage.GetDirPathsForGenerall(rootDir+'\\'+date,r'generall_res')
		dirs += FileManage.GetDirPathsForSingle(rootDir+'\\'+date,r'\d')
		for dir in dirs:
			resFileName = SetPredicateDate(dir,DataFileName,dataSetTime,SetMode)
			FileManage.SeparateFile(dir,resFileName,nameFileName,contentFileName,dateFileName)
			DateUnification.TimeForward(dir,dateFileName)
	return contentFileName

if __name__ == "__main__":
	SetDateSetByPredicateDate(r"E:\stock\Data","NCD.txt")