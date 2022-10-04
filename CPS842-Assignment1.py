import json

filename = "20Lines2.json"
with open(filename, 'r', encoding='utf-16') as documentsJson:
    lines = documentsJson.readlines()

dictionary = {}
postings = {}

for lineNumber in range(len(lines)):
    currentLine = lines[lineNumber]
    documentJsonObject = json.loads(currentLine)

    titleAndText = documentJsonObject['title'] + ' ' + documentJsonObject['contents']
    terms = titleAndText.lower().split()

    for term in terms:
        if term in dictionary:
            dictionary.update({term: dictionary[term]+1})
        else:
            dictionary[term] = 1

print(dictionary)