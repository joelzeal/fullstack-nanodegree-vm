#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from players")
    result = c.fetchone()
    conn.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into players(player_name) values(%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * from playerstandings")
    result = c.fetchall()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    # create a new matches record with the winner and loser values
    c.execute("INSERT INTO matches(winner_id, loser_id, is_match_played) VALUES(%s, %s, 'true' )", (winner, loser, ))   # noqa

    # update winner's points in the players table.
    # Assuming each win is worth 1 Point
    c.execute("UPDATE players set points = points + 1 where player_id = %s", (winner,))  # noqa
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()

    # Get all available distinct points to be used to group various players
    c.execute("SELECT DISTINCT points from players")

    tempListOfPairs = []
    for point in c.fetchall():

        # Get all players having the same points
        c.execute("SELECT player_id, player_name FROM players where points = %s", (point[0],))  # noqa

        # Get values from and pass them to the pairing function be paired
        sameRankPlayers = c.fetchall()

        # get player pairs and append result to the main list
        tempListOfPairs.extend(generatePairings(sameRankPlayers))

    # cast the tempListOfPairs to a tuple
    return tuple(tempListOfPairs)

    # close connection
    conn.close()


def generatePairings(playerlist=[]):
    """Generates pairs given list

    Returns:
       A list of tuples containing player pairs

    Args:
       A list of players with the same points
    """

    PlayerPairs = []

    # using the // is to ensure floor devision
    for i in range(0, len(playerlist)//2):
        # pair players and return the pairs
        PlayerPairs.append((playerlist[i*2][0], playerlist[i*2][1], playerlist[(i*2)+1][0], playerlist[(i*2)+1][1]))  # noqa
    return PlayerPairs
