##bfm py

## Program to run hourly via cron, in order to process bFM show MP3s, spat out by the studio system.
## The idea is to pick up the file, read the filename and decide which show it is (from a list, populated from xls).
## When the show is determined, check if it needs a custom intro/outro added, or add the standard intro outro to each end.
## Write the new file out to a separate folder, then delete the original file.

## Kind of works, this version 8.
## Changes from version 7:
## Slight change to output file, leave files in temp and let shell script take care, so mp3val can run quicker
## Changes from version 6:
## Spaces to tabs, removed james file copy. Going to add proper MP3 handling in next run.
## Changes from version 5:
## Added some basic-ass error handling for crap left in the root folder
## Tried to add a way to handle 3 digit timecodes in csv manifest due to Excel gummo-ness
## Fell into a pit

import os
import datetime
import shutil

## Your path
PATH = "/home/james/podcasts"
PATH_INTRO = PATH + "/intros"
PATH_TEMP = PATH + "/temp"

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

def friendlyName(name):
        for char in [' ']:
                name = name.replace(char, "_")
        return name

## Create a list of lists of files, days of the week from date and air times
## Todo, if the list is empty, quit the programme
def mp3gen():
        manifest = readManifest()
        mp3List = []
        introList = []
        outroList =[]
        #only allow script to find things in the current working dir
        files = [filename for filename in os.listdir(PATH) if os.path.isfile(PATH+"/"+filename)]
        fileCounter = 0
## Do the merging of intro and outro files, for every file we have matching
        for filename in files:
                ## Check if we're dealing with an MP3 here
                try:
                        if os.path.splitext(filename)[1] == ".mp3":
                                #shutil.copy(filename, PATH+"/james/")
                                # Pull the 4 digit timecode from the filename
                                showTime = filename[7:11]
                                # Get the day the show aired
                                day = datetime.datetime.strptime(filename[0:6], '%d%m%y').strftime('%A')
                                # Add the file we're talkin' about to the MP3 List
                                mp3List.append(filename)
                                # Iterate through the full manifest for each show, try to find a match
                                for show in manifest:
                                        # We got a Monday 9am show (etc)? Then boom
                                        if len(show[1]) == 3:
                                                show[1] = "0"+show[1]
                                        if day == show[0] and showTime == show[1]:
                                                # Move the file into a temporary location (we did this to stop the greedy script breaking some other unrelated process)
                                                shutil.move(PATH+"/"+filename, PATH_TEMP+"/"+filename)
                                                # Generate a friendly show-name
                                                friendlyShowName = friendlyName(show[2])
                                                # Generate the full name of the output file
                                                outputName = friendlyShowName+"_"+filename
                                                podcastFile = open(PATH+"/temp/"+outputName, 'wb')
                                                intro = show[3]
                                                outro = show[4]
                                                shutil.copyfileobj(open(PATH_INTRO+"/"+intro, 'rb'), podcastFile)
                                                shutil.copyfileobj(open(PATH_TEMP+"/"+filename, 'rb'), podcastFile)
                                                shutil.copyfileobj(open(PATH_INTRO+"/"+outro, 'rb'), podcastFile)
                                                podcastFile.close()
                                                #shutil.move(PATH_TEMP+"/"+outputName, PATH+"/done/")
                                                os.remove(PATH_TEMP+"/"+filename)
                                                #os.remove(PATH_TEMP+"/*.mp3")
                                                fileCounter = fileCounter + 1
                except:
                        print("I fell into the pit")
                        continue
        print("All done, we wrote",fileCounter,"mp3(s)!")

mp3gen()
