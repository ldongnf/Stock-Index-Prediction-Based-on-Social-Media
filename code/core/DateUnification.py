#!/usr/bin/env python
#-*- coding: utf8 -*-
import re
import os
def DateUnified(dateFileDir, dateFileName, baseFileName):
	baseFilePath = dateFileDir+'\\'+ baseFileName
	baseTimeFile = open(baseFilePath,'r')
	baseTime = baseTimeFile.read()
	baseDate,time = baseTime.split(' ')
	baseTimeFile.close()
	
	WordsReplaceToDate(dateFileDir, dateFileName, '今天', baseDate)
	#ReplaceWordsToDate(dateFileDir, dateFileName, '来自(.*)','')
	DateFormatUnified(dateFileDir,dateFileName,'\d\d?月\d\d?日',baseDate)
	UpdateMinuteToDate(dateFileDir,dateFileName,'\d\d?分钟前',baseTime)
	DateExtract(dateFileDir,dateFileName)
def WordsReplaceToDate(dateFileDir, dateFileName,keyWord,baseDate):
	tempFileName = "tempdate.txt" 
	dateFilePath = dateFileDir+'\\'+dateFileName
	tempFilePath = dateFileDir + '\\'+tempFileName
	dateFile = open(dateFilePath,"r")
	tempfile = open(tempFilePath,"w")
	pattern = re.compile(keyWord)
	for line in dateFile:
		res = pattern.sub(baseDate,line)
		tempfile.write(res)
	tempfile.close()
	dateFile.close()
	os.remove(dateFilePath)
	os.rename(tempFilePath,dateFilePath)
	return
def UpdateMinuteToDate(dateFileDir, dateFileName,keyWord,baseDate):
	tempFileName = "tempdate.txt"
	dateFilePath = dateFileDir + '//'+dateFileName
	tempFilePath = dateFileDir + '//' + tempFileName
	dateFile = open(dateFilePath,"r")
	tempFile = open(dateFileDir+'//'+tempFileName,"w")
	pattern = re.compile(keyWord)
	for line in dateFile:
		res = pattern.search(line)
		if res:
			newMinute = res.group()
			newMinute = newMinute[:-9]
			newDate = GetNewTime(newMinute,baseDate)
			res = pattern.sub(newDate,line)
			newDate = ""
			tempFile.write(res)
		else:
			tempFile.write(line)
	tempFile.close()
	dateFile.close()
	os.remove(dateFilePath)
	os.rename(tempFilePath,dateFilePath)
def GetNewTime(newMinute, baseDate):
	date,time = baseDate.split(' ')
	hour,minute = time.split(':')
	year,month,day = date.split('-')
	m = int(minute)
	h = int(hour)
	d = int(day)
	mon = int(month) 
	y = int(year)
	m = m - int(newMinute)
	if m < 0:
		m = m + 60
		h = h - 1
		if h < 0:
			h = h + 24
			d = d - 1
			if d <= 0 :
				if mon == 5 or mon == 7 or mon == 10 or mon == 12:
					d = d + 30
				if mon == 1 or mon == 2 or mon == 8 or mon == 4 or mon == 6 or mon == 9 or mon == 11:
					d = d + 31
				if mon == 3:
					if y%4==0:
						d = d + 29
					else:
						d = d + 28
				mon = mon - 1
				if mon <= 0:
					y = y - 1
					mon = mon + 12
	if m < 10:
		minute = '0' + str(m)
	else:
		minute = str(m)
	if h < 10:
		hour = '0' + str(h)
	else:
		hour = str(h)
	if d < 10:
		day = '0' + str(d)
	else:
		day = str(d)
	if mon < 10:
		month = '0' + str(mon)
	else:
		month = str(mon)
	year = str(y)
	newDate = str(year)+'-'+str(month)+'-'+str(day)+' '+ str(hour) +':'+str(minute)
	return newDate
def DateFormatUnified(dateFileDir,dateFileName,oldDate,baseDate):
	tempFileName = "tempdate.txt"
	dateFilePath = dateFileDir + '//' + dateFileName
	tempFilePath = dateFileDir + '//' + tempFileName
	dateFile = open(dateFilePath,"r")
	tempfile = open(tempFilePath,"w")
	pattern = re.compile(oldDate)
	
	for line in dateFile:
		res = pattern.search(line)
		if res:
			newDate = GetNewDate(res.group(),baseDate)
			res = pattern.sub(newDate,line)
			newDate = ""
			tempfile.write(res)
		else:
			tempfile.write(line)
		
	tempfile.close()
	dateFile.close()
	os.remove(dateFilePath)
	os.rename(tempFilePath,dateFilePath)
def GetNewDate(oldDate, baseDate):
	month_t,day_t = oldDate.split('月')
	day_t,junk = day_t.split('日')
	year,month,day = baseDate.split('-')
	newDate = year+'-'+month_t+'-'+day_t
	return newDate
def GetNewDateByDay(newDay,oldDate):
	year,month,day = oldDate.split('-')
	d = int(day)
	mon = int(month) 
	y = int(year)
	d = d - int(newDay)
	if d <= 0 :
		if mon == 5 or mon == 7 or mon == 10 or mon == 12:
			d = d + 30
		if mon == 1 or mon == 2 or mon == 8 or mon == 4 or mon == 6 or mon == 9 or mon == 11:
			d = d + 31
		if mon == 3:
			if y%4==0:
				d = d + 29
			else:
				d = d + 28
		mon = mon - 1
		if mon <= 0:
			y = y - 1
			mon = mon + 12
	if d < 10:
		day = '0' + str(d)
	else:
		day = str(d)
	if mon < 10:
		month = '0' + str(mon)
	else:
		month = str(mon)
	year = str(y)
	newDate = str(year)+'-'+str(month)+'-'+str(day)
	return newDate

def DateExtract(dateFileDir,dateFileName):
	tempFileName = "tempdate.txt"
	dateFilePath = dateFileDir + '//' + dateFileName
	tempFilePath = dateFileDir + '//' + tempFileName
	dateFile = open(dateFilePath,"r")
	tempFile = open(tempFilePath,"w")
	datePattern = re.compile("\d{4}-\d\d-\d\d \d\d:\d\d")
	for line in dateFile:
		dateRes = datePattern.search(line)
		if dateRes:
			tempFile.write(dateRes.group()+'\n')
		else:
			tempFile.write(line)
	tempFile.close()
	dateFile.close()
	os.remove(dateFilePath)
	os.rename(tempFilePath,dateFilePath)
def TimeBackwardByHour(newHour,oldDate):
	date,time = oldDate.split(' ')
	hour,minute = time.split(':')
	year,month,day = date.split('-')
	m = int(minute)
	h = int(hour)
	d = int(day)
	mon = int(month) 
	y = int(year)
	h = h - int(newHour)
	if h < 0:
		h = h + 24
		d = d - 1
		if d <= 0 :
			if mon == 5 or mon == 7 or mon == 10 or mon == 12:
				d = d + 30
			if mon == 1 or mon == 2 or mon == 8 or mon == 4 or mon == 6 or mon == 9 or mon == 11:
				d = d + 31
			if mon == 3:
				if y%4==0:
					d = d + 29
				else:
					d = d + 28
			mon = mon - 1
			if mon <= 0:
				y = y - 1
				mon = mon + 12
	if m < 10:
		minute = '0' + str(m)
	else:
		minute = str(m)
	if h < 10:
		hour = '0' + str(h)
	else:
		hour = str(h)
	if d < 10:
		day = '0' + str(d)
	else:
		day = str(d)
	if mon < 10:
		month = '0' + str(mon)
	else:
		month = str(mon)
	year = str(y)
	newDate = str(year)+'-'+str(month)+'-'+str(day)+' '+ str(hour) +':'+str(minute)
	return newDate

def TimeForwardByHour(newHour,oldDate):
	date,time = oldDate.split(' ')
	hour,minute = time.split(':')
	year,month,day = date.split('-')
	m = int(minute)
	h = int(hour)
	d = int(day)
	mon = int(month) 
	y = int(year)
	h = h + int(newHour)
	if h>=24:
		h = h - 24
		d = d + 1
		if mon == 1 or mon == 3 or mon == 5 or mon == 7 or mon == 8 or mon == 10:
			if d > 31:
				d = 1
				mon += 1
		if mon == 4 or mon == 6 or mon == 9 or mon == 11:
			if d > 30:
				d = 1
				mon += 1
		if mon == 2:
			if d>28:
				if y%4 == 0:
					d +=1
				else:
					d =1
					mon +=1
		if mon == 12 and day>31:
			d = 1
			mon = 1
			y += 1
	if m < 10:
		minute = '0' + str(m)
	else:
		minute = str(m)
	if h < 10:
		hour = '0' + str(h)
	else:
		hour = str(h)
	if d < 10:
		day = '0' + str(d)
	else:
		day = str(d)
	if mon < 10:
		month = '0' + str(mon)
	else:
		month = str(mon)
	year = str(y)
	newDate = str(year)+'-'+str(month)+'-'+str(day)+' '+ str(hour) +':'+str(minute)
	return newDate
	
def TimeBackward(dateFileDir,dateFileName):
	tempFileName = "tfate.txt"
	dateFilePath = dateFileDir + '//'+dateFileName
	tempFilePath = dateFileDir + '//' + tempFileName
	dateFile = open(dateFilePath,"r")
	tempFile = open(dateFileDir+'//'+tempFileName,"w")
	for line in dateFile:
		tempFile.write(TimeBackwardByHour(9,line)+'\n')
	tempFile.close()
	dateFile.close()
	os.remove(dateFilePath)
	os.rename(tempFilePath,dateFilePath)
def TimeForward(dateFileDir,dateFileName):
	tempFileName = "tf.txt"
	dateFilePath = dateFileDir + '//'+dateFileName
	tempFilePath = dateFileDir + '//' + tempFileName
	dateFile = open(dateFilePath,"r")
	tempFile = open(dateFileDir+'//'+tempFileName,"w")
	for line in dateFile:
		tempFile.write(TimeForwardByHour(9,line)+'\n')
	tempFile.close()
	dateFile.close()
	os.remove(dateFilePath)
	os.rename(tempFilePath,dateFilePath)
def DateSeparate(dateFileDir,dateFileName,saveFileName):
	dateFile = open(dateFileDir+'\\'+dateFileName)
	saveFile = open(dateFileDir+'\\'+saveFileName,"w")
	for line in dateFile:
		date,time = line.split(' ')
		saveFile.write(date+'\n')
	dateFile.close()
	saveFile.close()
if __name__ == "__main__":
	#print GetNewDateByDay(1,'2015-03-01')
	DateSeparate("e:\\data","date_all.txt","all.txt")