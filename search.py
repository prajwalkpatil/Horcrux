import re
import json
import nltk
import string
from googlesearch import search   
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

link_results = []
text_content = []
selected_words = []

def is_ul(j):
    if re.match(r"\S*youtube.com\S*",j):
        return True
    if re.match(r"\S*dictionary.com\S*",j):
        return True
    if re.match(r"\S*facebook.com\S*",j):
        return True
    if re.match(r"\S*twitter.com\S*",j):
        return True
    if re.match(r"\S*urbandictionary.com\S*",j):
        return True
    if re.match(r"\S*amazon.\S*",j):
        return True
    return False

def get_links(keyword):
    global link_results
    for j in search(keyword, tld="com", num=20, stop=20, pause=2): 
        if not is_ul(j):
            link_results.append(j) 
    print(link_results)

def get_text_content():
    global link_results
    global text_content
    for i in link_results:
        url = i
        try:
            page = urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            content = soup.findAll('p')
            article = ''
            for i in content:
                article = article + ' ' +  i.text
            text_content.append(article)
        except:
            print("Error opening the URL")   

def remove_punctuation(text):
    translator = str.maketrans("","",string.punctuation)
    return text.translate(translator)

def process_text_content():
    global text_content
    global selected_words
    for content in text_content:
        #Remove all the footnotes to match - Ex: [12]
        content = re.sub(r"\[\d*\]","",content) 
        #Replace all the hyphens with space
        content = content.replace("-"," ")
        #Remove all the punctuations
        content = remove_punctuation(content)
        #Tokenize the words
        content = word_tokenize(content)
        tagged = nltk.pos_tag(content)
        #Select only nouns out of the extracted text
        selected_words.append([])
        for i in tagged:
            if i[1]== 'NN' or i[1]== 'NNS' or i[1] == 'NNPS' or i[1] == 'NNP':
                selected_words[-1].append(i[0])


get_links("India")
get_text_content()
process_text_content()
print(selected_words)

with open("fetched.json", "w") as f:
    json.dump(text_content, f)

with open("selected.json", "w") as f:
    json.dump(selected_words, f)