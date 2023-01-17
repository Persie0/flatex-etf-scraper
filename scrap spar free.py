import requests
#install beatifulsoup4
from bs4 import BeautifulSoup
import json
import time

#check if links.json exists
try:
    with open('sparlinks.json') as json_file:
        all = json.load(json_file)
except:
    url="https://www.flatex.at/produkte-handel/produkte/sparplaene/ergebnisse/#c26216"    # get html and extract ul class="pagination  text-right" and extract the links with beautifulsoup
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', attrs={'class': 'pagination text-right'})
    links = pagination.find_all('a', href=True)
    #extract the urls
    urls = [link['href'] for link in links]
    #add the base url
    urls = ['https://www.flatex.at' + url for url in urls]
    #visit each url and extraxt ul class="pagination text-right" and extract the links with beautifulsoup, repeat for all new urls
    current=[]
    while len(urls) != len(current):
        current = urls
        new = []
        for url in urls:
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            pagination = soup.find('ul', attrs={'class': 'pagination text-right'})
            links = pagination.find_all('a', href=True)
            new = [link['href'] for link in links]
            #add the base url
            new = ['https://www.flatex.at' + a for a in new]
            #add to urls
        urls = urls + new
        #remove duplicates
        urls = list(set(urls))
        print(len(urls))

    #save json
    with open('sparlinks.json', 'w') as f:
        json.dump(urls, f)
        
#check if isin.json exists) as json_file:
try:
    with open('spar_isins.json', 'r') as json_file:
        allisin = json.load(json_file)
except:
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
    for isin in allisin:
        for entry in data:
            if entry['number'] == isin:
                entry['free'] = True
    with open('everything.json', 'w') as f:
        json.dump(data, f)
