__author__ = 'Laur'

import sys
import os

def process(read, masterlist, tundmatud, dances):
    dance = ""
    songfirst = True
    songno = 0
    for rida in read:
        #print("Töötlen:", rida, end="")
        lugu = {}
        if rida == "" or rida == None or rida.startswith("#"):
            pass
        elif rida.startswith("@"):
            if rida.isupper():
                if "@SONG - ARTIST" in rida:
                    songfirst = True
                    #print("Vaatan ridu: Lugu - Autor")
                elif "@ARTIST - SONG" in rida:
                    songfirst = False
                    #print("Vaatan ridu: Autor - Lugu")
            else:
                dance = rida[1:-1]
                dances.add(dance)
        elif rida.startswith("#"):
            pass
        elif "-" in rida or "–" in rida:
            if songfirst:
                song, artist = parseRow(rida, True)
            else:
                song, artist = parseRow(rida, False)
            songno += 1
            lugu = {"artist": artist, "song": song, "dances": {dance}}
            if artist == "?" or song == "?":
                masterlist.append(lugu)
            elif not any(d["artist"] == artist and d["song"] == song for d in masterlist):
                masterlist.append(lugu)
                songno += 1
            else:
                num = -1
                for i, j in enumerate(masterlist):
                    if j["artist"] == artist and j["song"] == song:
                        num = i
                if num > -1:
                    masterlist[num]["dances"].add(dance)
        else:
            if rida != "" and rida != "\n" and rida != " \n":
                lugu = {"artist": "?", "song": rida.strip(), "dances": {dance}}
                masterlist.append(lugu)
        #print("Korras!")
    #print(dance, "tantsust töödeldud", songno, "erinevat lugu")




def parseRow(rida, songFirst):
    if "-" in rida:
        kriips = rida.find("-")
    elif "–" in rida:
        kriips = rida.find("–")
    else:
        return
    #print(kriips)
    esipool = rida[0:kriips].strip()
    tagupool = rida[kriips + 1:len(rida)].strip()
    if songFirst:
        return esipool, tagupool
    else:
        return tagupool, esipool



def prepare(loc = "."):
    txtfiles = []
    for e in os.listdir(loc):
        if e.endswith(".txt") and not e.startswith("@"):
            txtfiles.append(e)
    #print(txtfiles)
    masterlist = []
    tundmatud = []
    dances = set()

    for e in txtfiles:
        #total_songs_by_dance[e] = 0
        with open(e, encoding="UTF-8") as f:
            read = f.readlines()
        #print(e)
        process(read, masterlist, tundmatud, dances)# töötle sisseloetud andmemaht läbi.
    return masterlist, dances



# masterlist, dances = prepare()
# #for i in masterlist:
# #    print(i)
# print("erinevaid lugusid kokku: ", len(masterlist))
#
# num=0
# for i in masterlist:
#     if len(i["dances"]) > 1:
#         #print(i)
#         num += 1
# print(num, "lugu sobib vähemalt kaheks erinevaks tantsuks")
#
# nom = 0
# for i in masterlist:
#     if i["artist"] == "?" or i["song"] == "?":
#         print(i)
#         nom += 1
# print(nom, "lugu nimekirjas sisaldavad tundmatut")
# print(len(dances), dances)