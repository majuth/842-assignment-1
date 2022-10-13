from turtle import title
import pandas as pd 
from bs4 import BeautifulSoup

corpus_df = pd.read_json("20Lines2.json", encoding="utf-16", lines=True)
dictionary = {}
postings = {}
for i in range (0, len(corpus_df)-1):
    titleAndContent = corpus_df.title[i] .join(' ').join(BeautifulSoup(corpus_df.contents[i], "html.parser").stripped_strings)
    terms = titleAndContent.lower().split()

# remove punctuation and symbols
    filtered_terms = []
    acceptable_characters = set('-0123456789abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for term in terms:
        answer = ''.join(filter(acceptable_characters.__contains__, term))
        filtered_terms.append(answer)

    # sort alphabetically
    filtered_terms=sorted(filtered_terms)

# create dictionary
    for term in filtered_terms:
        if term in dictionary:
            dictionary.update({term: dictionary[term]+1})
        else:
            dictionary[term] = 1

# TODO: remove words that aren't words LOL

print(dictionary)