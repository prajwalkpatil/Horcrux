#   Author: Prajwal K. Patil
#   This program is used to clean the generated knowledge base.
#       This program should be executed after executing base_generator.py

import json

copy_base = {}
knowledge_base = {}
knowledge_base_string = {}
#Reading from the json file
with open("./json/base.json","r") as json_file:
    knowledge_base = json.load(json_file)    


#Converting array to set to remove duplicates  
#And then from set to array for JSON serialization.
for i in knowledge_base:
    print(i)
    copy_base[i] = []
    for j in knowledge_base[i]:
        temp_set = set(j)
        copy_base[i].append(list(temp_set))

#Joining seperate attributes to form a string seperated by spaces
for h in knowledge_base:
    knowledge_base_string[h] = []
    for h_array in knowledge_base[h]:
        knowledge_base_string[h].append([])
        base_string = " "
        for keys in h_array:
            keys = keys.lower()
            base_string = base_string + ' ' + keys
        knowledge_base_string[h][-1] = base_string
        

#Dumping the processed file
try:
    with open("json/base_refined.json", "w") as write_file:
        json.dump(copy_base, write_file, indent=4)
except:
    print("Error in dumping JSON!")

#Dumping the joined file
try:
    with open("./json/base_joined.json", "w") as write_file:
        json.dump(knowledge_base_string, write_file, indent=4)
except:
    print("Error in dumping JSON!")
