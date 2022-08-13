import requests
import json

knowledge_base = {}

def generate(word, limit = 500):
    global knowledge_base
    knowledge_base[word] = []
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": word,
        "prop": "links",
        "pllimit": limit
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    knowledge_base[word].append([])
    PAGES = DATA["query"]["pages"]
    for k, v in PAGES.items():
        try:
            for l in v["links"]:
                if(':' not in l["title"]):
                        knowledge_base[word][0].append(l["title"])
        except:
            continue


def generate_secondary(word, limit = 500):
    global knowledge_base
    if word not in knowledge_base:
        generate(word)
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    knowledge_base[word].append([])
    for i in knowledge_base[word][-2]:
        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": i,
            "prop": "links",
            "pllimit": limit
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        PAGES = DATA["query"]["pages"]
        for k, v in PAGES.items():
            try:
                for l in v["links"]:
                    if(':' not in l["title"]) :
                        if(l["title"] not in knowledge_base[word][-2]):
                            knowledge_base[word][-1].append(l["title"])
            except:
                continue

def dump_base():
    global knowledge_base
    print(knowledge_base)
    try:
        with open("json/base.json", "w") as write_file:
            json.dump(knowledge_base, write_file, indent=4)
    except:
        print("Error in dumping JSON!")

generate_secondary("Electronics", 500)
generate_secondary("Computer science", 500)
generate_secondary("Mathematics", 500)
generate_secondary("Medicine", 500)
generate_secondary("Country", 500)
generate_secondary("Animal", 500)
generate_secondary("Business", 500)
dump_base()