#!/usr/bin/env python
#-*- coding: utf8 -*-
import DataParser
import DataFilter
import SelectDate
import re
import os
import FileManage
def DataEngine(rootDir,nameFileName,contentFileName,dateFileName,parserMode):
#rootDir 			root file
#nameFileName 		name file
#contentFileName	content file
#dateFileName		date file
	sumFileName = 'name_all.txt'
	sumFileContent = 'content_all.txt'
	sumFileDate = 'date_all.txt'
	print 'Generate Engine:	'
	FileManage.FilePrepare(rootDir,sumFileName)
	FileManage.FilePrepare(rootDir,sumFileContent)
	FileManage.FilePrepare(rootDir,sumFileDate)
	fileDirs = []
	fileDirs = FileManage.GetFilePaths(rootDir,r'\d.html')
	print 'FilePath: ',fileDirs
	print 'Generate Parser:'
	size = 0
	for dir in fileDirs:
#Parser
		DataParser.ParserNCD(dir,nameFileName,contentFileName,dateFileName,parserMode)
#Copy to the root dir
		size = size + FileManage.CopyFile(rootDir + '\\' + sumFileName,dir+ '\\' +nameFileName)
		FileManage.CopyFile(rootDir + '\\' + sumFileContent,dir+ '\\' +contentFileName)
		FileManage.CopyFile(rootDir + '\\' + sumFileDate,dir+ '\\' +dateFileName)
	print 'DataSize: ',size
	print 'Generate Filter:'
#Remove Duplicates using name file, content file, date file
	print 'Step1: remove Duplicates:'
	resFileName = DataFilter.RemoveDuplicates(rootDir,sumFileName,sumFileContent,sumFileDate,'B',0.5)
#Remove noises
	print 'Step2: remove Noises:',resFileName
	DataFilter.RemoveNoise(rootDir,resFileName);
	print 'Data Ready!'
	return resFileName

def EngineBat(rootDir,parserMode):
	nameFileName = 'name.txt'
	contentFileName = 'content.txt'
	dateFileName = 'date.txt'
	dirs = []
	dirs = FileManage.GetDirPathsForGenerall(rootDir,r'generall_res')
	dirs += FileManage.GetDirPathsForSingle(rootDir,r'\d')
	print dirs
	for dir in dirs:
		fileName = DataEngine(dir,nameFileName,contentFileName,dateFileName,parserMode)
	return fileName
if __name__ == "__main__":
	#root = r'..\..\Data\20160321'
	root =r'E:\stock\Data\data'
	fileName =  EngineBat(root,"ADD")
	SelectDate.SetDateSetByPredicateDate(root,fileName)

