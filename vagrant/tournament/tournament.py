#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def deleteMatches():
    """Remove all the match records from the database."""
    DB().execute("delete from matches", None, True)


def deletePlayers():
    """Remove all the player records from the database."""
    DB().execute("delete from players", None, True)


def countPlayers():
    """Returns the number of players currently registered."""
    conn = DB().execute("select count(*) from players")
    cursor = conn["cursor"].fetchone()
    conn["conn"].close()
    return cursor[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # query = "insert into players(player_name) values(%s)", (name,)
    DB().execute("insert into players(player_name) values(%s)", (name,), True)


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
    conn = DB().execute("SELECT * from playerstandings")
    cursor = conn["cursor"].fetchall()
    conn["conn"].close()
    return cursor


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB().execute("INSERT INTO matches(winner_id, loser_id) VALUES(%s, %s)", (winner, loser, ), True)  # noqa


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
    conn = DB().execute("SELECT player_id, player_name from playerstandings order by won desc;")  # noqa
    cursor = conn["cursor"]

    # Get values from and pass them to the pairing function be paired
    sameRankPlayers = cursor.fetchall()

    # cast the tempListOfPairs to a tuple
    return tuple(generatePairings(sameRankPlayers))

    # close connection
    conn["conn"].close()


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


class DB:

    def __init__(self, db_con_str="dbname=tournament"):
        """
        Creates a database connection with the connection string provided
        :param str db_con_str: Contains the database connection string,
        with a default value when no argument is passed to the parameter
        """
        self.conn = psycopg2.connect(db_con_str)

    def cursor(self):
        """
        Returns the current cursor of the database
        """
        return self.conn.cursor()

    def execute(self, sql_query_string, sql_query_param_tuple=None, and_close=False):  # noqa
        """
        Executes SQL queries
        :param str sql_query_string: Contain the query string to be executed
        :param bool and_close: If true, closes the database connection after
        executing and commiting the SQL Query
        :param tuple sql_query_param_tuple: Contains query paramenters
        """
        cursor = self.cursor()
        cursor.execute(sql_query_string, sql_query_param_tuple)
        if and_close:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not and_close else None}

    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()
