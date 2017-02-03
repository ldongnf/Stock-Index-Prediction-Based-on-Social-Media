#!/usr/bin/env python
#-*- coding: utf8 -*-
from bs4 import BeautifulSoup
import os
import re
import DateUnification
import time

def ParserNCD(fileDir, nameFileName,contentFileName,dateFileName,parserMode):
	CustomParser(fileDir, nameFileName, 'a', "nk",parserMode)
	CustomParser(fileDir, contentFileName, 'span', "ctt",parserMode)
	CustomParser(fileDir, dateFileName, 'span', "ct",parserMode)
	DateUnification.DateUnified(fileDir, dateFileName, 'basetime.txt')

def CustomParser(fileDir,saveFileName,htmlTag,htmlTagAttribute,parserMode):
	if parserMode == "ADD":
		if os.path.exists(fileDir+'\\'+saveFileName):
			return
	saveFile = open(fileDir + '\\' + saveFileName,"w")
	for i in range(1,getFileAmount(fileDir) + 1):
		htmlFile = open(fileDir + "//%s.html"%str(i),"r")
		html = htmlFile.read().decode("utf-8")
		htmlFile.close()
		soup = BeautifulSoup(html,"html.parser")
		htmlContent = soup.find_all(htmlTag,class_=htmlTagAttribute)
		for text in htmlContent:
			saveFile.write(text.get_text().encode('utf-8')+'\n')
		html = ""
	saveFile.close()

def getFileAmount(filePath):
	i = 0
	for root, dirs, files in os.walk(filePath, topdown=True):
		if not files:
			break
		else:
			pattern = re.compile(r"\d.html")		
			for name in files:
				res = pattern.search(name)
				if res: 
					i = i + 1
	return i
if __name__ == "__main__":
	nameFileName = 'name.txt'
	contentFileName = 'content.txt'
	dateFileName = 'date.txt'
	ParserNCD("E://testpack//cangwei",nameFileName,contentFileName,dateFileName)