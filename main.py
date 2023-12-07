#William's file (all work is done by William)
import sqlite3
import json
import requests
import os
import re


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createMasterTable(conn, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS master (id INTEGER PRIMARY KEY, title TEXT UNIQUE, artist TEXT)''')
    conn.commit()


def insertBillboardSongs(conn, cur):
    tracks = get25(cur)
    for track in tracks:
        id = track[0]
        title = track[1]
        artist = track[2]
        cur.execute("INSERT OR IGNORE INTO master (id, title, artist) VALUES (?, ?, ?)", (id, title, artist))
    conn.commit()

def get25(cur):
    url = "https://billboard2.p.rapidapi.com/hot_100"

    # date of billboard chart
    querystring = {"date":"2023-12-06"}

    # gets api keys dict
    with open('secrets.json') as f:
            secrets = json.load(f)

    # top 100 song list
    response = requests.get(url, headers=secrets['billboard'], params=querystring)
    top100 = response.json()
    
    # finds last entry in db 
    cur.execute('SELECT MAX(id) FROM master')
    startRank = cur.fetchone()
    
    # if there are no entries, set to 1
    if startRank[0] is None:
        startRank = 1
    else:
        # fetchone return type is a tuple -> startRank[first_element_in_tuple] 
        startRank = startRank[0] + 1
    # creates a list starting at last recorded rank + 1, spanning for 25
    # * is used to unpack range, otherwise it would store [range(params)]
    rankRange = [*range(startRank, startRank + 25)]

    result = []
    for track in top100:
        trackStats = []
        rank = int(track['rank'])
        # adds 25 songs in rank range
        if rank in rankRange:
            title = track['title' ]
            title = title.replace("&#039;", "'")
            artist = track['artist']
            trackStats.append(rank)
            trackStats.append(title)
            trackStats.append(artist)
            result.append(trackStats)
    return result

def main():
    cur, conn = setUpDatabase('database.db')
    #createMasterTable(conn, cur)
    #insertBillboardSongs(conn, cur)
    
main()
    

# example data
# {'artist': 'Big Sean', 'title': 'Why Would I Stop?', 'last_week': '-', 'rank': '97', 'award': True, 'image': 'https://charts-static.billboard.com/img/2011/01/big-sean-obf-180x180.jpg', 'peak_position': '97', 'weeks_on_chart': '1'}, 
# {'artist': 'Nio Garcia x Anuel AA x Myke Towers x Brray x Juanka', 'title': 'La Jeepeta', 'last_week': '95', 'rank': '98', 'award': True, 'image': 'https://charts-static.billboard.com/img/2020/05/nio-garcia-hk8-la-jeepeta-l5s-180x180.jpg', 'peak_position': '93', 'weeks_on_chart': '5'}, 
# {'artist': 'Migos Featuring YoungBoy Never Broke Again', 'title': 'Need It', 'last_week': '88', 'rank': '99', 'award': False, 'image': 'https://charts-static.billboard.com/img/2020/06/migos-ca0-needit-mz7-180x180.jpg', 'peak_position': '62', 'weeks_on_chart': '15'}, 
# {'artist': 'Ariana Grande &amp; Justin Bieber', 'title': 'Stuck With U', 'last_week': '91', 'rank': '100', 'award': False, 'image': 'https://charts-static.billboard.com/img/2020/05/ariana-grande-da0-stuck-with-u-yqg-180x180.jpg', 'peak_position': '1', 'weeks_on_chart': '18'}]