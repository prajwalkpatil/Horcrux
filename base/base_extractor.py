import json

copy_base = {}

with open("json/base.json") as json_file:
    knowledge_base = json.load(json_file)    


for i in knowledge_base:
    print(i)
    copy_base[i] = []
    for j in knowledge_base[i]:
        temp_set = set(j)
        copy_base[i].append(list(temp_set))


try:
    with open("json/base_refined.json", "w") as write_file:
        json.dump(copy_base, write_file, indent=4)
except:
    print("Error in dumping JSON!")
