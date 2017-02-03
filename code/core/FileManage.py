#!/usr/bin/env python
#-*- coding: utf8 -*-
import os
import re
def CopyFile(resFilePath,sourceFilePath):
#resFilePath
#sourceFilePath 
	row = 0
	resFile = open(resFilePath,"a")
	if not resFile:
		resFile = open(resFilePath)
	sourceFile = open(sourceFilePath,"r")
	for line in sourceFile:
		resFile.write(line)
		row = row + 1
	sourceFile.close()
	resFile.close()
	print sourceFilePath + '   ->   ' + resFilePath
	return row
def GetFilePaths(fileDir,targetFileName):
	paths = []
	i = 0
	for root, dirs, files in os.walk(fileDir,topdown = True):
		if not files:
			continue
		else:
			pattern = re.compile(targetFileName)
			for name in files:
				res = pattern.search(name)
				if res: 
					paths.append(root)
					break
	return paths
def GetDirPathsForGenerall(fileDir,targetDirName):
	paths = []
	i = 0
	for root, dirs, files in os.walk(fileDir,topdown = True):
		pattern = re.compile(targetDirName)
		for dir in dirs:
			res = pattern.search(dir)
			if res: 
				paths.append(root)
				break
	return paths
def GetDirPathsForSingle(fileDir,targetDirName):
	paths = []
	i = 0
	for root, dirs, files in os.walk(fileDir,topdown = True):
		basePattern = re.compile(r'single')
		pattern = re.compile(targetDirName)
		if basePattern.search(root):
			for dir in dirs:
				res = pattern.search(dir)
				if res: 
					paths.append(root+'\\'+dir)
	return paths
def FilePrepare(fileDir,fileName):
	if os.path.exists(fileDir + '//' + fileName):
		os.remove(fileDir + '//' + fileName)
		print 'remove: ' +  fileName
	else:
		print 'Generate: ' + fileName
def MergeFile(fileDir,fileName1,fileName2,saveFileName):
	res = ""
	file1 = open(fileDir+'//'+fileName1,"r")
	file2 = open(fileDir+'//'+fileName2,"r")
	saveFile = open(fileDir + '//'+saveFileName,"w")
	for words in file1:
		res = words[:-1] +' '+file2.readline()
		saveFile.write(res)
	saveFile.close()
	file2.close()
	file1.close()
def SeparateFile(fileDir,sourceFileName,nameFileName,contentFileName,dateFileName):
	DFileName = 'D.txt'
	CFileName = 'C.txt'
	NFileName = 'N.txt'
	DFilePath = fileDir +'\\'+DFileName
	CFilePath = fileDir +'\\'+CFileName
	NFilePath = fileDir +'\\'+NFileName
	NFile = open(NFilePath,'w')
	CFile = open(CFilePath,'w')
	DFile = open(DFilePath,'w')
	sourceFile = open(fileDir + '\\'+sourceFileName)
	for line in sourceFile:
		date,time = line.split(' ',1)
		time,name = time.split(' ',1)
		name,content = name.split(' ',1)
		NFile.write(name+"\n")
		CFile.write(content)
		DFile.write(date + ' ' + time+"\n")
	NFile.close()
	CFile.close()
	DFile.close()
	sourceFile.close()
	nameFilePath = fileDir + '\\' + nameFileName
	contentFilePath = fileDir + '\\' + contentFileName
	dateFilePath = fileDir + '\\' + dateFileName
	os.remove(nameFilePath)
	os.remove(contentFilePath)
	os.remove(dateFilePath)
	os.rename(NFilePath,nameFilePath)
	os.rename(CFilePath,contentFilePath)
	os.rename(DFilePath,dateFilePath)
def FileCleaner(rootDir,fileNameList):
	for root,dirs,files in os.walk(rootDir,topdown = True):
		for file in files:
			if file in fileNameList:
				os.remove(root + '\\'+file)
				print root + '\\' + file + ' removed'
def FileCompare(filePath1,filePath2):
	file1 = open(filePath1)
	file2 = open(filePath2)
	lines1 = file1.readlines();
	lines2 = file2.readlines();
	if len(lines1)!=len(lines2):
		return False
	else:
		if lines1 == lines2:
			return True
		else:
			return False
def SumResultFile(rootDir,targetDir,sourceFileName,SumMode):
	for root,dirs,files in os.walk(rootDir,topdown = True):
		dirNamedByDate = dirs
		break
	for dir in dirNamedByDate:
		if SumMode =='ADD':
			if os.path.exists(targetDir+'\\'+dir+'.txt'):
				print targetDir + '	'+dir+'.txt' + " existed" 
				continue
		saveFile = open(targetDir+'\\'+dir+'.txt',"w")
		sourceFile = open(rootDir + '\\' + dir+'\\'+sourceFileName)
		saveFile.writelines(sourceFile.readlines())
		saveFile.close()
if __name__ == "__main__":
	#print GetFilePaths(r'E:\Datas\20160320\2016032021',r'\d.html')
	#print GetDirPathsForGenerall(r'E:\stock\Data',r'generall_res')
	dirs = []
	dirs = GetDirPathsForSingle(r'E:\stock\Data',r'\d')
	for dir in dirs:
		print dir