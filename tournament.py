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

    # Connect to database
    conn = connect()

    # Set up cursor
    cursor = conn.cursor()

    # Execute query to empty match record table "matches"
    cursor.execute("DELETE FROM matches;")

    # Commit changes
    conn.commit()

    # Close connection
    conn.close


def deletePlayers():
    """Remove all the player records from the database."""

    # Connect to database
    conn = connect()

    # Set up cursor
    cursor = conn.cursor()

    # Execute query to empty registered player table "players"
    cursor.execute("DELETE FROM players;")

    # Commit changes
    conn.commit()

    # Close connection
    conn.close


def countPlayers():
    """Returns the number of players currently registered."""

    # Connect to database
    conn = connect()

    # Set up cursor
    cursor = conn.cursor()

    # Execute query to count number of players in "players" table
    cursor.execute("SELECT COUNT(*) as numOfPlayers FROM players;")

    # Store query results in results list
    results = cursor.fetchall()

    # Extract number of players from the results list
    for result in results:
        numOfPlayers = result[0]

    # Close connection
    conn.close

    # Return number of players for function call
    return numOfPlayers


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # Connect to database
    conn = connect()

    # Set up cursor
    cursor = conn.cursor()

    # Execute query to register a new player in table "players"
    cursor.execute("INSERT INTO players (name) values (%s);", (name,))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close


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

    # Connect to database
    conn = connect()

    # Set up cursor
    cursor = conn.cursor()

    # Execute query to fetch player standings
    cursor.execute("SELECT players.id, players.name, \
                    matches.points/3 as wins, \
                    matches.numofmatches \
                    FROM players join matches \
                    on players.id = matches.id \
                    ORDER BY wins desc;")

    # Store query results in results list
    playerStandings = cursor.fetchall()

    # If player standings comes back empty then populate matches table from
    # ids in players table
    if playerStandings == []:

        # Fetch registered players ids database
        cursor.execute("SELECT id FROM players;")
        playersDatabase = cursor.fetchall()

        # Iterate through the list of IDs to populate matches table for
        # first time
        for IDdata in playersDatabase:

            # Enter each registered player id into matches database and give
            # them zero points
            cursor.execute("INSERT INTO matches (ID, points, numofmatches) \
                            VALUES (%s,'0','0');", (IDdata[0],))

        # Commit changes after for loop is finished
        conn.commit()

        # Execute query to fetch player standings
        cursor.execute("SELECT players.id, players.name, \
                        matches.points/3 as wins, \
                        matches.numofmatches \
                        FROM players join matches \
                        on players.id = matches.id \
                        ORDER BY wins desc;")

        # Fetch the query result
        playerStandings = cursor.fetchall()

    # Close connection
    conn.close

    # Return the playerStandings list
    return playerStandings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Connect to database
    conn = connect()

    # Set up cursor
    cursor = conn.cursor()

    # Execute query to  update matches table with winner ID and points
    cursor.execute("UPDATE matches \
                    SET points = points + 3,\
                    numofmatches = numofmatches + 1 \
                    WHERE id = %s;", (winner,))
    # Execute query to update matches table with loser ID and points
    cursor.execute("UPDATE matches \
                    SET numofmatches = numofmatches + 1 \
                    WHERE id = %s;", (loser,))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close


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

    # Connect to database
    conn = connect()

    # Set up cursor
    cursor = conn.cursor()

    # Retrieve playerStandings table
    playerStandingsTable = playerStandings()

    # Set up variables to unpack returned table list
    tupletemp = ()
    temp = []
    swissPairs = []

    # Unpack the playerStandings table into a one dimensional list
    for row in playerStandingsTable:
        temp.append(row[0])
        temp.append(row[1])

    # Loop through the 1D list and pack the pairs in tuples inside a list
    for idx in xrange(0, len(temp), 4):
        for off in range(4):
            tupletemp = tupletemp + (temp[idx+off],)
        swissPairs.append(tupletemp)
        tupletemp = ()

    # Return the swissPairs list
    return swissPairs
