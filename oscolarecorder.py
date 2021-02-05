from OscOlaRecorder.ola_recorder import OlaRecorder
from OSC import OSCServer, OSCClient, OSCMessage, ThreadingOSCServer
import sys
from time import sleep
import time
import types
import os
import subprocess
import threading
from threading import Thread
from os import listdir
from os.path import isfile, join
from random import shuffle
from random import sample
from ola_recorder import OlaRecorder

# TODO: add code to create "/home/pi/myoscrecs" folder if not present.
os.chdir("/home/pi/myoscrecs")
time.sleep(5)

# TODO: Add code to retreive ip address automatically (ethernet IP prioritized, wifi IP if ethernet not connected)
server = ThreadingOSCServer(
    ("10.1.1.143", 7002)
)  # the ip adress of your pi/device goes here and the incoming OSC port you would like to use, i used 7002 for the port - the incoming port should be matched on your TouchOSC / OSC app
client = OSCClient()

# def handle_timeout(self):
# 	print ("I'm IDLE")
# This here is just to do something while the script recieves no information....
# server.handle_timeout = types.MethodType(handle_timeout, server)

# Set to loop Global Var
loop = 1
# Duration Time Global Var
loopd = 10
# Set to Shuffle Global Var
shuffleloop = 1

ola = OlaRecorder()

# Function to record DMX input using ola_recorder program and save into banks numbered 1-XX
# Recording starts and stops when triggered via OSC.
def record(self, path, tags, args, source):
    split = path.split("/1/toggle")
    x = split.pop()
    state = int(args[0])
    print ("Record", x)
    if state == 1:
        ola.record(x)
    else:
        ola.kill_record()


# Function to Playback recorded DMX clips using ola_recorder program -  Playback starts and stops when triggered via OSC.
def playback(path, tags, args, source, ola):
    split = path.split("/2/push")
    y = split.pop()
    state = int(args[0])
    print ("Playback:", y)
    if state == 1:
        ola.play(y)

# Function to kill all playback
def stopallplay(path, tags, args, source):
    state = int(args[0])
    print ("Stop All Playback:", state)
    if state == 1:
        ola.kill_play()


# Function to kill all recording
def stopallrec(path, tags, args, source):
    state = int(args[0])
    print ("Stop All Recording:", state)
    if state == 1:
        ola.kill_record()

# Function to set loop duration
def loopduration(path, tags, args, source):
    global loopd
    loopd = int(args[0])

# 		print "Loop Duration", loopd;

# Function to play all recorded clips in sequence
def playall(path, tags, args, source):
    global loop
    state = int(args[0])
    loop = state
    if loop == 1:
        playallloop()


# Function to shuffle order of clips playing back
def shuffler(path, tags, args, source):
    global shuffleloop
    state = int(args[0])
    shuffleloop = state
    # if shuffle == 1:


# Function to loop single file
def playallloop():
    global loop
    global loopd
    global shuffleloop
    while loop == 1:
        if loop == 0:
            ola.kill_play()
            break
        print ("Play on Loop")
        file_list = os.listdir(r"/home/pi/myoscrecs")
        # file_list_sorted = sorted([file_list, key=int)
        file_shuffle = sample(file_list, len(file_list))
        if shuffleloop == 0:
            files = sorted(file_list)
        else:
            files = file_shuffle
            for i in files:
                if loop == 0:
                    ola.kill_play()
                    break
                print ("Loop Duration", loopd)
                ola.play(i)
                time.sleep(loopd)


# OSC Client message handling -You can increase the amount of record and playback banks by increasing the number 
# from 70 to whatever in the below lines.
for x in range(1, 70):
    server.addMsgHandler("/1/" + "toggle" + repr(x), record)

for y in range(1, 70):
    server.addMsgHandler("/2/" + "push" + repr(y), playback)

server.addMsgHandler("/3/stopallplay", stopallplay)
server.addMsgHandler("/3/stopallrec", stopallrec)
server.addMsgHandler("/3/playall", playall)
server.addMsgHandler("/3/loopduration", loopduration)
server.addMsgHandler("/3/shuffle", shuffler)


# The way that the MSG Handlers work is by taking the values from set accessory, then it puts them into a function
# The function then takes the values and separates them according to their class (args, source, path, and tags)

while True:
    server.handle_request()

server.close()
# This will kill the server when the program ends
