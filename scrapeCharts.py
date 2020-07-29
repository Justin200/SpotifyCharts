#coding: utf-8
import json
import operator
import re
import requests
from bs4 import BeautifulSoup

url5 =  "https://open.spotify.com/playlist/4fC7lFCZnFOa4UaZ6MeJaZ?si=UUhJCwU5TPyYPi-jkThXjA" #my custom playlist
url4 = "https://open.spotify.com/playlist/2YRe7HRKNRvXdJBp9nXFza" #Spotify most played all time
url2 = "https://open.spotify.com/playlist/37i9dQZF1DX10zKzsJ2jva" #Viva Latino
url3 = "https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd" #Rap Caviar
url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" #Today's Top Hits
r = requests.get(url)
r2 = requests.get(url2)
r3 = requests.get(url3)
r4 = requests.get(url4)
r5 = requests.get(url5)
soup = BeautifulSoup(r.content, features="html.parser")
soup2 = BeautifulSoup(r2.content, features="html.parser")
soup3 = BeautifulSoup(r3.content, features="html.parser")
soup4 = BeautifulSoup(r4.content, features="html.parser")
soup5 = BeautifulSoup(r5.content, features="html.parser")
link1 = soup.find_all("a")
link2 = soup2.find_all("a")
link3 = soup3.find_all("a")
link4 = soup4.find_all("a")
link5 = soup5.find_all("a")
combinedLinks = link4 
# print(link4)
#link2 + link3 + link1 + link5

#function that opens listener.json and puts in artist data
def addArtistToJSON(data, filename = 'listeners.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

#remove duplicate artists from sorted JSON file
#Works for removing dupliactes, but now its not sorted
#Also need to fix formatting
def removeDuplicates():
    with open('listeners.json') as f:
        data = json.load(f)
        temp = data['artists']
        unique_stuff = { each['artist'] : each for each in temp }.values()
        final_stuff = {"artists": unique_stuff} 
        
    with open("uniqueArtists.json", "w") as uniqueFile:
        #dumping a string
        json.dump(final_stuff, uniqueFile, indent=4)  
    
#sort the JSON data by monthlylistener key
def sortJSON():
    with open('uniqueArtists.json') as f:
        data = json.load(f)
        temp = data['artists']
        temp.sort(key=operator.itemgetter('monthlylisteners'))
        
    with open("sorted.json", "w") as sortedJsonFile:
        #dumping a string
        json.dump(data, sortedJsonFile, indent=4)

#go through each artist and extract monthly listeners
for link in combinedLinks:
    if "artist" in link.get("href"):
        artistName = link.text
        artistPath = link.get("href")
        artistURL = "https://open.spotify.com" + artistPath 
        artistData = requests.get(artistURL)
        soupArtist = BeautifulSoup(artistData.content, features="html.parser")
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

removeDuplicates()     
sortJSON()
