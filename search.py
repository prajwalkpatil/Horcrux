import re
import json
import nltk
import string
from datetime import datetime
from googlesearch import search   
from urllib.request import urlopen
from collections import Counter
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

this_file = "search.py"
link_results = []
text_content = []
selected_words = []
knowledge_base = {}
match_number = {}
match_ratio = {}

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
    if re.match(r"\S*gstatic.\S*",j):
        return True
    return False

def get_links(keyword):
    global link_results
    for j in search(keyword, tld="com", num = 25, stop = 25, pause=2): 
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
            continue
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
    print(log_msg)


# ----------------------- Functions for matching Horcrux ---------------------- #

def does_match(word, given_string):
    if len(word) <= 2:
        return 0
    reg = r" ?" + word + r" ?";
    m = re.findall(reg, given_string, re.IGNORECASE)
    return len(m)

def init_match_number():
    global match_number
    match_number = {}
    for i in knowledge_base:
        match_number[i] = []
        for j in knowledge_base[i]:
            match_number[i].append(0)

def match_horcrux(word):
    global match_number
    if match_number == {}:
        init_match_number()
    for i in knowledge_base:
        for index in range(0, len(knowledge_base[i])):
            match_number[i][index] += does_match(word, knowledge_base[i][index])

def find_horcrux(number_of_common = 8):
    for i in selected_words:
        common_words = Counter(i).most_common(number_of_common)
        for j in common_words:
            match_horcrux(j[0])
    write_log(match_number,this_file)

def calculate_horcrux():
    global match_number
    global match_ratio
    total_score = 0
    for i in match_number:
        match_ratio[i] = {}
        match_ratio[i]["score"] = 0;
        match_ratio[i]["percentage"] = 0;
        for j in range(0, len(match_number[i])):
            match_ratio[i]["score"] += match_number[i][j] * (1 / pow(20,j))
    for i in match_ratio:
        total_score += match_ratio[i]["score"]
    for i in match_ratio:
        match_ratio[i]["percentage"] = (match_ratio[i]["score"] / total_score) * 100;
    print(match_ratio)


def main():
    write_log("===================== START SESSION ======================", this_file)

    try:
        fetch_base()
    except:
        write_log("Error in fetching the base", this_file)
    
    query = input("Enter the key-word: ")
    while True:
        try:
            get_links(query)
            break
        except:
            write_log(f"Error in getting links for \'{query}\', Trying again.", this_file)
            continue

    try:
        get_text_content()
    except:
        write_log("Error in getting the text content", this_file)
        exit()

    try:
        process_text_content()
    except:
        write_log("Error in processing the text content", this_file)
        exit()

    try:
        find_horcrux()
    except:
        write_log("Error in finding Horcrux", this_file)
        exit()

    calculate_horcrux()

    write_log("====================== END SESSION ======================\n\n\n", this_file)

main()
