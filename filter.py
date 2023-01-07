import json

with open('everything.json') as data_file:    
    data = json.load(data_file)

#remove all entries with ter < 0
data = [x for x in data if x['ter'] >= 0]

#remove all entries with isDistributing = true
data = [x for x in data if x['isDistributing'] == False]

#writing to a new file
with open('filtered.json', 'w') as outfile:
    json.dump(data, outfile)