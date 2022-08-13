import json

copy_base = {}

#Reading from the json file
with open("json/base.json") as json_file:
    knowledge_base = json.load(json_file)    


#Converting array to set to remove duplicates  
#And thenfrom set to array for JSON serialization.
for i in knowledge_base:
    print(i)
    copy_base[i] = []
    for j in knowledge_base[i]:
        temp_set = set(j)
        copy_base[i].append(list(temp_set))

#Dumping the processed file
try:
    with open("json/base_refined.json", "w") as write_file:
        json.dump(copy_base, write_file, indent=4)
except:
    print("Error in dumping JSON!")
