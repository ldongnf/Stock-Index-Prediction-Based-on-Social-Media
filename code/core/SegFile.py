#!/usr/bin/env python
#-*- coding: utf8 -*-
import jieba

def FileSegement(fileDir,fileName,saveFileName):
	filePath = fileDir +'\\' + fileName
	saveFilePath = fileDir +'\\' + saveFileName
	file = open(filePath)
	saveFile = open(saveFilePath,'w')

	for lines in file:
		str = ""
		segList = jieba.cut(lines, cut_all = False)
		for words in segList:
			str = str + words + " "
		str = str[:-1]
		saveFile.write(str.encode('utf-8'))

	file.close()
	saveFile.close()
