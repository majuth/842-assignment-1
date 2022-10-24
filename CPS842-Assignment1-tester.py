from os import times
import sys
from porterStemming import PorterStemmer
import time

dictionary = {}
postings = []

timings = []

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

        for document in postingList:
            print("Document ID: " + document.strip().split(",")[0][1:])
            print("Document Title: ")
            print("Term Frequency: " + document.split(",")[1][1:])
            print("Positions: " + document.split("[")[1].split("]")[0])
            print("Document Summary: ")
            end = time.time()
            timings.append((end-start))
            print("Search time: " + str(end - start))

    else:
        print("Term is not in the collection")