import re
from googlesearch import search   
from urllib.request import urlopen
from bs4 import BeautifulSoup

link_results = []
text_content = []


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
        except:
            print("Error opening the URL")   
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.findAll('p')
        article = ''
        for i in content:
            article = article + ' ' +  i.text
        print(article)
        text_content.append(article)

get_links("Apple Inc")
get_text_content()
print(text_content)
