##bfm py

## Program to run half-hourly via cron, in order to process bFM show MP3s, spat out by the studio system.
## The idea is to pick up the file, read the filename and decide which show it is (from a list, populated from xls).
## When the show is determined, check if it needs a custom intro/outro added, or add the standard intro outro to each end.
## Write the new file out to a separate folder, then delete the original file.

## Kind of works, this version 2.

import os
import datetime
import shutil

## Your path
#PATH = os.getcwd()
PATH = "/home/james/podcasts"
PATH_INTRO = PATH + "/intros"

## Generate list from show manifest file
## This file should exist in the main directory, named showManifest.csv
## TODO - add a try/catch to make sure this file exists
def readManifest():
    manifest = []
    manifestInput = open(PATH+"/showManifest.csv","r")
    for line in manifestInput:
        line = line.replace('\n','')
        chunk = line.split(",")
        chunkList = []
        for word in chunk:
            chunkList.append(word)
        manifest.append(chunkList)
    ## Close the manifest file ffs
    manifestInput.close()
    return manifest

## Create a list of lists of files, days of the week from date and air times
## Todo, if the list is empty, quit the programme
def mp3gen():
    manifest = readManifest()
    mp3List = []
    introList = []
    outroList =[]
    #only allow script to find things in the current working dir
#    files = [filename for filename in os.listdir('.') if os.path.isfile(filename)]
#    files = [filename for filename in os.listdir(PATH) if os.path.isfile(filename)]
    files = [filename for filename in os.listdir(PATH) if os.path.isfile(PATH+"/"+filename)]
    for filename in files:
        fileCounter = 0
        if os.path.splitext(filename)[1] == ".mp3":
            showTime = filename[7:11]
            day = datetime.datetime.strptime(filename[0:6], '%d%m%y').strftime('%A')
            mp3List.append(filename)
            for show in manifest:
                if day == show[0] and showTime == show[1]:
                    shutil.move(PATH+"/"+filename, PATH_INTRO+"/"+filename)
                    outputName = "final_"+filename
                    podcastFile = open(PATH+"/done/"+outputName, 'wb')
                    intro = show[3]
                    outro = show[4]
                    shutil.copyfileobj(open(PATH_INTRO+"/"+intro, 'rb'), podcastFile)
                    shutil.copyfileobj(open(PATH_INTRO+"/"+filename, 'rb'), podcastFile)
                    shutil.copyfileobj(open(PATH_INTRO+"/"+outro, 'rb'), podcastFile)
                    podcastFile.close()
                    os.remove(PATH_INTRO+"/"+filename)
                    fileCounter = fileCounter + 1
    print("All done, we wrote",fileCounter,"mp3(s)!")


mp3gen()
