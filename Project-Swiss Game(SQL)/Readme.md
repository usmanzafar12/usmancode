# Swiss Pair Tournament

# Features

  - Project implements functions that query that database and return the required information

# How To Use It
- use the command `psql` to connect to the database
- use `\li tournament_sql` to create the database along with the required tables
- use `python tournament_test.py` to run the test functions present in tournament.py against the database.


# Technical Aspects Of The Code
### Data Model
- The data model designed was a 1 to many relationship between a Player entity and a Match entity.
- The Player entity contains the columns: id, matches won, matches lost and name.
- The Match entity contains the columns: id, player1 (foreign key which references player.id), player2(foreign key which references player.id) and result( which again references player.id) 





