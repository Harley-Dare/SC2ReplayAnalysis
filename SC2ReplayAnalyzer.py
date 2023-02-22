import os
import sc2reader
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

print('WELCOME TO HARLEY\'S SC2 REPLAY ANALYZER / FIRST PYTHON PROGRAM\n')
fileList = []
replayCount = 0
longestReplayLength = None
shortestReplayLength = None
totalTime = None
zergCount = 0
protossCount = 0
terranCount = 0
playersSet = set(())

# Create a root Tkinter window (it won't actually appear on the screen)
root = tk.Tk()

# Hide the root window since we don't need to show it
root.withdraw()

# Use the file dialog to ask the user to select a folder containing replay files
folder = filedialog.askdirectory()

# Walk through folder and subfolders, getting list of files.
# TODO: Make sure to only grab .SC2Replay files
for folderName, subfolders, filenames in os.walk(folder):
    for filename in filenames:
        file = folderName + '/' + filename
        fileList.append(file)

for file in fileList:
    replayCount += 1
    # Loading Replay
    replay = sc2reader.load_replay(file, load_level=2)

    # Sets initial longestReplayLength to compare to the rest of the replays
    if longestReplayLength == None:
        longestReplayLength = replay.game_length

    # Sets initial longestReplayLength to compare to the rest of the replays
    if shortestReplayLength == None:
        shortestReplayLength = replay.game_length
    # Sums the total length of all replays analyzed
    if totalTime == None:
        totalTime = replay.game_length
    else:
        totalTime += replay.game_length

    # Compares current replay to longest replay so far
    if replay.game_length > longestReplayLength:
        longestReplayLength = replay.game_length
        longestReplay = replay

    # Compares current replay to shortest replay so far
    if replay.game_length < shortestReplayLength:
        shortestReplayLength = replay.game_length
        shortestReplay = replay

    # Counts chosen races, creates set of participants
    for player in replay.players:
        playersSet.add(player.name)
        if player.pick_race == "Zerg":
            zergCount += 1
        elif player.pick_race == "Protoss":
            protossCount += 1
        elif player.pick_race == "Terran":
            terranCount += 1

print(str(replayCount) + ' total replays found and analyzed')
print(str(Path(longestReplay.filename).name) + ' was the longest replay with a length of ' + str(longestReplayLength))
print(
    str(Path(shortestReplay.filename).name) + ' was the shortest replay with a length of ' + str(shortestReplayLength))

print('Total length of all replays: ' + str(totalTime))
averageTime = totalTime / replayCount
print('Average length of replay: ' + str(averageTime))
print("Zerg games: " + str(zergCount))
print("Protoss games: " + str(protossCount))
print("Terran games: " + str(terranCount))
print("players: \t" + str(playersSet))
print(str(len(playersSet)))

print('\nGOODBYE')