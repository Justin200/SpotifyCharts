# class Artist:
#     def __init__(self, artistName, artistMonthlyListeners):
#         self.artistName = artistName
#         self.artistMonthlyListeners = artistMonthlyListeners

#     def __str__(self):
#         return self.artistName + ',' + self.artistMonthlyListeners

#     def __repr__(self):
#         return self.artistName + ',' + self.artistMonthlyListeners

# artistList = []

# artistList.append(Artist(artistName, artistMonthlyListeners))





# print artistName + ": " + str(artistMonthlyListeners)


def addArtistToJSON(path, filename, rank, artist, monthlyListeners, url):
    filePathName = './' + path + '/' + fileName + '.json'
    jsonRank = {'rank': rank}
    jsonArtist = {'artist': artist}
    jsonMonthlyListeners = {'monthlylisteners': monthlyListeners}
    jsonURL = {'url': url}

    with open('filePathName') as f:
        data = json.load(f)
    
    data.update(jsonRank)
    data.update(jsonRank)
    data.update(jsonMonthlyListeners)
    data.update(jsonURL)

    with open('filePathName', 'w') as f:
        json.dump(data, f)



        f.write(json.dumps(data, indent=4))



        #1: Today’s Top Hits 2: Viva Latino 3: Rap Caviar  4: Top Songs All Time
