__author__ = 'Laur'

import importLists
import os


def setPath(mediadir = "d:/meedia/muusika/"):
    vastus = "0"
    while True:
        print("1. d:/meedia/muusika/")
        print("2. z:/avalik/muusika/")
        vastus = input("vali otsitee")
        if vastus == "1":
            mediadir = "d:/meedia/muusika/"
            break
        elif vastus == "2":
            mediadir = "z:/avalik/muusika/"
            break
    return mediadir


def detectFolders(artists,mediadir):
    num = 1
    for e in os.listdir("d:/meedia/muusika/"):
        if e in artists:
            print(num, "Artisti kaust", e, "on olemas")
            num += 1


def getArtists(masterlist, artists):
    for i in masterlist:
        if i["artist"] not in artists:
            artists.append(i)

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
    count = {}

    for i in masterlist:
        if i["artist"] in count.keys():
            count[i["artist"]] += 1
        else:
            count[i["artist"]] = 1
    print(count)
    for keys in count:
        if count[keys] > 4:
            print(keys, "\t",count[keys])





masterlist, dances = importLists.prepare()
mediadir = "d:/meedia/muusika/"
artists = []
getArtists(masterlist, artists)



end = False
while not end:
    comm = input("Insert command: ")
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