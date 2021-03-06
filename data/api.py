"""
This file has functions that get data from twitch api.

Functions:
    1) Request helper function.
    2) Get top games by amount of viewers.
    3) Get user logins broadcasting a specified game ID.
"""

import requests

from config import CLIENT_ID, ACCESS_TOKEN

BASE_URL = 'https://api.twitch.tv/helix/'
HEADERS = {
    'Authorization': 'Bearer ' + ACCESS_TOKEN,
    'Client-Id': CLIENT_ID
}

def requestQuery(query):
    """Make a request and return a response."""

    """Contact API."""
    try:
        response = requests.get(BASE_URL + query, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.RequestException:
        return None

def getTopGames():
    """
    Return top games dictionary of format:
    {game_id: game_name}
    """

    notVideoGames = {
        "509658": "Just Chatting",
        "26936": "Music",
        "509660": "Art",
        "518203": "Sports",
        "417752": "Talk Shows & Podcasts",
        "509670": "Science & Technology",
        "66082": "Games + Demos",
        "5899": "Stocks And Bonds",
        "743": "Chess",
        "27284": "Retro",
        "509659": "ASMR",
        "488190": "Poker",
        "498566": "Slots"
    }
    
    """Number of objects to return (100 max)."""
    first = 25

    """Make query."""
    query = f'games/top?first={first}'
    response = requestQuery(query)

    """Parse response."""
    try:
        quote = response.json()
        games = dict()
        for game in quote['data']:
            id = game['id']
            name = game['name']

            """Ensure it's a game and it is streamed by more than 75 streamers."""
            if id in notVideoGames or name in notVideoGames.values():
                continue

            """Ensure the game is streamed by more than 75 streamers."""
            if len(getStreams(id)) > 90:
                games[id] = name
        return games
    except (KeyError, TypeError, ValueError):
        return None


def getStreams(gameID):
    """Return a set of user logins broadcasting a specified game ID."""

    """Number of objects to return (100 max)."""
    first = 100

    query = f"streams?game_id={gameID}&first={first}"
    response = requestQuery(query)
    
    """Parse response."""
    try:
        quote = response.json()
        streams = set()
        for stream in quote['data']:
            streams.add(stream['user_login'])
        return streams
    except (KeyError, TypeError, ValueError):
        return None
