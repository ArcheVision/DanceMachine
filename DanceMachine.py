__author__ = 'Laur'

import importLists
import os
from classes import Song, Player
import vlc
import pygame
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


def setPath():
    try:
        with open("folders.path", encoding = "UTF-8") as f:
            lines = f.readlines()
    except:
        return []
    num = 1
    path = []
    #print("Currently available media folders:")
    for l in lines:
        #print(num, "\t", l.strip(), ("OK" if os.path.exists(l.strip()) else "Inaccessible" )  )
        if os.path.exists(l.strip()):
            path.append(l.strip())
        num += 1
    return path


def detectFolders(artists,mediadir):
    num = 1
    avail = {}
    artistsFound = []
    for folder in mediadir:
        for e in os.listdir(folder):
            if e in artists and e not in artistsFound:
                #print(num, "\tArtisti", e, "kaust on olemas: ", folder + e + "/")
                avail[e] = folder + e + "/"
                artistsFound.append(e)
                num += 1
    return avail


def getArtists(masterlist, artists):
    for i in masterlist:
        if i["artist"] not in artists:
            artists.append(i["artist"])

def printSongs(masterlist):
    rows = []
    for i in masterlist:
        rows.append(i["artist"] + "\t" + i["song"] + "\t(" + str(i["dances"]) + ")")
    for i in (sorted(rows)):
        print(i)

def find(masterlist, dances):
    found = False
    while not found:
        inp = input("Find by (A)uthor, (S)ong or (D)ance?")
        if inp.lower() == "a":
            otsi = "artist"
            found = True
        elif inp.lower() == "s":
            otsi = "song"
            found = True
        elif inp.lower() == "d":
            otsi = "dances"
            found = True
    inp = input("Search: ")
    rows = []
    for i in masterlist:
        if inp in i[otsi]:
            rows.append(i["artist"] + "\t" + i["song"] + "\t(" + str(i["dances"]) + ")")
    for i in (sorted(rows)):
        print(i)

def countArtists(masterlist):
    inp = input("Enter minimum song count threshold for artist to be displayed: ")
    count = {}

    for i in masterlist:
        if i["artist"] in count.keys():
            count[i["artist"]] += 1
        else:
            count[i["artist"]] = 1
    print(count)
    for keys in count:
        if count[keys] >= inp:
            print(keys, "\t",count[keys])

def numSongs():
    print(len(songs))

def loadFiles(songs, artists, mediadir):
    foldersOK = detectFolders(artists, mediadir)
    folderList = []
    for i in sorted(foldersOK.keys()):
        for song in songs:
            if song.artist() == i:
                reply = findsong(i, song.title(), foldersOK[i])
                if reply != None:
                    #print(reply)
                    song.setPath(reply)



def findsong(artist, title, filePath):
    for root, dirs, files in os.walk(filePath):
        for name in dirs:
            findsong(artist, title, os.path.join(root, name))
        for name in files:
            if title in name:
                return os.path.join(root,name)


def qtPlayer(songs, artists):
    playables = []
    for song in songs:
        if song.isPresent():
            playables.append(song)
    if len(playables) == 0:
        print("no songs available")
        return
    else:
        end = False
        player = vlc.MediaPlayer()
        while not end:
            n = 1
            print("Available commands: Play \t Pause \t Stop \t Exit \t - type and press >>Enter<<")
            ask = input("Command:  ")
            if ask.lower() == "play":

                ask2 = input("Choose filter: (All) \t By (Artist) \t By (Dance) ")
                if ask2.lower() == "all" or ask2.lower() == "":
                    for i in playables:
                        print(n, "\t", i.artist(), "-", i.title(), ":", i.dances())
                        n += 1
                elif ask2.lower() == "artist":
                    for e in sorted(artists):
                        print(e)
                    ask3 = input("Enter artist name: ")
                    num = 1
                    for e in playables:
                        if e.artist() == ask3:
                            print(num, "\t", e.artist(), "-", e.title(), ":", e.dances())
                            num += 1
                        else:
                            num += 1

                elif ask2.lower() == "dance":
                    for e in playables:
                        print(str(e.dances()))
                    ask3 = input("Which dance: ")
                    num = 1
                    for e in playables:
                        if ask3 in e.dances():
                            print(num, "\t", e.artist(), "-", e.title(), ":", e.dances())
                            num += 1
                        else:
                            num += 1

                inp = input("Choose a song to play: ")
                if inp.isdigit():
                    player = vlc.MediaPlayer(playables[int(inp) - 1].getPath())
                    player.play()
                else:
                    pass
            if ask.lower() == "conf":
                break
            elif ask.lower() == "pause":
                player.pause()
            elif ask.lower() == "stop":
                player.stop()
            #elif isinstance(inp, int) and inp in range(len(playables)):
            else:
                pass


def pygPlayer(songs):
    playables = []
    for song in songs:
        if song.isPresent() and song.getPath().endswith("mp3"):
            playables.append(song)
    if len(playables) == 0:
        print("no songs available")
        return
    else:
        pygame.mixer.init()
        while not end:
            n = 1
            print("available songs:")
            for i in playables:
                print(n, "\t", i.artist(), "-", i.title(), ":", i.dances())
                n += 1
            inp = input("Choose a song to play: ")
            if inp.lower() == "conf":
                break
            elif isinstance(inp, int) and inp in range(len(playables)):
                pygame.mixer.music.load(playables[inp].getPath())
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue


def loadPlayer():
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    #player.resize(640, 480)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())



masterlist, dances, songs = importLists.prepare()
mediadir = setPath()
artists = []
getArtists(masterlist, artists)
loadFiles(songs, artists, mediadir)
qtPlayer(songs, artists)
loadplayer()
# if __name__ == "__main__":
#     app = QtGui.QApplication(sys.argv)
#     player = Player()
#     player.show()
#     player.resize(640, 480)
#     if sys.argv[1:]:
#         player.OpenFile(sys.argv[1])
#     sys.exit(app.exec_())




end = False
while not end:
    comm = input("Insert command: ").upper()
    if comm == "EXIT":
        end = True
    if comm == "PATH":
        mediadir = setPath()
    if comm == "LISTDIR":
        detectFolders(artists,mediadir)
    if comm == "SONGS":
        printSongs(masterlist)
    if comm == "FIND":
        find(masterlist,dances)
    if comm == "ARTISTS":
        countArtists(masterlist)
    if comm == "TOTAL":
        numSongs()
    if comm == "DANCES":
        print(Song.differentDances())
        print(Song.listDances())
    if comm == "LOADF":
        loadFiles(songs, artists, mediadir)
    if comm == "PLAYER":
        qtPlayer(songs, artists)
    if comm == "PYGPLAYER":
        pygPlayer(songs)