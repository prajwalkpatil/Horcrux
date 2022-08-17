import re
import json
import nltk
import string
from datetime import datetime
from googlesearch import search   
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

this_file = "search.py"
link_results = []
text_content = []
selected_words = []
knowledge_base = {}

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
    write_log(f"Links fetched for \"{keyword}\" successfully", this_file)
    # print(link_results)

def get_text_content():
    global link_results
    global text_content
    for i in link_results:
        url = i
        page = ""
        try:
            page = urlopen(url)
            write_log(f"Text fetched for the URL - {url}", this_file)
        except:
            write_log(f"Couldn't open the URL - {url}", this_file)
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.findAll('p')
        article = ''
        for i in content:
            article = article + ' ' +  i.text
        text_content.append(article)
    write_log("Text content fetched successfully", this_file)

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
    write_log("Text processed successfully", this_file)

def fetch_base():
    global knowledge_base
    with open("base/json/base_joined.json","r") as json_file:
        knowledge_base = json.load(json_file)
    write_log("Base fetched successfully", this_file)


def write_log(log_msg, from_file_name, log_file_name = "log"):
    now = datetime.now()
    date_time = now.strftime("%d %B %Y, %H:%M:%S")
    with open(f"logs/{log_file_name}.txt","a") as file_ptr:
        msg = f"{from_file_name} : {date_time} - {log_msg} \n";
        file_ptr.write(msg)
    print(f"{log_msg} - logs/{log_file_name}.txt")



write_log("===================== START SESSION ======================", this_file)

try:
    fetch_base()
except:
    write_log("Error in fetching the base", this_file)

try:
    query = "Hindu"
    get_links(query)
except:
    write_log(f"Error in getting links for {query}", this_file)

try:
    get_text_content()
except:
    write_log("Error in getting the text content", this_file)

try:
    process_text_content()
except:
    write_log("Error in processing the text content", this_file)


with open("fetched.json", "w") as f:
    json.dump(text_content, f)
write_log(f"text_content written to - \"fetched.json\"", this_file)

with open("selected.json", "w") as f:
    json.dump(selected_words, f)
write_log(f"selected_words written to - \"selected.json\"", this_file)

write_log("====================== END SESSION ======================\n\n\n", this_file)