#sort everything.json by TER
import json
with open('everything.json') as data_file:    
    data = json.load(data_file)

data.sort(key=lambda x: x['ter'], reverse=True)

with open('everything.json', 'w') as outfile:
    json.dump(data, outfile)