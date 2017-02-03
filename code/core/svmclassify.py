#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import subprocess
import math

def getlexicon(documents):
    words=[]
    for document in documents:
        words+=document.words.keys()
    words=set(words)
    
    lexicon=dict([(word,i+1) for i,word in enumerate(words)])
    return lexicon
    
def createSvmText(documents,lexicon,path):
    text=''
    for document in documents:
        if document.polarity==True:
            line="+1 "
        else:
            line="-1 "
        pairs=[(lexicon[word],document.words[word]) for word in document.words.keys() if word in lexicon]
        pairs.sort()
        for pair in pairs:
            line+='%d:%d ' %(pair[0],pair[1])
        text+=line+'\n'
    if len(text)>0:
        output=open(path,'w')
        output.write(text)
     
def createResults(tests):
	dataSize = len(tests)
	input=open('result.output','rb')
	results=[]
	count=0
	positive = 0
	negative = 0
	if dataSize == 0:
		return dataSize,positive,negative
	for i,line in enumerate(input):
		score=float(line)
		if (tests[i].polarity==True and score>0) or (tests[i].polarity==False and score<0):
			count+=1 
		distance=float(line)
		x0=1/(1+math.exp(abs(distance)))
		x1=1/(1+math.exp(-1*abs(distance)))
		prob=x1/(x0+x1)
		if distance<0:prob*=-1
		if prob>0:
			positive += 1
		if prob < 0:
			negative += 1
		results.append(prob)
	acc=float(count)/len(tests)

	percentage_p = positive * 1.0/dataSize
	percentage_n = negative *1.0/dataSize
	
	print 'Size: ',dataSize
	print 'Positive: ',positive,percentage_p
	print 'Negative: ',negative,percentage_n
	print 'accuracy is %f(%d/%d)' % (acc,count,len(tests))
	return dataSize,positive,negative
    
def svm_classify(trains,tests):
    lexicon=getlexicon(trains)
    createSvmText(trains,lexicon,'train.txt')
    createSvmText(tests,lexicon,'test.txt')
    subprocess.call("cmd.bat",shell=True)
    return createResults(tests)

def run_svm_classify(tests):
    subprocess.call("cmd.bat",shell=True)
    return createResults(tests)

