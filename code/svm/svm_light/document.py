from __future__ import division

class Document:
    def __init__(self,polarity, words):
    # polarity: the document polarity
    # words:    all the words in the document
        self.polarity = polarity
        self.words = words

def generate_documents(file_path, polarity):
    # use the input file to generate documents with polarity and trailing words
    # file_path:    file source
    # polarity:     polarity for the text
    # rtype:        documents

    with open(file_path, 'rb') as file:
        documents = []
        for line in file:
            words = map(str.lower, line.split())
            dictionary = {}
            for i, word in enumerate(words):
                if word not in dictionary:
                    dictionary[word] = 1
            if dictionary:
                documents.append(Document(polarity, dictionary))
    return documents

def create_domain(domain):
    # generate negative and positive documents from corpus
    # domain:   corpus_name
    # rtype:    negative_corpus, positive_corpus
    
    negative_corpus = generate_documents(r'corpus/%s/negative.review' % domain, False)
    positive_corpus = generate_documents(r'corpus/%s/positive.review' % domain, True)
    return negative_corpus, positive_corpus



