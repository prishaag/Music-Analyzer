#William's file (all work is done by William)
import sqlite3
import billboard

def createMasterTable(conn, cur):
    cur.execute('''DROP TABLE IF EXISTS master''')
    cur.execute('''CREATE TABLE master (id INTEGER PRIMARY KEY, title TEXT UNIQUE, artist TEXT)''')
    conn.commit()

def insertMasterTable(conn, cur, title, artist):
    for track in soupList:
        cur.execute('''INSERT OR IGNORE INTO master (title, artist), values(?, ?)''', (title, artist))
        conn.commit()

def insertBillboardSongs(conn, cur):
    chart = billboard.ChartData('hot-100')
    for song in chart:
        insertMasterTable(conn, cur, song.title, song.artist)

