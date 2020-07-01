import json
import operator
import re
import requests
from bs4 import BeautifulSoup


url4 = "https://open.spotify.com/playlist/2YRe7HRKNRvXdJBp9nXFza"
url2 = "https://open.spotify.com/playlist/37i9dQZF1DX10zKzsJ2jva"
url3 = "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd"
url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
r = requests.get(url)
r2 = requests.get(url2)
r3 = requests.get(url3)
r4 = requests.get(url4)
soup = BeautifulSoup(r.content)
soup2 = BeautifulSoup(r2.content)
soup3 = BeautifulSoup(r3.content)
soup4 = BeautifulSoup(r4.content)
link1 = soup.find_all("a")
link2 = soup2.find_all("a")
link3 = soup3.find_all("a")
link4 = soup4.find_all("a")
print(link4)
combinedLinks = link1 
#+ link2 + link3 + link4

#function that opens listener.json and puts in artist data
def addArtistToJSON(data, filename = 'listeners.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

#remove duplicates in a JSON file
def removeDuplicates():
    ds = json.load('listeners.json') #this contains the json
    unique_stuff = { each['artist'] : each for each in ds }.values()

#sort the JSON data by monthlylistener key
def sortJSON():
    with open('listeners.json') as f:
        data = json.load(f)
        temp = data['artists']
        temp.sort(key=operator.itemgetter('monthlylisteners'))
        #sortedJSON is a string
        sortedJSON = json.dumps(data, f, indent=4)
        #print(sortedJSON)
        
    with open("sorted.json", "w") as sortedJsonFile:
        #dumping a string
        json.dump(sortedJSON, sortedJsonFile)

#go through each artist and extract monthly listeners
for link in combinedLinks:
    if "artist" in link.get("href"):
        artistName = link.text
        artistPath = link.get("href")
        artistURL = "https://open.spotify.com" + artistPath 
        artistData = requests.get(artistURL)
        soupArtist = BeautifulSoup(artistData.content)
        artistLine = soupArtist(text=re.compile('monthly_listeners'))
        artistJSON = json.loads(re.search(r"\{\"external\_urls\"\:.*", artistLine[0]).group()[:-1])
        artistMonthlyListeners = artistJSON['insights']['monthly_listeners']
        
        #convert data to json format and add it to listener.json
        with open('listeners.json') as f:
            data = json.load(f)
            temp = data['artists']
            artistProfileJSON = {"artist": artistName, "monthlylisteners": artistMonthlyListeners, "url": artistURL}
            temp.append(artistProfileJSON)
        addArtistToJSON(data)
        
# removeDuplicates()
sortJSON()