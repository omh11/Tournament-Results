-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop the tournament database if its already created
DROP DATABASE IF EXISTS tournament;

-- Create the tournament database
CREATE DATABASE tournament;

-- Connect to tournament database
\c tournament

-- Drop the players table if it already exists
DROP TABLE IF EXISTS players;

-- Create the tournament players table with a player ID column containing integer data
-- type and a player name column containing text data type
-- Set the serial id as a primary key
CREATE TABLE players (id serial primary key, name text);

-- Drop the match record table if it already exists
DROP TABLE IF EXISTS matches;

-- Create the tournament matches table with a player ID and Opponent ID columns
-- both containing integer data type. The match table also includes a column
-- with the round number of integer data type and finally two columns
-- "ID points" and "OppIDpoints" including an integer data type to record
-- the round poind for each player.
-- reference the primary key in the players table
CREATE TABLE matches (id serial references players, points int, numofmatches int);
