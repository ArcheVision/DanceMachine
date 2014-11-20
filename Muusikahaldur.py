__author__ = 'Laur'
import sys
import os


def lõpeb(filename, ext):
    return filename.endswith(ext)

def checkauthors(authors, author):
    pass



def parseFile(read, dance, authorsong, authors, dances, lineswithunknown, songs, dancelist):
    songfirst = True
    dancename = dance.replace(".txt","")
    linesunknown = lineswithunknown
    artistsong = authorsong
    totsongs = songs
    artists = authors
    print(dancename)
    dancesprocessed = dances
    songno = 1
    for line in read:
        if line == "":
            pass
        elif line.startswith("@"):
            if line.isupper():
                if "@SONG - ARTIST" in line:
                    songfirst = True
                elif "@ARTIST - SONG" in line:
                    songfirst = False
            else:
                if dancename != line[1:-1]:
                    print("Tantsunimi ei klapi hästi")
                    break
                else:
                    if dancename not in dancesprocessed:
                        dancesprocessed.append(dancename)
        elif line.startswith("#"):
            pass
        elif "-" not in line or "–" not in line or "?" in line:
            linesunknown.append(line)
        else:
            if songfirst:
                song, artist = parseRow(line, True)
            else:
                song, artist = parseRow(line, False)
            songno += 1
            lugu = {"artist": artist, "song": song, "dances": {dancename}}

            if not exists(lugu, artistsong, dancename):
                artistsong.append(lugu)
            if artist not in artists:
                artists.append(artist)
    totsongs += songno
    return artistsong, artists, dancesprocessed, linesunknown, totsongs, dancelist

def exists(lugu, artistsong, dancename):
    there = False
    if len(artistsong) == 0:
        pass
    else:
        for e in artistsong:
            if e[artist] == lugu[artist] and e[song] == lugu[song]:
                if dancename in e[dances]:
                    return True
                else:
                    e[dances].add(dancename)
                    return True
        artistsong.append(lugu)
        there = True
    return there

def sortUnknown(linesunknown):
    unknowns = []
    for i in linesunknown:
        if i != "\n":
            unknowns.append(i.strip())
    return unknowns


def parseRow(rida, songFirst):
    kriips = rida.find("-")
    #print(kriips)
    esipool = rida[0:kriips].strip()
    tagupool = rida[kriips + 1:len(rida)].strip()
    if songFirst:
        return esipool, tagupool
    else:
        return tagupool, esipool



def printSongs(artists, artists_and_songs,dancelist):
    artsongs = artists_and_songs[:]
    nr = 1
    for art in sorted(artists):
        for e in artsongs:
            if e[artist] == art:
                print(str(nr) + ": " + e[artist] + " - " + e[song] + " : " + str(e[dances]).join(", "))
                artsongs.remove(e)
                nr += 1

def detectFolders(artists,mediadir):
    num = 1
    for e in os.listdir("d:/meedia/muusika/"):
        if e in artists:
            print(num, "Artisti kaust", e, "on olemas")
            num += 1

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

def findSong(artists, artists_and_songs, unknowns):
    term = input("Input search term: ")
    num = 1
    for e in unknowns:
        if term in e:
            print(num, e)
            num += 1
    for e in artists_and_songs:
        if term in e:
            print(num, e[0], "-", e[1])
            num += 1


txtfiles = []
for e in os.listdir("."):
    if lõpeb(e, ".txt")and not e.startswith("@"):
        txtfiles.append(e)

# total_songs_by_dance = {}                   # Dict  tantsunimi(str):lugusid kokku(int)
# songs_by_dance = {}                         # Dict  tantsunimi(str):(dict) - autor(str):lood(list)
# total_songs_by_artist = {}                  # Dict  autor(str):lugusid kokku(int)
artists_and_songs = []                        # List  index(STRautor, STRloonimi, LISTtantsud) - loo nimi(str):sobivad tantsud(list)
artists = []                                # List  nimekiri erinevatest autoritest
dancesprocessed = []                                 # List  nimekiri erinevatest tantsudest
dancelist = []
lines_with_unknown = []                     # List  read, mida pole võimalik standardtöötlusega rünnata.
totsongs = 0
mediadir = "d:/meedia/muusika/"



for e in txtfiles:
    #total_songs_by_dance[e] = 0
    with open(e, encoding="UTF-8") as f:
        read = f.readlines()
    artists_and_songs, artists, dancesprocessed, lines_with_unknown, totsongs,dancelist = parseFile(read, e, artists_and_songs, artists, dancesprocessed, lines_with_unknown, totsongs, dancelist)
    #total_songs_by_dance, songs_by_dance, total_songs_by_artist, songs_by_artist, artists, dances, lines_with_unknown = parseFile(read, e, total_songs_by_dance, songs_by_dance, total_songs_by_artist, songs_by_artist, artists, dances, lines_with_unknown)

print("Teadmata sisuga read")
unknowns = sortUnknown(lines_with_unknown)
print(len(unknowns),"tunnistamatut nime:", unknowns)
print("\n")
print("Läbi vaadatud " + str(len(dancesprocessed)) + " tantsu:")
print(str(dancesprocessed))
nr = 1
print("Nimekirjas " + str(len(artists_and_songs)) + " individuaalset lugu:")
# for e in artists_and_songs:
#     print(str(nr) + ": " + e[0] + " - " + e[1])
#     nr += 1
print("läbi käidud " + str(totsongs) + " lugu, nende hulgas " + str(len(artists_and_songs)) + "individuaalset pala.")
#printSongs(artists, artists_and_songs)
#print(len(artists), "artisti kokku")
#detectFolders(artists)
print(sorted(artists))

end = False
while not end:
    comm = input("Insert command: ")
    if comm == "EXIT":
        end = True
    if comm == "PATH":
        mediadir = setPath(mediadir)
    if comm == "LISTDIR":
        detectFolders(artists,mediadir)
    if comm == "SONGS":
        printSongs(artists,artists_and_songs,dancelist)
    if comm == "FIND":
        findSong(artists, artists_and_songs, unknowns)