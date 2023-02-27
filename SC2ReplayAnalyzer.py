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
    # # firstRace = ""
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
    matchup = defineMatchup(firstRace, secondRace, replay)
        
    return matchup

# Takes two race inputs and returns the matchup. Adds replay to matchup specific list
def defineMatchup(firstRace, secondRace, replay):
    if (firstRace == "Zerg" and secondRace == "Terran") or (firstRace == "Terran" and secondRace == "Zerg"):
        zvTMatches.append(replay)
        determineWinningRaceZvT(replay)
        return "ZvT"
    if (firstRace == "Zerg" and secondRace == "Protoss") or (firstRace == "Protoss" and secondRace == "Zerg"):
        zvPMatches.append(replay)
        determineWinningRaceZvP(replay)
        return "ZvP"
    if (firstRace == "Terran" and secondRace == "Protoss") or (firstRace == "Protoss" and secondRace == "Terran"):
        tvPMatches.append(replay)
        determineWinningRaceTvP(replay)
        return "TvP"
    if (firstRace == "Terran" and secondRace == "Terran"):
        tvTMatches.append(replay)
        return "TvT"
    if (firstRace == "Protoss" and secondRace == "Protoss"):
        pvPMatches.append(replay)
        return "PvP"
    if (firstRace == "Zerg" and secondRace == "Zerg"):
        zvZMatches.append(replay)
        return "ZvZ"
    
# Finds the winning race and increments either the Zerg or Terran wins in ZvT (or draw)
def determineWinningRaceZvT(replay):
    global zvTZergWins
    global zvTTerranWins
    global drawGames
    
    winner = replay.winner
    if "(Zerg)" in str(winner):
        zvTZergWins += 1
    elif "(Terran)" in str(winner):
        zvTTerranWins += 1
    else:
        drawGames += 1

# Finds the winning race and increments either the Zerg or Terran wins in ZvT (or draw)
def determineWinningRaceZvP(replay):
    global zvPZergWins
    global zvPProtossWins
    global drawGames
    
    winner = replay.winner
    if "(Zerg)" in str(winner):
        zvPZergWins += 1
    elif "(Protoss)" in str(winner):
        zvPProtossWins += 1
    else:
        drawGames += 1

# Finds the winning race and increments either the Zerg or Terran wins in ZvT (or draw)
def determineWinningRaceTvP(replay):
    global tvPTerranWins
    global tvPProtossWins
    global drawGames
    
    winner = replay.winner
    if "(Terran)" in str(winner):
        tvPTerranWins += 1
    elif "(Protoss)" in str(winner):
        tvPProtossWins += 1
    else:
        drawGames += 1

# Returns player 1's namne and race
def getPlayer1(replay):
    player1 = replay.players
    player1 = str(player1[0]).split('- ')
    return player1[1]

# Returns player 2's namne and race
def getPlayer2(replay):
    player1 = replay.players
    player1 = str(player1[1]).split('- ')
    return player1[1]

# Prints some global stats (total time, average time, etc...)
def printGlobalReplayStats(replayCount, shortestReplay, longestReplay, totalTime):
    averageTime = totalTime / replayCount
    print("%s total replays found and analyzed" % replayCount)
    print("%s vs %s on %s was the shortest replay with a length of %s" % (getPlayer1(shortestReplay), getPlayer2(shortestReplay), shortestReplay.map_name, shortestReplay.length))
    print("%s vs %s on %s was the longest replay with a length of %s" % (getPlayer1(longestReplay), getPlayer2(longestReplay), longestReplay.map_name, longestReplay.length))
    print("Total length of all replays: %s" % totalTime)
    print("Average length of replay: %s" % averageTime)

# Prints Zerg vs Terran Stats
def printZvTStats(zvTmatches, zvTZergWins, zvTTerranWins):
    zvTWinRate = str(round(((zvTZergWins / (len(zvTMatches))) * 100), 2))
    print("Zerg vs Terran Total Games: %s" % len(zvTMatches))
    print("\tZerg Map Wins: %s" % zvTZergWins)
    print("\tTerran Map Wins: %s" % zvTTerranWins)
    print("\tZvT: %s%%" % zvTWinRate)

# Prints Zerg vs Protoss Stats
def printZvPStats(zvPMatches, zvPZergWins, zvPProtossWins):
    zvPWinRate = str(round(((zvPZergWins / (len(zvPMatches))) * 100), 2))
    print("Zerg vs Protoss Total Games: %s" % len(zvPMatches))
    print("\tZerg Map Wins: %s" % zvPZergWins)
    print("\tProtoss Map Wins: %s" % zvPProtossWins)
    print("\tZvP: %s%%" % zvPWinRate)
    
# Prints Terran vs Protoss Stats
def printTvPStats(tvPMatches, tvPTerranWins, tvPProtossWins):
    tvPWinRate = str(round(((tvPTerranWins / (len(tvPMatches))) * 100), 2))
    print("Terran vs Protoss Total Games: %s" % len(tvPMatches))
    print("\tTerran Map Wins: %s" % tvPTerranWins)
    print("\tProtoss Map Wins: %s" % tvPProtossWins)
    print("\tTvP: %s%%" % tvPWinRate)
    
# Prints mirror matchup info
def printMirrorMatchUps(tvTMatches, zvZMatches, pvPMatches):
    print('Terran vs Terran Total Games: ' + str(len(tvTMatches)))
    print('Zerg vs Zerg Total Games: ' + str(len(zvZMatches)))
    print('Protoss vs Protoss Total Games: ' + str(len(pvPMatches)))


######################################################## initializing some variables
replayCount = 0
longestReplay = None
shortestReplay = None
totalTime = None
playersSet = set(())
loadLevel = 2
matchups = {'ZvT' : 0, 'ZvP' : 0, 'TvP' : 0, 'TvT' : 0, 'PvP' : 0, 'ZvZ' : 0,}
zvTMatches = list()
zvPMatches = list()
tvPMatches = list()
zvZMatches = list()
pvPMatches = list()
tvTMatches = list()
zvTZergWins = 0
zvPZergWins = 0
zvTTerranWins = 0
tvPTerranWins = 0
zvPProtossWins = 0
tvPProtossWins = 0
drawGames = 0

#################################################################### Start 
folder = setPath()
fileList = gatherReplayFilePaths(folder)

# Main loop
for file in fileList:
    replay = loadReplay(file, loadLevel)
    if len(replay.players) == 2:
        replayCount = incrementReplayCount(replayCount)
        longestReplay = findLongestReplay(longestReplay, replay)
        shortestReplay = findShortestReplay(shortestReplay, replay)
        totalTime = sumTotalTime(totalTime, replay)
        currentMatchup = findMatchUp(replay)
        matchups[currentMatchup] += 1


# TODO: Cleanup print statements, probably write results to a file in the future instead. these prints are a mess
printGlobalReplayStats(replayCount, shortestReplay, longestReplay, totalTime)
printZvTStats(zvTMatches, zvTZergWins, zvTTerranWins)
printZvPStats(zvPMatches, zvPZergWins, zvPProtossWins)
printTvPStats(tvPMatches, tvPTerranWins, tvPProtossWins)
printMirrorMatchUps(tvTMatches, zvZMatches, pvPMatches)

print('Draw games: ' + str(drawGames))


print('\nGOODBYE')

# TODO: Add a lot more insightful analysis (matchup win rates(done), player win rates, workers built, map data, etc...)
# TODO: Add some sort of graphical output to better visualize results (maybe export into Google Sheets or something)
# TODO: Make program usable by people other than myself and take feedback
# TODO: Add in a team replay to my replay folder and see if ruins everything
# TODO: Clean up code in general