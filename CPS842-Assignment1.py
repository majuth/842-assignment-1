import pandas as pd 
from bs4 import BeautifulSoup
from porterStemming import PorterStemmer
import argparse

corpus_df = pd.read_json("20Lines2.json", encoding="utf-16", lines=True)

stopwords=[]
with open('stopwords.txt', 'r') as f:
    for term in f:
        term = term.split('\n')
        stopwords.append(term[0])

parser = argparse.ArgumentParser()
parser.add_argument('-stopword', action='store_true')
parser.add_argument('-stem', action='store_true')
options = parser.parse_args()

# convert html text to list of words
dictionary = {}
postings = {}
for doc in range (0, len(corpus_df)):
    titleAndContent = corpus_df.title[doc] .join(' ').join(BeautifulSoup(corpus_df.contents[doc], "html.parser").stripped_strings)
    terms = titleAndContent.lower().split()

# remove punctuation and symbols
    filtered_terms = []
    acceptable_characters = set('-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for term in terms:
        answer = ''.join(filter(acceptable_characters.__contains__, term))
        filtered_terms.append(answer)

# optional porter stemming
    if options.stem:
        stemmed_terms=[]
        for term in filtered_terms:
            p=PorterStemmer()
            stemmed_term = []
            stemmed_term = (p.stem(term, 0, len(term)-1))
            stemmed_terms.append("".join(stemmed_term))
        filtered_terms=stemmed_terms

# optional stopword removal
    if options.stopword:
        stopwords_removed = [term for term in filtered_terms if term not in stopwords]
        filtered_terms = stopwords_removed

# create dictionary
    for term in filtered_terms:
        if term in dictionary:
            dictionary.update({term: dictionary[term]+1})
        else:
            dictionary[term] = 1

# create postings list
    for i in range(len(filtered_terms)):
        term = filtered_terms[i]
        if term in postings:
            if doc in postings[term]:
                tf = postings[term][doc]["term frequency"]
                tf += 1
                positions = postings[term][doc]["positions"]
                positions.append(i)
                postings[term][doc].update({
                    "term frequency" : tf,
                    "positions" : positions
                })
            else:
                postings[term][doc] = {
                    "term frequency" : 1,
                    "positions" : [i]
                }
        else:
            postings[term] = {
                doc : {
                    "term frequency": 1,
                    "positions" : [i]
                }
            }

# write dictionary file
with open('dictionary.txt', 'w') as dicFile:
    for term, docFreq in sorted(dictionary.items()):
        dicFile.write(term + " " + str(docFreq) + "\n")

# write postings list file
with open('postings.txt', 'w') as postFile:
    for term, doc in sorted(postings.items()):
        for docPosition, text in doc.items():
            postFile.write("(" + str(corpus_df.id[docPosition]) + ", " + str(text["term frequency"]) + ", " + str(text["positions"]) + "); " )
        postFile.write("\n")
