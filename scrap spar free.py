import requests
#install beatifulsoup4
from bs4 import BeautifulSoup
import json
import time

#check if isin.json exists
try:
    with open('spar_isins.json', 'r') as json_file:
        allisin = json.load(json_file)
except:
    #https://www.flatex.at/produkte-handel/produkte/sparplaene/ergebnisse/?tx_ftfondssearch_search%5B%40widget_0%5D%5Bcategory%5D=-1&tx_ftfondssearch_search%5B%40widget_0%5D%5BcurrentPage%5D=24&tx_ftfondssearch_search%5B%40widget_0%5D%5Bisin%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Bpremiumagio%5D=1&tx_ftfondssearch_search%5B%40widget_0%5D%5Bpublisher%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Brisk%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Bsavingplan%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Btitle%5D= is page 24
    all = []
    for i in range(1, 27):
        #get all links to sparplan pages
        all.append('https://www.flatex.at/produkte-handel/produkte/sparplaene/ergebnisse/?tx_ftfondssearch_search%5B%40widget_0%5D%5Bcategory%5D=-1&tx_ftfondssearch_search%5B%40widget_0%5D%5BcurrentPage%5D='+str(i)+'&tx_ftfondssearch_search%5B%40widget_0%5D%5Bisin%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Bpremiumagio%5D=1&tx_ftfondssearch_search%5B%40widget_0%5D%5Bpublisher%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Brisk%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Bsavingplan%5D=&tx_ftfondssearch_search%5B%40widget_0%5D%5Btitle%5D=')

    allisin = []
    #loop through all links and extract class="hideIfOpen td-isin show-for-medium"
    for link in all:
        #delay 1s
        time.sleep(1)
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        isin = soup.find_all('td', attrs={'class': 'hideIfOpen td-isin show-for-medium'})
        isin = [i.text for i in isin]
        #trim whitespaces
        isin = [i.strip() for i in isin]
        allisin+=isin
        print(len(allisin))
    #save json
    with open('spar_isins.json', 'w') as f:
        json.dump(allisin, f)

#add "free":true to all etries in everyting.json with isin in allisin
with open('everything.json') as json_file:
    data = json.load(json_file)
    for entry in data:
        if entry['number'] in allisin:
            entry['sparkosten'] = "keine"
    with open('everything.json', 'w') as f:
        json.dump(data, f)
