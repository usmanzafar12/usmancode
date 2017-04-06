#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament user=vagrant")
        curr = conn.cursor()
        return conn, curr
    except:
        print"There was an error connectiong"
        exit()


def deleteMatches():
    """Remove all the match records from the database."""
    conn, curr = connect()
    curr.execute('TRUNCATE TABLE match;')
    conn.commit()
    curr.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, curr = connect()
    curr.execute('TRUNCATE TABLE player CASCADE;')
    conn.commit()
    curr.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, curr = connect()
    curr.execute('SELECT  COUNT(*) FROM player;')
    x = curr.fetchall()
    curr.close()
    conn.close()
    return x[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, curr = connect()
    query = 'INSERT INTO player (name) VALUES(%s)'
    param = (name,)
    curr.execute(query, param)
    conn.commit()
    curr.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, curr = connect()
    won = """SELECT player.id, player.name, COUNT(*) AS win
              FROM player
              JOIN match
              ON player.id=match.winner
              GROUP BY player.id
          """
    lost = """SELECT player.id, COUNT(*) AS lost
              FROM player
              JOIN match
              ON player.id=match.loser
              GROUP BY player.id
           """
    query = """SELECT player.id, player.name,
           coalesce(count_won.win, 0) AS win,
           (coalesce(count_won.win, 0)+coalesce(count_lost.lost,0)) AS matches
           FROM player
           LEFT JOIN ({}) AS count_won
           ON player.id=count_won.id
           LEFT JOIN ({}) AS count_lost
           ON player.id=count_lost.id
           ORDER BY win""".format(won, lost)
    curr.execute(query)
    results = curr.fetchall()
    curr.close()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, curr = connect()
    q = "INSERT INTO match (winner, loser, result) VALUES (%s,%s,%s)"
    curr.execute(q, (winner, loser, winner))
    conn.commit()
    curr.close()
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
    conn, curr = connect()
    # Selecting players which have won a match
    won = """SELECT player.id, player.name, COUNT(*) AS win
              FROM player
              JOIN match
              ON player.id=match.winner
              GROUP BY player.id
          """
    # Selecting players which have lost a match
    lost = """SELECT player.id, COUNT(*) AS lost
              FROM player
              JOIN match
              ON player.id=match.loser
              GROUP BY player.id
           """
    # creating a view and a standing of players sorted by number of wins
    query = """CREATE OR REPLACE VIEW standing AS SELECT player.id,
            player.name, row_number() over (ORDER BY
            coalesce(count_won.win, 0)) AS row FROM player
           LEFT JOIN ({}) AS count_won
           ON player.id=count_won.id
           LEFT JOIN ({}) AS count_lost
           ON player.id=count_lost.id
           ORDER BY win""".format(won, lost)
    curr.execute(query)
    # Selecting even rows from the view created above
    even_rows_query = """CREATE OR REPLACE VIEW even_rows AS
                        SELECT even_row.id, even_row.name, even_row.row,
                        row_number() over (ORDER BY even_row.row)
                        FROM standing AS even_row
                        WHERE mod(even_row.row,2)=0
                      """
    curr.execute(even_rows_query)
    # Selecting odd rows from the view created above
    odd_rows_query = """CREATE OR REPLACE VIEW odd_rows AS
                        SELECT odd_row.id, odd_row.name, odd_row.row,
                        row_number() over (ORDER BY odd_row.row)
                        FROM standing AS odd_row
                        WHERE mod(odd_row.row,2)!=0
                     """
    curr.execute(odd_rows_query)
    # Joining the adjacent rows to select the swiss pairing
    new_query = """ SELECT even.id, even.name, odd.id, odd.name
                   FROM even_rows AS even
                   INNER JOIN odd_rows AS odd
                   ON even.row_number=odd.row_number;"""
    curr.execute(new_query)
    result = curr.fetchall()
    curr.close()
    conn.close()
    return result
