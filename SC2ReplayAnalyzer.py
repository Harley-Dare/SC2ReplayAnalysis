# Program to analyze Starcraft 2 Replay files (.SC2Replay)
# This is my first Python program, any advice or feedback is more than welcome
# Big credit to the folk(s?) at sc2reader https://github.com/GraylinKim/sc2reader for making this possible

import os
import sc2reader
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

# Brings up GUI to select folder to analyse
def setPath():
    # TODO: Learn more about how tkinter works
    # Create a root Tkinter window (it won't actually appear on the screen)
    root = tk.Tk()
    # Hide the root window since we don't need to show it
    root.withdraw()
    
    print('Please choose a folder containing the SC2 replay files you wish to analyse\n')
    folder = filedialog.askdirectory()
    return folder

# Walk through folder and subfolders, return list of filepaths.
def gatherReplayFilePaths(folder):
    fileList = []
    for folderName, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".SC2Replay"):
                file = folderName + '/' + filename
                fileList.append(file)
    return fileList

# Increments the replay counter by 1
def incrementReplayCount(replayCount):
    replayCount += 1
    return replayCount

# Loads the replay when given a filepath and load level (int)
def loadReplay(file, loadLevel):
    replay = sc2reader.load_replay(file, load_level = loadLevel)
    return replay


# Compares current longest replay to another replay and returns the longer one
def findLongestReplay(longestReplay, replay):
    if longestReplay == None:
        longestReplay = replay
    if replay.game_length > longestReplay.game_length:
        longestReplay = replay
    return longestReplay

# Compares current shortest replay to another replay and returns the shorter one
def findShortestReplay(shortestReplay, replay):
    if shortestReplay == None:
        shortestReplay = replay
    if replay.game_length < shortestReplay.game_length:
        shortestReplay = replay
    return shortestReplay

# returns the sum of totalTime + current replay's length in time
def sumTotalTime(totalTime, replay):
    if totalTime == None:
        totalTime = replay.game_length
    else:
        totalTime += replay.game_length
    return totalTime

# Finds the two races and returns the matchup. Also adds players to a set
def findMatchUp(replay):
    firstFound = False
    firstRace = ""
    secondRace = ""
    playerNumber = 1
    for player in replay.players:
        playersSet.add(player.name)
        if player.pick_race == "Zerg" and playerNumber == 2:
            secondRace = "Zerg"
        elif player.pick_race == "Protoss" and playerNumber == 2:
            secondRace = "Protoss"
        elif player.pick_race == "Terran" and playerNumber == 2:
            secondRace = "Terran"
        if player.pick_race == "Zerg" and playerNumber == 1:
            firstRace = "Zerg"
            playerNumber += 1
        elif player.pick_race == "Protoss" and playerNumber == 1:
            firstRace = "Protoss"
            playerNumber += 1
        elif player.pick_race == "Terran" and playerNumber == 1:
            firstRace = "Terran"
            playerNumber += 1
    matchup = defineMatchup(firstRace, secondRace)
        
    return matchup

# Takes two race inputs and returns the matchup
def defineMatchup(firstRace, secondRace):
    if (firstRace == "Zerg" and secondRace == "Terran") or (firstRace == "Terran" and secondRace == "Zerg"):
        return "ZvT"
    if (firstRace == "Zerg" and secondRace == "Protoss") or (firstRace == "Protoss" and secondRace == "Zerg"):
        return "ZvP"
    if (firstRace == "Terran" and secondRace == "Protoss") or (firstRace == "Protoss" and secondRace == "Terran"):
        return "TvP"
    if (firstRace == "Terran" and secondRace == "Terran"):
        return "TvT"
    if (firstRace == "Protoss" and secondRace == "Protoss"):
        return "PvP"
    if (firstRace == "Zerg" and secondRace == "Zerg"):
        return "ZvZ"
        
replayCount = 0
longestReplay = None
shortestReplay = None
totalTime = None
playersSet = set(())
loadLevel = 2
matchups = {'ZvT' : 0, 'ZvP' : 0, 'TvP' : 0, 'TvT' : 0, 'PvP' : 0, 'ZvZ' : 0,}

folder = setPath()
fileList = gatherReplayFilePaths(folder)

# Main loop
for file in fileList:
    replayCount = incrementReplayCount(replayCount)
    replay = loadReplay(file, loadLevel)
    longestReplay = findLongestReplay(longestReplay, replay)
    shortestReplay = findShortestReplay(shortestReplay, replay)
    totalTime = sumTotalTime(totalTime, replay)
    currentMatchup = findMatchUp(replay)
    matchups[currentMatchup] += 1
    
# TODO: Cleanup print statements, probably write results to a file in the future instead
print(str(replayCount) + ' total replays found and analyzed')
for key in matchups:
    print(key + ': ' + str(matchups[key]))
print(str(Path(longestReplay.filename).name) + ' was the longest replay with a length of ' + str(longestReplay.game_length))
print(str(Path(shortestReplay.filename).name) + ' was the shortest replay with a length of ' + str(shortestReplay.game_length))
print('Total length of all replays: ' + str(totalTime))
averageTime = totalTime / replayCount
print('Average length of replay: ' + str(averageTime))

print('\nGOODBYE')

# TODO: Add a lot more insightful analysis (matchup win rates, player win rates, workers built, map data, etc...)
# TODO: Add some sort of graphical output to better visualize results (maybe export into Google Sheets or something)
# TODO: Make program usable by people other than myself and take feedback
# TODO: Clean up code in general