-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- drop the tournament database if it alreadty exists
-- DROP DATABASE IF EXISTS tournament;

-- create tournament database
-- CREATE DATABASE tournament;


-- drop tables before creating if there already exit
 DROP VIEW IF EXISTS playerstandings;
 DROP TABLE IF EXISTS matches;
 DROP TABLE IF EXISTS players;

-- create table for players
CREATE TABLE players (
	player_id serial primary key,
	player_name varchar(50) NOT NULL,
	points int DEFAULT 0
);

-- create table for matches
CREATE TABLE matches(
	match_id bigserial primary key,
	winner_id integer references Players(player_id),
	loser_id integer references Players(player_id),
	winner_points int ,
	loser_points int ,
	is_match_played boolean DEFAULT 'false',
	round int 
);


-- create a view to aid display of player standings
CREATE VIEW playerstandings
AS SELECT player_id, player_name, 
(select count(*) from matches where winner_id = player_id ) as won, 
(select count(*) from matches where is_match_played = 'true' and winner_id = player_id or loser_id = player_id) as matches
from players



--CREATE TABLE tournament(
--
--);