"""
This file gets top viewed games of twitch, adds them to database.
Then it finds the game with the least amount of saved frames and
finds streams in that category. After that it tries to download
frames from 5 random streams.
"""


from download import downloadFrames
from api import *
from dbFuncs import *
import random

"""
Make a thread that will stop the while loop on input.
"""
import threading

def inputThread(inputList):
    """Thread that waits for an input."""
    input()
    inputList.append(True)
    print("Interrupting.")

"""Start a thread that updates `inputList` with inputs."""
inputList = []
threading.Thread(target=inputThread, args=(inputList, )).start()
print("Press Enter to stop downloading.")


"""Update data while no input (Enter not pressed)."""
downloadCountGlobal = 0
adCount = 0
while not inputList:
    
    with sessionScope() as session:

        """Update top categories."""
        games = getTopGames()
        updateGames(session, games)
        updateFrameCount(session)

        """Get category with least data."""
        gameID = minDataCategory(session)

        """Update category (download frames 5 times)."""
        
        downloadCount = 0
        downloadAttempts = 0

        """Get streams from category."""
        streams = getStreams(gameID)
        while streams and downloadCount < 5 and downloadAttempts < 10:

            """Get random stream."""
            stream = random.choice(list(streams))
            streams.discard(stream)

            print(f"Stream: {stream}, gameID: {gameID}")

            """Download frames from stream, update database."""
            download = False
            for framePath in downloadFrames(stream, gameID):
                download = True
                """Save frame in database."""
                addFrame(session, framePath, gameID, stream)
            
            downloadCount += download
            downloadAttempts += 1

            downloadCountGlobal += download
            adCount += not download
            

"""Update database."""
with sessionScope() as session:
    updateFrameCount(session)

print("Done.")
print(f"Download frames from {downloadCountGlobal} streams. Got {adCount} ads.")

