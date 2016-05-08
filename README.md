# MasteryMakeMaps #
Riot API Challenge 2016 (spring)

 * The website [Mastery Makes Maps](https://championsmaps.herokuapp.com/) presents this entry's results.
 * The present documentation contains the detailed ideas and processes.
 * This entry was written in python.
 * The folder *sampleData* contains the programs used to sample the Champion Mastery Data.
 * The folder *analyseData* contains the programs used to analyse the data and create the graphs.

Those programs were written to run as a python backend of the website, but the backend-to-frontend was not implemented. The backend processes were thus run locally and the results presented in the websites are static.


Introduction
============

This is my submission to the [RIOT API challenge 2016](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1).

This entry aims to use the champion mastery points to create a graph (or map) of the champions : the closeness of the champions reflect their similarity.

Similarity of the champons are derived from their respective mastery scores for one given player: similar high scores mean they are close. Data of many players are then aggregated to create a large map.

This graph can be analyzed using graph and community-detection tools. The last one in particular shows the appearance of five groups, which are, as expected, the five in-game positions played. Further analysis would show which champions act as "bridges" between those groups.

Another use of the graph is to look at the neighbors of one champion, thus answering the question : which champions are the most similar to one chosen champion (based on player's willingness and ability to play those)? or, in other words : What would be easy to learn next after mastering champion X, Y or Z?





Ideas
=====

Masteries lead to champion pool
-------------------------------

Champion pools lead to similarity of champions
----------------------------------------------

Similarity of champions = distance between them
------------------------------------------------

Distance = Maps (also known as graph)
-------------------------------------

Community detections
--------------------

Bridges between groups of champions
-----------------------------------

Neighbors and recommendations
-----------------------------


Implementations
===============


All codes are heavily commented. This allow us to focus here on the general ideas behind the code. A last paragraph is dedicated to the python packages and resources used.


Sample players
--------------

Champion mastery data are made accessible for one given player. This means one needs to possess a list of players or player id-s (with the associated server) to gather champion mastery data.
I used the "league/challenger" and "league/master" requests to gather players id. This was run on the four following servers : euw, na, br, jp.
Additionaly, I used featured games to access random players and then the "league/by-summoner/" request to gather additional players from a similar league (and rank).

I collected the champion mastery data of 13 126 players using such method. The information stored were the following : 
 * server (through file name)
 * player id (through file name)
 * sampling date
 * filtered masteries (see next paragraph)
 * player rank (but unused so far)
 
The first two points are used to create the file name so we avoid sampling twice the same player (if a player is sampled a second time, the former information is replaced by the more recent one). Those data are not made available here but were used to create the champion graph (main result of this work). They can be gathered using the programs in the *sampleData* folder. Such programs would ideally be run as the backend of the website to keep up-to-date graphs. In the current setting, the "backend" was run locally and the  [website](https://championsmaps.herokuapp.com/) presents the results.


Sample and Filter Masteries
---------------------------



Create Graphs
-------------

Community detections
--------------------

Visualisation
-------------

Creating the website
--------------------

Results
=======


Further developments
====================
