#   Author: Prajwal K. Patil
#   This program is used to perform the core operation of identifying the Horcruxes.
#   This program requires 'base/json/base_joined.json' file.
#       If the file is not generated, execute 'base/base_generator.py' and 'base/base_cleaner.py'

import re
import json
import nltk
import string
from datetime import datetime
from googlesearch import search   
from urllib.request import urlopen
from collections import Counter
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize

#Global variables used throughout the program 
this_file = "search.py"
link_results = []
text_content = []
selected_words = []
knowledge_base = {}
match_number = {}
match_ratio = {}
sorted_strings = []
display_logs = True
query = ""

#Function to check if the extracted URL belongs to the domain with pages of unextractable text 
def is_ul(j):
    #The following domains can't be used as a source for getting text_content
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

#Function that uses the library googlesearch to get the top 25 search results when a query is entered
def get_links(keyword):
    global link_results
    for j in search(keyword, tld="co.in", num = 25, stop = 25, pause=10): 
        #Check if its forbidden URL
        if not is_ul(j):
            #Append the link to the array
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
            #Function call to open a page
            page = urlopen(url)
            #If successful, write success message to the log file 
            write_log(f"Text fetched for the URL - {url}", this_file)
        except:
            #If there are any exceptions, write error message to the log file 
            write_log(f"Couldn't open the URL - {url}", this_file)
            #Continue the loop so that it fetches other pages 
            continue
        #Get text content from all the <p> tags from the fetched page
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.findAll('p')
        #Join each text snippet to a string then appeng it to an array
        article = ''
        for i in content:
            article = article + ' ' +  i.text
        text_content.append(article)
    write_log("Text content fetched successfully", this_file)

#Function to remove punctuations from given text and return a processed text
def remove_punctuation(text):
    translator = str.maketrans("","",string.punctuation)
    return text.translate(translator)

#Function for processing the 
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
            #Find only Nouns from the given words
            if i[1]== 'NN' or i[1]== 'NNS' or i[1] == 'NNPS' or i[1] == 'NNP':
                #Append them to selected words array
                selected_words[-1].append(i[0])
    write_log("Text processed successfully", this_file)

#Function to fetch knowledge_base from 'base/json/base_joined.json' 
def fetch_base():
    global knowledge_base
    with open("base/json/base_joined.json","r") as json_file:
        knowledge_base = json.load(json_file)
    write_log("Base fetched successfully", this_file)

#Function to write log message to the specified log file
def write_log(log_msg, from_file_name, log_file_name = "log"):
    global display_logs
    #Get date and time at this moment
    now = datetime.now()
    date_time = now.strftime("%d %B %Y, %H:%M:%S")
    with open(f"logs/{log_file_name}.txt","a") as file_ptr:
        msg = f"{from_file_name} : {date_time} - {log_msg} \n";
        file_ptr.write(msg)
    #If display_logs is True then, display logs on the terminal while execution
    if display_logs:
        print(log_msg)


# ----------------------- Functions for matching Horcrux ---------------------- #

#Function to check the number of occurences of a word in the given_string
def does_match(word, given_string):
    #Discard words with less than 3 letters
    if len(word) <= 2:
        return 0
    reg = r" ?" + word + r" ?";
    #Regular expression function to find all occurences ignoring the case of the words
    m = re.findall(reg, given_string, re.IGNORECASE)
    #Return the number of times the given word appears in the given string
    return len(m)

#Function to initialize the dictionary that stores the number of matches for each Horcrux
def init_match_number():
    global match_number
    match_number = {}
    for i in knowledge_base:
        match_number[i] = []
        for j in knowledge_base[i]:
            match_number[i].append(0)

#Function to match horcrux for a given word
def match_horcrux(word):
    global match_number
    #If the match_number dictionary is empty then, initialise it.
    if match_number == {}:
        init_match_number()
    for i in knowledge_base:
        for index in range(0, len(knowledge_base[i])):
            #Check if the word matches for each horcrux and add the number of occurences
            match_number[i][index] += does_match(word, knowledge_base[i][index])

#Function to iterate over each selected words and select most common words(8) among them
def find_horcrux(number_of_common = 8):
    for i in selected_words:
        #Fetch the most common words
        common_words = Counter(i).most_common(number_of_common)
        #Iterate over those most common words and match them to Horcruxes
        for j in common_words:
            match_horcrux(j[0])
    write_log(match_number,this_file)

#Function to calculate Horcrux match score and percentage
#from the matched primary and secondary attributes
def calculate_horcrux():
    global match_number
    global match_ratio
    total_score = 0
    for i in match_number:
        #Initialize score and percentage to 0 
        match_ratio[i] = {}
        match_ratio[i]["score"] = 0;
        match_ratio[i]["percentage"] = 0;
        #The weight of secondary match is (1/20)th as that of primary match (Geometric progression)
        for j in range(0, len(match_number[i])):
            match_ratio[i]["score"] += round(match_number[i][j] * (1 / pow(20, j)), 2)
    #Add scores of each Horcrux to get a total score
    for i in match_ratio:
        total_score += match_ratio[i]["score"]
    #Calculate percentage for each Horcrux upto 2 decimal places
    for i in match_ratio:
        match_ratio[i]["percentage"] = round(((match_ratio[i]["score"] / total_score) * 100), 2)
    # print(match_ratio)

#Function to sort Horcruxes as per their percentages in decreasing order
def sort_horcruxes():
    global match_ratio
    global sorted_strings
    temp_greater = 0
    temp_string = ""
    for j in match_ratio:
        for i in match_ratio:
            if match_ratio[i]['percentage'] > temp_greater and i not in sorted_strings:
                temp_greater = match_ratio[i]['percentage']
                temp_string = i
        #Append the horcrux to an array containing sorted_strings
        sorted_strings.append(temp_string)
        temp_greater = 0
        temp_string = ""
    # print(sorted_strings)

#Function to print the matching Horcrux in decreasing order with theri score and percentages
def print_results():
    global display_logs
    #Log function will not display logs on terminal
    display_logs = False
    #The logs for this function are written in a seperate file - "results.txt"
    write_log("======================== RESULTS - START =====================",this_file,"results")
    print("=========================== RESULTS ==========================")
    global sorted_strings
    global match_ratio
    Horcrux_title = "Horcrux"
    Score_title = "Score"
    Percentage_title = "Percentage"
    write_log(f"Keyword: \'{query}\'",this_file,"results")
    #Print heading 
    print(f"{Horcrux_title:{20}} {Score_title:>{20}} {Percentage_title:>{20}}")
    write_log(f"{Horcrux_title:{20}} {Score_title:>{20}} {Percentage_title:>{20}}",this_file,"results")
    print("")
    #Print name, score and percentage match for each Horcrux
    for i in sorted_strings:
        print(f"{i:{20}} {match_ratio[i]['score']:{20}} {match_ratio[i]['percentage']:{19}}%")
        write_log(f"{i:{20}} {match_ratio[i]['score']:{20}} {match_ratio[i]['percentage']:{19}}%",this_file, "results")
    write_log("======================== RESULTS - END  ======================\n\n\n",this_file,"results")


def main():
    global query
    write_log("===================== START SESSION ======================", this_file)

    try:
        fetch_base()
    except:
        write_log("Error in fetching the base", this_file)
    
    #User prompt to get the keyword as input
    query = input("Enter the key-word: ")
    #Infinite loop which breaks when google results are fetched successfully for a given search term
    while True:
        try:
            get_links(query)
            break
        except:
            write_log(f"Unable to get search results for \'{query}\', Trying again.", this_file)
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

    print("Getting results. Please wait.")
    try:
        find_horcrux()
    except:
        write_log("Error in finding Horcrux", this_file)
        exit()

    calculate_horcrux()
    sort_horcruxes()

    write_log("====================== END SESSION ======================\n\n\n", this_file)
    print_results()
#Execute the main function
main()
