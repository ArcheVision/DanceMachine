__author__ = 'Laur'
import collections
import sys
import vlc
import time
import os
from tkinter import *
import threading
import easygui
from PyQt5 import uic
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QApplication, QDialog


#form_class = uic.loadUiType("AppUI.ui")[0]


class Song(object):


    dancesPresent = {}

    def __init__(self, artist, songName, dance, tempo = 0, ispresent = False, osPath = "", rating = 0, playcount = 0, difficulty = 0):
        if dance not in Song.dancesPresent.keys():
            Song.dancesPresent[dance] = 1
        self.__artist = artist
        self.__title = songName
        self.__dances = [dance]
        self.__ispresent = ispresent
        self.__ospath = osPath
        self.__rating = rating
        self.__playcount = playcount
        self.__islocal = False
        self.__localpath = ""
        self.__difficulty = difficulty
        self.__tempo = tempo


    @staticmethod
    def differentDances():
        return len(Song.listDances())

    @staticmethod
    def listDances():
        return list(Song.dancesPresent.keys())


    #### List view etc ####
    def listView(self):
        return self.__artist, self.__title, self.__dances


    #### Artist accessors ####
    def artist(self):
        return self.__artist

    def setArtist(self, artist):
        self.__artist = artist


    #### Title accessors ####
    def title(self):
        return self.__title

    def setTitle(self,newtitle):
        self.__title = newtitle


    #### Dances accessors ####
    def dances(self):
        return self.__dances

    def addDance(self, newdance):
        if newdance in self.__dances:
            Song.dancesPresent[newdance] += 1
            pass
        else:
            if newdance not in Song.dancesPresent.keys():
                Song.dancesPresent[newdance] = 1
            self.__dances.append(newdance)


    def remDance(self, rmdance):
        if rmdance in self.__dances:
            self.__dances.remove(rmdance)
            if Song.dancesPresent[rmdance] == 1:
                del(Song.dancesPresent[rmdance])
            else:
                Song.dancesPresent[rmdance] -= 1

    #### Present/Missing accessors ####
    def isPresent(self):
        return self.__ispresent

    def isMissing(self):
        return not self.__ispresent

    def setPresent(self):
        self.__ispresent = True

    def setMissing(self):
        self.__ispresent = False


    #### Os Path accessors ####
    def getPath(self):
        if self.__ispresent:
            return self.__ospath
        else:
            return "N/A"

    def setPath(self, newPath):
        self.__ospath = newPath
        self.setPresent()

    def delPath(self):
        self.__ospath = ""
        self.setMissing()


    #### Rating accessors ####
    def getRating(self):
        return self.__rating

    def setRating(self, newRating):
        self.__rating = newRating

    def incRating(self):
        self.__rating += 0.5
        if self.__rating > 5:
            self.__rating = 5

    def decRating(self):
        self.__rating -= 0.5
        if self.__rating < 0:
            self.__rating = 0


# ### Difficulty accessors ####
def getDifficulty(self):
    return self.__difficulty


def setDifficulty(self, newDifficulty):
    self.__difficulty = newDifficulty


def incDifficulty(self):
    self.__difficulty += 1
    if self.__difficulty > 5:
        self.__difficulty = 5


def decDifficulty(self):
    self.__difficulty -= 1
    if self.__difficulty < 0:
        self.__difficulty = 0


    #### PlayCount accessors ####
    def getPlayCount(self):
        return self.__playcount

    def setPlayCount(self, newcount):
        self.__playcount = newcount

    def addPlayCount(self):
        self.__playcount += 1

    def cutPlayCount(self):
        self.__playcount -= 1


    #### Local File management ####
    def isLocal(self):
        return self.__islocal

    def localPath(self):
        return self.__localpath

    def makeLocal(self, address):
        self.__islocal = True
        self.__localpath = address

    def remLocal(self):
        self.__islocal = False
        self.__localpath = ""





class Player(Frame):

    def __init__(self, parent, songs = [], artists = []):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.__songs = songs
        self.__artists = artists
        self.vlc = vlc.Instance()
        self.player = self.vlc.media_player_new()
        self.initUI()



    def initUI(self):
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)


        quitButton = Button(self, text="Quit",
                            command=self.quit)
        quitButton.place(x=550, y=50)

        playButton = Button(self, text="Play",
                            command = self.play())
        playButton.place(x=550, y=90)

        pauseButton = Button(self, text="Pause",
                            command=self.play())

        pauseButton.place(x=550, y=130)

        stopButton = Button(self, text="Stop",
                            command=self.play())

        stopButton.place(x=550, y=170)

        songList = Listbox(self, width=80, height=30)
        playables = []
        num = 1
        for s in self.__songs:
            if s.isPresent():
                songString = (str(num) + ":\t" + str(s.dances()) + " " + s.artist() + " - " + s.title())
                songList.insert(END, songString)
                playables.append(s)
                num += 1
        songList.bind("<<ListboxSelect>>", self.onSelect)
        songList.place(x=30, y = 30)


    def onSelect(self, val):

        print(val)
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var.set(value)


    def play(self):
        pass



# class Player(QWidget):
#
#     def __init__(self, songs, artists, parent=None):
#         super(Form, self).__init__()
#
#         #self.setStyleSheet('''
#         #    QWidget {
#         #      background-color: #000;
#         #      color: #FFF;
#         #    }
#         #    QLabel {
#         #      font-size: 18px;
#         #    }
#         #    ''')
#         self.__songs = songs
#         self.__artists = artists
#
#
#         self.screen = QWidget()
#         self.screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.vlc = vlc.Instance()
#         self.player = self.vlc.media_player_new()
#         self.player.set_xwindow(self.screen.winId())
#
#         #self.mainBox = QVBoxLayout()
#         #self.setLayout(self.mainBox)
#         #self.mainBox.addWidget(self.screen)
#
#         #self.label = QLabel()
#         #self.label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
#         #self.mainBox.addWidget(self.label)
#         #self.label.hide()
#
#         #self.slider = Slider(Qt.Horizontal, self)
#         #self.slider.player = self.player
#         #self.slider.setMaximum(65536)
#         #self.slider.sliderMoved.connect(self.setPosition)
#         #self.mainBox.addWidget(self.slider)
#         #self.slider.hide()
#
#         #self.timer = QTimer(self)
#         #self.timer.setInterval(200)
#         #self.timer.timeout.connect(self.update)
#
#         #self.files = []
#         #for arg in sys.argv[1:]:
#         #    media = self.vlc.media_new(arg)
#         #    self.files.append(File(arg, media))
#             # #    loc = "d:\\Muusika\\python\\tisko\\"
#             ##    for item in os.listdir(loc):
#             ##        if item.endswith(".mp3"):
#             ##            media = self.vlc.media_new(loc)
#             ##            self.files.append(File(loc+item, media))
#
#         #self.index = 0
#         #self.play()
#
#
#     def play(self):
#         self.player.set_media(self.files[self.index].media)
#         self.player.play()
#         m = self.player.get_media()
#         self.label.setText(' '.join([
#             '%d / %d' % (self.index + 1, len(self.files)),
#             self.files[self.index].path,
#         ]))
#         self.timer.start()
#
#
#     def playOrPause(self):
#         self.player.pause()
#         self.timer.start()
#
#
#     def setPosition(self, position):
#         self.player.set_position(position / 65536)
#
#
#     def update(self):
#         self.slider.setValue(self.player.get_position() * 65536)
#         if not self.player.is_playing():
#             self.timer.stop()
#
#
#     def mspf(self):
#         return int(1000 // (self.player.get_fps() or 25))
#
#
#     def keyPressEvent(self, event):
#         if event.key() == Qt.Key_Q:
#             sys.exit(0)
#         elif event.key() == Qt.Key_D:
#             self.player.set_time(self.player.get_time() + 3000)
#         elif event.key() == Qt.Key_A:
#             self.player.set_time(self.player.get_time() - 3000)
#         elif event.key() == Qt.Key_S:
#             self.player.set_time(self.player.get_time() + 10000)
#         elif event.key() == Qt.Key_W:
#             self.player.set_time(self.player.get_time() - 10000)
#         elif event.key() == Qt.Key_C:
#             self.player.set_time(self.player.get_time() + self.mspf())
#         elif event.key() == Qt.Key_X:
#             self.player.set_time(self.player.get_time() - self.mspf())
#         elif event.key() == Qt.Key_Space:
#             self.playOrPause()
#         elif event.key() == Qt.Key_F:
#             filename = os.path.join(os.path.expanduser("~"),
#                                     os.path.basename(self.files[self.index].path) + "-" + str(time.time()) + ".png")
#             self.player.video_take_snapshot(0, filename, 0, 0)
#         elif event.key() == Qt.Key_J:
#             self.index += 1
#             if self.index == len(self.files):
#                 self.index = 0
#             self.play()
#         elif event.key() == Qt.Key_K:
#             self.index -= 1
#             if self.index < 0:
#                 self.index = len(self.files) - 1
#             self.play()
#         elif event.key() == Qt.Key_E:
#             if self.label.isHidden():
#                 self.label.show()
#                 self.slider.show()
#             else:
#                 self.label.hide()
#                 self.slider.hide()
#         elif event.key() == Qt.Key_1:
#             self.player.set_rate(1)
#         elif event.key() == Qt.Key_2:
#             self.player.set_rate(1.2)
#         elif event.key() == Qt.Key_3:
#             self.player.set_rate(1.5)
#         elif event.key() == Qt.Key_4:
#             self.player.set_rate(2)
#         elif event.key() == Qt.Key_5:
#             self.player.set_rate(3)
#
#
# class Slider(QSlider):
#     def __init__(self, *args):
#         super(QSlider, self).__init__(*args)
#         self.player = None
#
#     def mousePressEvent(self, event):
#         self.setValue(self.maximum() * event.x() / self.width())
#         self.player.set_position(self.value() / self.maximum())
#
#
# # class Player(QtGui.QMainWindow, form_class):
# #
# #     def __init__(self, parent=None):
# #         QMainWindow.__init__(self, parent)
# #         self.setupUI(self)
# #         self.setWindowTitle("DanceMachine")
# #         # creating a basic vlc instance
# #         self.instance = vlc.Instance()
# #     #     # creating an empty vlc media player
# #         self.mediaplayer = self.instance.media_player_new()
# #     #
# #         #self.createUI()
# #         self.isPaused = False
#
#






"""
Here be lions.
And some pretty creepy advanced stuff to be used as a reference.




#! /usr/bin/python

#
# Qt example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#



class Player(QtGui.QMainWindow):
    ""A simple Media Player using VLC and Qt
    ""
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False

    def createUI(self):
        ""Set up the user interface, signals & slots
        ""
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.hbuttonbox = QtGui.QHBoxLayout()
        self.playbutton = QtGui.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)

        self.stopbutton = QtGui.QPushButton("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                     self.Stop)

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        open = QtGui.QAction("&Open", self)
        self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def PlayPause(self):
        ""Toggle play/pause status
        ""
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        ""Stop player
        ""
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def OpenFile(self, filename=None):
        ""Open a media file in a MediaPlayer
        ""
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File")#, user.home)
        if not filename:
            return

        # create the media
        self.media = self.instance.media_new(unicode(filename))
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform == "linux2": # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()

    def setVolume(self, Volume):
        ""Set the volume
        ""
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        ""Set the position
        ""
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        ""updates the user interface""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())














class OrderedSet(collections.MutableSet):
#Ordered set class copied from http://code.activestate.com/recipes/576694/


    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

"""