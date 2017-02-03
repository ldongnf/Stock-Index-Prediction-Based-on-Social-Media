from __future__ import division

class Document:
    def __init__(self,polarity,words):
        self.polarity=polarity
        self.words=words

def readFromFile(path,polarity):
    input=open(path,'rb')
    documents=[]
    for line in input:
        pieces=line.split()
        words={}
        for i,piece in enumerate(pieces):
            word=piece.lower()
            if word not in words: words[word]=1
        if len(words)>0:
            documents.append(Document(polarity,words))
    return documents

def createDomain(domain):
    neg=readFromFile(r'corpus\%s\negative.review' % domain,False)
    pos=readFromFile(r'corpus\%s\positive.review' % domain,True)
    return neg,pos



