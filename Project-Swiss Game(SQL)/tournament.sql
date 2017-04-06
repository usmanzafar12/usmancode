-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create database tournament;

\c tournament

create table if not exists player (
 id serial PRIMARY KEY NOT NULL,
 name varchar(30)
);

create table if not exists match (
 id serial PRIMARY KEY NOT NULL,
 winner integer references player(id),
 loser integer references player(id),
 result integer references player(id)  
);