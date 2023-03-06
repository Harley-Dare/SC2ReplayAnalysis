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

# Takes two race inputs and returns the matchup. 
def defineMatchup(firstRace, secondRace, replay):
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

#
    
# Add replay to matchup specific list
def appendMatchupSpecificList(replay, matchup):
    if matchup == "ZvT":
        zvTMatches.append(replay)
    elif matchup == "ZvP":
        zvPMatches.append(replay)
    elif matchup == "TvP":
        tvPMatches.append(replay)
    elif matchup == "ZvZ":
        zvZMatches.append(replay)
    elif matchup == "TvT":
        tvTMatches.append(replay)
    elif matchup == "PvP":
        pvPMatches.append(replay)
    
# Finds the winning race in ZvT (or draw) and returns that race as a string
def determineWinningRaceZvT(replay):
    winner = replay.winner
    if "(Zerg)" in str(winner):
        return "(Zerg)"
    elif "(Terran)" in str(winner):
        return "(Terran)"
    else:
        return "Draw Game"

# Finds the winning race in ZvP (or draw) and returns that race as a string
def determineWinningRaceZvP(replay):
    winner = replay.winner
    if "(Zerg)" in str(winner):
        return "(Zerg)"
    elif "(Protoss)" in str(winner):
        return "(Protoss)"
    else:
        return "Draw Game"

# Finds the winning race in TvP (or draw) and returns that race as a string
def determineWinningRaceTvP(replay):
    winner = replay.winner
    if "(Terran)" in str(winner):
        return "(Terran)"
    elif "(Protoss)" in str(winner):
        return "(Protoss)"
    else:
        return "Draw Game"
# Increment total matchup wins
def incrementMatchUpWins(replay, matchup, zvTZergWins, zvPZergWins, zvTTerranWins, tvPTerranWins, zvPProtossWins, tvPProtossWins, drawGames):
    if matchup == "ZvT":
        winningRace = determineWinningRaceZvT(replay)
        if winningRace == "(Zerg)":
            zvTZergWins += 1
        elif winningRace == "(Terran)" :
            zvTTerranWins += 1
        else:
            drawGames += 1
    elif matchup == "ZvP":
        winningRace = determineWinningRaceZvP(replay)
        if winningRace == "(Zerg)":
            zvPZergWins += 1
        elif winningRace == "(Protoss)" :
            zvPProtossWins += 1
        else:
            drawGames += 1
    elif matchup == "TvP":
        winningRace = determineWinningRaceTvP(replay)
        if winningRace == "(Terran)":
            tvPTerranWins += 1
        elif winningRace == "(Protoss)" :
            tvPProtossWins += 1
        else:
            drawGames += 1
    return zvTZergWins, zvPZergWins, zvTTerranWins, tvPTerranWins, zvPProtossWins, tvPProtossWins, drawGames
        

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
    averageTime = str(averageTime).split('.')
    print("%s total replays found and analyzed" % replayCount)
    print("%s vs %s on %s was the shortest replay with a length of %s" % (getPlayer1(shortestReplay), getPlayer2(shortestReplay), shortestReplay.map_name, shortestReplay.length))
    print("%s vs %s on %s was the longest replay with a length of %s" % (getPlayer1(longestReplay), getPlayer2(longestReplay), longestReplay.map_name, longestReplay.length))
    print("Total length of all replays: %s" % totalTime)
    print("Average length of replay: %s" % averageTime[0])

# Prints Zerg vs Terran Stats
def printZvTStats(zvTmatches, zvTZergWins, zvTTerranWins, zvTshortestReplay, zvTlongestReplay, zvTtotalTime):
    zvTWinRate = str(round(((zvTZergWins / (len(zvTMatches))) * 100), 2))
    print("Zerg vs Terran Total Games: %s" % len(zvTMatches))
    print("\tZerg Map Wins: %s" % zvTZergWins)
    print("\tTerran Map Wins: %s" % zvTTerranWins)
    print("\tZvT: %s%%" % zvTWinRate)
    averageTime = zvTtotalTime / len(zvTMatches)
    averageTime = str(averageTime).split('.')
    print("\t%s vs %s on %s was the shortest ZvT replay with a length of %s" % (getPlayer1(zvTshortestReplay), getPlayer2(zvTshortestReplay), zvTshortestReplay.map_name, zvTshortestReplay.length))
    print("\t%s vs %s on %s was the longest ZvT replay with a length of %s" % (getPlayer1(zvTlongestReplay), getPlayer2(zvTlongestReplay), zvTlongestReplay.map_name, zvTlongestReplay.length))
    print("\tTotal length of ZvT replays: %s" % zvTtotalTime)
    print("\tAverage length of ZvT replay: %s" % averageTime[0])
    print('')

# Prints Zerg vs Protoss Stats
def printZvPStats(zvPMatches, zvPZergWins, zvPProtossWins, zvPshortestReplay, zvPlongestReplay, zvPtotalTime):
    zvPWinRate = str(round(((zvPZergWins / (len(zvPMatches))) * 100), 2))
    print("Zerg vs Protoss Total Games: %s" % len(zvPMatches))
    print("\tZerg Map Wins: %s" % zvPZergWins)
    print("\tProtoss Map Wins: %s" % zvPProtossWins)
    print("\tZvP: %s%%" % zvPWinRate)
    averageTime = zvPtotalTime / len(zvPMatches)
    print("\t%s vs %s on %s was the shortest ZvP replay with a length of %s" % (getPlayer1(zvPshortestReplay), getPlayer2(zvPshortestReplay), zvPshortestReplay.map_name, zvPshortestReplay.length))
    print("\t%s vs %s on %s was the longest ZvP replay with a length of %s" % (getPlayer1(zvPlongestReplay), getPlayer2(zvPlongestReplay), zvPlongestReplay.map_name, zvPlongestReplay.length))
    print("\tTotal length of ZvP replays: %s" % zvPtotalTime)
    print("\tAverage length of ZvP replay: %s" % averageTime)
    print('')
    
# Prints Terran vs Protoss Stats
def printTvPStats(tvPMatches, tvPTerranWins, tvPProtossWins, tvPshortestReplay, tvPlongestReplay, tvPtotalTime):
    tvPWinRate = str(round(((tvPTerranWins / (len(tvPMatches))) * 100), 2))
    print("Terran vs Protoss Total Games: %s" % len(tvPMatches))
    print("\tTerran Map Wins: %s" % tvPTerranWins)
    print("\tProtoss Map Wins: %s" % tvPProtossWins)
    print("\tTvP: %s%%" % tvPWinRate)
    averageTime = tvPtotalTime / len(zvPMatches)
    averageTime = str(averageTime).split('.')
    print("\t%s vs %s on %s was the shortest TvP replay with a length of %s" % (getPlayer1(tvPshortestReplay), getPlayer2(tvPshortestReplay), tvPshortestReplay.map_name, tvPshortestReplay.length))
    print("\t%s vs %s on %s was the longest TvP replay with a length of %s" % (getPlayer1(tvPlongestReplay), getPlayer2(tvPlongestReplay), tvPlongestReplay.map_name, tvPlongestReplay.length))
    print("\tTotal length of TvP replays: %s" % tvPtotalTime)
    print("\tAverage length of TvP replay: %s" % averageTime[0])
    print('')
    
# Prints Zerg vs Zerg Stats
def printZvZStats(zvZMatches, zvZshortestReplay, zvZlongestReplay, zvZtotalTime):
    print("Zerg vs Zerg Total Games: %s" % len(zvZMatches))
    averageTime = zvZtotalTime / len(zvZMatches)
    averageTime = str(averageTime).split('.')
    print("\t%s vs %s on %s was the shortest ZvZ replay with a length of %s" % (getPlayer1(zvZshortestReplay), getPlayer2(zvZshortestReplay), zvZshortestReplay.map_name, zvZshortestReplay.length))
    print("\t%s vs %s on %s was the longest ZvZ replay with a length of %s" % (getPlayer1(zvZlongestReplay), getPlayer2(zvZlongestReplay), zvZlongestReplay.map_name, zvZlongestReplay.length))
    print("\tTotal length of ZvZ replays: %s" % zvZtotalTime)
    print("\tAverage length of ZvZ replay: %s" % averageTime[0])
    print('')

# Prints Terran vs Terran Stats
def printTvTStats(tvTMatches, tvTshortestReplay, tvTlongestReplay, tvTtotalTime):
    print("Terran vs Terran Total Games: %s" % len(tvTMatches))
    averageTime = tvTtotalTime / len(tvTMatches)
    averageTime = str(averageTime).split('.')
    print("\t%s vs %s on %s was the shortest TvT replay with a length of %s" % (getPlayer1(tvTshortestReplay), getPlayer2(tvTshortestReplay), tvTshortestReplay.map_name, tvTshortestReplay.length))
    print("\t%s vs %s on %s was the longest TvT replay with a length of %s" % (getPlayer1(tvTlongestReplay), getPlayer2(tvTlongestReplay), tvTlongestReplay.map_name, tvTlongestReplay.length))
    print("\tTotal length of TvT replays: %s" % tvTtotalTime)
    print("\tAverage length of TvT replay: %s" % averageTime[0])
    print('')

# Prints Protoss vs Protoss Stats
def printPvPStats(pvPMatches, pvPshortestReplay, pvPlongestReplay, pvPtotalTime):
    print("Protoss vs Protoss Total Games: %s" % len(pvPMatches))
    averageTime = pvPtotalTime / len(pvPMatches)
    averageTime = str(averageTime).split('.')
    print("\t%s vs %s on %s was the shortest PvPreplay with a length of %s" % (getPlayer1(pvPshortestReplay), getPlayer2(pvPshortestReplay), pvPshortestReplay.map_name, pvPshortestReplay.length))
    print("\t%s vs %s on %s was the longest PvP replay with a length of %s" % (getPlayer1(pvPlongestReplay), getPlayer2(pvPlongestReplay), pvPlongestReplay.map_name, pvPlongestReplay.length))
    print("\tTotal length of PvP replays: %s" % pvPtotalTime)
    print("\tAverage length of PvP replay: %s" % averageTime[0])
    print('')

# Returns the average length of a game for a certain map
def getMapAverageLength(mapList):
    mapTotalTime = None
    for replay in mapList:
        mapTotalTime = sumTotalTime(mapTotalTime, replay)
    mapAverageTime = mapTotalTime / len(mapList)
    return mapAverageTime

# Returns the total length of all games played on a certain map
def getMapTotalLength(mapList):
    mapTotalTime = None
    for replay in mapList:
        mapTotalTime = sumTotalTime(mapTotalTime, replay)
    return mapTotalTime

def getMapSpecificZvPStats(mapList):
    mapSpecificZvPWinRate = 0
    mapZvPDraws = 0
    mapSpecificZvPZergWins = 0
    mapSpecificZvPProtossWins = 0
    for replay in mapList:
        matchup = findMatchUp(replay)
        if matchup == "ZvP":
            if "(Protoss)" in str(replay.winner):
                mapSpecificZvPProtossWins += 1
            elif "(Zerg)" in str(replay.winner):
                mapSpecificZvPZergWins += 1
            else:
                mapZvPDraws += 1
    zvPGames = mapSpecificZvPProtossWins + mapSpecificZvPZergWins
    if zvPGames > 0:
        mapSpecificZvPWinRate = str(round(((mapSpecificZvPZergWins / (zvPGames)) * 100), 2)) + "%"
    return mapSpecificZvPWinRate, mapZvPDraws, mapSpecificZvPZergWins, mapSpecificZvPProtossWins

# Get map specific ZvT Stats
def getMapSpecificZvTStats(mapList):
    mapSpecificZvTWinRate = 0
    mapZvTDraws = 0
    mapSpecificZvTZergWins = 0
    mapSpecificZvTTerranWins = 0
    for replay in mapList:
        matchup = findMatchUp(replay)
        if matchup == "ZvT":
            if "(Terran)" in str(replay.winner):
                mapSpecificZvTTerranWins += 1
            elif "(Zerg)" in str(replay.winner):
                mapSpecificZvTZergWins += 1
            else:
                mapZvTDraws += 1
    zvTGames = mapSpecificZvTTerranWins + mapSpecificZvTZergWins
    if zvTGames > 0:
        mapSpecificZvTWinRate = str(round(((mapSpecificZvTZergWins / (zvTGames)) * 100), 2)) + "%"
    return mapSpecificZvTWinRate, mapZvTDraws, mapSpecificZvTZergWins, mapSpecificZvTTerranWins

# Get map specific TvP Stats
def getMapSpecificTvPStats(mapList):
    mapSpecificTvPWinRate = 0
    mapTvPDraws = 0
    mapSpecificTvPTerranWins = 0
    mapSpecificTvPProtossWins = 0
    for replay in mapList:
        matchup = findMatchUp(replay)
        if matchup == "TvP":
            if "(Protoss)" in str(replay.winner):
                mapSpecificTvPProtossWins += 1
            elif "(Terran)" in str(replay.winner):
                mapSpecificTvPTerranWins += 1
            else:
                mapTvPDraws += 1
    tvPGames = mapSpecificTvPProtossWins + mapSpecificTvPTerranWins
    if tvPGames > 0:
        mapSpecificTvPWinRate = str(round(((mapSpecificTvPTerranWins / (tvPGames)) * 100), 2)) + "%"
    return mapSpecificTvPWinRate, mapTvPDraws, mapSpecificTvPTerranWins, mapSpecificTvPProtossWins

# Get map specific mirror matchups stats
def getMapSpecificMirrorStats(mapList):
    mapZvZGames = 0
    mapTvTGames = 0
    mapPvPGames = 0 
    for replay in mapList:
        matchup = findMatchUp(replay)
        if matchup == "ZvZ":
            mapZvZGames += 1
        elif matchup == "PvP":
            mapPvPGames += 1
        elif matchup == "TvT":
            mapTvTGames += 1
    return mapZvZGames, mapTvTGames, mapPvPGames
        

# Print map data              Clean this up, way too long and too much global nonsense
def printMapData(mapDict):
    for mapList in mapDict:
        tempAverageTime = getMapAverageLength(mapDict[mapList])
        tempAverageTime = str(tempAverageTime).split('.')
        tempTotalTime = getMapTotalLength(mapDict[mapList])
        mapSpecificZvPWinRate, mapZvPDraws, mapSpecificZvPZergWins, mapSpecificZvPProtossWins = getMapSpecificZvPStats(mapDict[mapList])
        mapSpecificZvTWinRate, mapZvTDraws, mapSpecificZvTZergWins, mapSpecificZvTTerranWins = getMapSpecificZvTStats(mapDict[mapList])
        mapSpecificTvPWinRate, mapTvPDraws, mapSpecificTvPTerranWins, mapSpecificTvPProtossWins = getMapSpecificTvPStats(mapDict[mapList])
        mapZvZGames, mapTvTGames, mapPvPGames = getMapSpecificMirrorStats(mapDict[mapList])
        print("Map: %s\n\tGames played: %s\n\tTotal time played on this map: %s\n\tAverage game length: %s" % (mapList, len(mapDict[mapList]), tempTotalTime, tempAverageTime[0]))
        print("\tZvT games: %s\n\t\tZerg wins: %s\n\t\tTerran wins: %s\n\t\tZvT winrate: %s\n\t\tZvT Draw games: %s" % ((mapSpecificZvTZergWins + mapSpecificZvTTerranWins), mapSpecificZvTZergWins, mapSpecificZvTTerranWins, mapSpecificZvTWinRate, mapZvTDraws))
        print("\tZvP games: %s\n\t\tZerg wins: %s\n\t\tProtoss wins: %s\n\t\tZvP winrate: %s\n\t\tZvP Draw games: %s" % ((mapSpecificZvPZergWins + mapSpecificZvPProtossWins), mapSpecificZvPZergWins, mapSpecificZvPProtossWins, mapSpecificZvPWinRate, mapZvPDraws))
        print("\tTvP games: %s\n\t\tTerran wins: %s\n\t\tProtoss wins: %s\n\t\tTvP winrate: %s\n\t\tTvP Draw games: %s" % ((mapSpecificTvPTerranWins + mapSpecificTvPProtossWins), mapSpecificTvPTerranWins, mapSpecificTvPProtossWins, mapSpecificTvPWinRate, mapTvPDraws))
        print("\tZvZ games: %s\n\tTvT games: %s\n\tPvP games: %s\n" % (mapZvZGames, mapTvTGames, mapPvPGames))


    
######################################################## initializing some variables
replayCount = 0
playersSet = set(())
loadLevel = 2
matchups = {'ZvT' : 0, 'ZvP' : 0, 'TvP' : 0, 'TvT' : 0, 'PvP' : 0, 'ZvZ' : 0,}
zvTMatches = list()
zvPMatches = list()
tvPMatches = list()
zvZMatches = list()
pvPMatches = list()
tvTMatches = list()
mapDict = {}
zvTZergWins = 0
zvPZergWins = 0
zvTTerranWins = 0
tvPTerranWins = 0
zvPProtossWins = 0
tvPProtossWins = 0
drawGames = 0
zvTlongestReplay = None
zvTshortestReplay = None
zvTtotalTime = None
zvPlongestReplay = None
zvPshortestReplay = None
zvPtotalTime = None
tvPlongestReplay = None
tvPshortestReplay = None
tvPtotalTime = None
tvTlongestReplay = None
tvTshortestReplay = None
tvTtotalTime = None
pvPlongestReplay = None
pvPshortestReplay = None
pvPtotalTime = None
zvZlongestReplay = None
zvZshortestReplay = None
zvZtotalTime = None
longestReplay = None
shortestReplay = None
totalTime = None

#################################################################### Start 
folder = setPath()
fileList = gatherReplayFilePaths(folder)

# Main loop
if len(fileList) > 0:
    for file in fileList:
        replay = loadReplay(file, loadLevel)
        if len(replay.players) == 2:
            replayCount = incrementReplayCount(replayCount)
            longestReplay = findLongestReplay(longestReplay, replay)
            shortestReplay = findShortestReplay(shortestReplay, replay)
            totalTime = sumTotalTime(totalTime, replay)
            currentMatchup = findMatchUp(replay)
            appendMatchupSpecificList(replay, currentMatchup)
            zvTZergWins, zvPZergWins, zvTTerranWins, tvPTerranWins, zvPProtossWins, tvPProtossWins, drawGames = incrementMatchUpWins(replay, currentMatchup, zvTZergWins, zvPZergWins, zvTTerranWins, tvPTerranWins, zvPProtossWins, tvPProtossWins, drawGames)
            matchups[currentMatchup] += 1
            
            # adds replay to a list in the mapDic
            if replay.map_name in mapDict:
                mapDict[replay.map_name].append(replay)
            else:
                tempList = list()
                mapDict[replay.map_name] = tempList
                mapDict[replay.map_name].append(replay)
                       
    # Gathering more ZvT data
    for replay in zvTMatches:
        zvTlongestReplay = findLongestReplay(zvTlongestReplay, replay)
        zvTshortestReplay = findShortestReplay(zvTshortestReplay, replay)
        zvTtotalTime = sumTotalTime(zvTtotalTime, replay)
        
    # Gathering more ZvP data
    for replay in zvPMatches:
        zvPlongestReplay = findLongestReplay(zvPlongestReplay, replay)
        zvPshortestReplay = findShortestReplay(zvPshortestReplay, replay)
        zvPtotalTime = sumTotalTime(zvPtotalTime, replay)

    # Gathering more TvP data
    for replay in tvPMatches:
        tvPlongestReplay = findLongestReplay(tvPlongestReplay, replay)
        tvPshortestReplay = findShortestReplay(tvPshortestReplay, replay)
        tvPtotalTime = sumTotalTime(tvPtotalTime, replay)
    
    # Gathering more ZvZ data
    for replay in zvZMatches:
        zvZlongestReplay = findLongestReplay(zvZlongestReplay, replay)
        zvZshortestReplay = findShortestReplay(zvZshortestReplay, replay)
        zvZtotalTime = sumTotalTime(zvZtotalTime, replay)
    
    # Gathering more TvT data
    for replay in tvTMatches:
        tvTlongestReplay = findLongestReplay(tvTlongestReplay, replay)
        tvTshortestReplay = findShortestReplay(tvTshortestReplay, replay)
        tvTtotalTime = sumTotalTime(tvTtotalTime, replay)
    
    # Gathering more PvP data
    for replay in pvPMatches:
        pvPlongestReplay = findLongestReplay(pvPlongestReplay, replay)
        pvPshortestReplay = findShortestReplay(pvPshortestReplay, replay)
        pvPtotalTime = sumTotalTime(pvPtotalTime, replay)

    # Printing all the stuff
    printZvTStats(zvTMatches, zvTZergWins, zvTTerranWins, zvTshortestReplay, zvTlongestReplay, zvTtotalTime)
    printZvPStats(zvPMatches, zvPZergWins, zvPProtossWins, zvPshortestReplay, zvPlongestReplay, zvPtotalTime)
    printTvPStats(tvPMatches, tvPTerranWins, tvPProtossWins, tvPshortestReplay, tvPlongestReplay, tvPtotalTime)
    printZvZStats(zvZMatches, zvZshortestReplay, zvZlongestReplay, zvZtotalTime)
    printTvTStats(tvTMatches, tvTshortestReplay, tvTlongestReplay, tvTtotalTime)
    printPvPStats(pvPMatches, pvPshortestReplay, pvPlongestReplay, pvPtotalTime)
    printMapData(mapDict)
    printGlobalReplayStats(replayCount, shortestReplay, longestReplay, totalTime)
else:
    print('No replays in directory')

print('\nGOODBYE')

# TODO: Add a lot more insightful analysis (matchup win rates(done), player stats, workers built, map data(sort of done), etc...)
# TODO: Add some sort of graphical output to better visualize results (maybe export into Google Sheets or something)
# TODO: Make program usable by people other than myself and take feedback
# TODO: Add in a team replay to my replay folder and see if ruins everything
# TODO: Clean up code in general
# TODO: Add try/exceptions 
# TODO: Add unit tests
# TODO: Cleanup print statements, probably write results to a file in the future instead. these prints are a mess
# TODO: Make time printouts look neater
