from turtle import title
import pandas as pd 
from bs4 import BeautifulSoup

corpus_df = pd.read_json("20Lines2.json", encoding="utf-16", lines=True)
print(corpus_df)
dictionary = {}
postings = {}
for i in range (0, len(corpus_df)-1):
    titleAndContent = corpus_df.title[i] .join(' ').join(BeautifulSoup(corpus_df.contents[i], "html.parser").stripped_strings)
    terms = titleAndContent.lower().split()

    for term in terms:
        if term in dictionary:
            dictionary.update({term: dictionary[term]+1})
        else:
            dictionary[term] = 1

print(dictionary)