"""
This file will have functions to contact with database.

Functions:
Update categories (`games` table)
Choose category with the least amount of data (`game_frames` table)
Add frame to database (`frames` table, `game_frames` table)
"""

from db import Session
from db import Game, Frame, GameFrames

from contextlib import contextmanager

@contextmanager
def sessionScope():
    """Provide a transactional scope around a series of operation."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def updateGames(session, games):
    """
    Updates `games` table.

    `games` is a dictionary of format:
    {game_id: game_name}
    """
    for game in games:
        
        id = game
        name = games[game]

        # Check if it already exists in the database
        if not session.query(Game).filter_by(id=id).all():

            # Insert `game` and `id` if not exist
            game = Game(id=id, name=name)
            session.add(game)
    
    """
    # Print all games
    for game in session.query(Game).all():
        print(game)
    """

def minDataCategory():
    raise NotImplementedError

def addFrame():
    raise NotImplementedError
