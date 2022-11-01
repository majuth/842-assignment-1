from os import times
import sys
from porterStemming import PorterStemmer
import time
import pandas as pd
from bs4 import BeautifulSoup
import json

dictionary = {}
postings = []

timings = []

# corpus_df = pd.read_json("20Lines2.json", encoding="utf-16", lines=True)

with open(sys.argv[1], 'r') as dictionaryFile:
    dictionaryLines = dictionaryFile.readlines()

    for line in range(0,len(dictionaryLines)):
        termAndNum = dictionaryLines[line].split("\n")[0].split(" ")
        dictionary.update({termAndNum[0]: termAndNum[1] + " ," + str(line)})

with open(sys.argv[2], 'r') as postingsFile:
    postings = postingsFile.readlines()

queryTerm = ""

while queryTerm != "ZZEND":
    queryTerm = input("Enter the term you are searching for: ")
    start = time.time()


    if queryTerm == "ZZEND":
        avg = sum(timings)/len(timings)
        print("The average search time was: " + str(avg))
        continue

    #get stemmed version of query term
    p=PorterStemmer()
    stemmedQueryTermList = (p.stem(queryTerm, 0, len(queryTerm)-1))
    stemmedQueryTerm = ("".join(stemmedQueryTermList))

    if (queryTerm in dictionary or stemmedQueryTerm in dictionary):
        print("Term is in " + str(dictionary[queryTerm].split(" ,")[0]) + " document(s) in the collection (document frequency)")
        postingList = (postings[int(dictionary[queryTerm].split(" ,")[1])]).split(";")[:-1]
        
        counter=0
        for document in postingList:
            docID =  document.strip().split(",")[0][1:]
            print("Document ID: " + docID)
            print("Term Frequency: " + document.split(",")[1][1:])
            print("Positions: " + document.split("[")[1].split("]")[0])
            with open ('./10000Lines.jsonl', encoding="utf-8", errors="ignore") as corpusFile:
                for line in corpusFile:
                    json_doc = json.loads(line)
                    if (json_doc['id'] == int(docID)):
                        print("Document Title: " + json_doc['title'])
                        contents = ' '.join(BeautifulSoup(json_doc['contents'], "html.parser").stripped_strings)
                        contents_list=contents.split()
                        pos=document.split("[")[1].split("]")[0]
                        first_occurence=(pos.split(","))[0]
                        if (int(first_occurence) < 5):
                            begin = 0
                            end = int(first_occurence)+10
                        elif (int(first_occurence)+6 > len(contents_list)):
                            begin=int(first_occurence)-5
                            end = len(first_occurence)
                        else:
                            begin = int(first_occurence)-5
                            end = int(first_occurence)+6
                        summary=output=' '.join(contents_list[begin:end])
                        print("Document summary: " + summary)
        end = time.time()
        timings.append((end-start))
        print("Search time: " + str(end - start))

    else:
        print("Term is not in the collection")