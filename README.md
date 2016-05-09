# MasteryMakeMaps #
Riot API Challenge 2016 (spring)

 * This is my submission to the [RIOT API challenge 2016](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1), following the [API terms and condition ](https://developer.riotgames.com/terms#statement)
 * The website [Mastery Makes Maps](https://championsmaps.herokuapp.com/) presents this entry's results.
 * The present documentation contains the detailed ideas and processes.
 * This entry was written in python.
 * The folder *sampleData* contains the programs used to sample the Champion Mastery Data.
 * The folder *analyseData* contains the programs used to analyse the data and create the graphs.

Those programs were written to run as a python backend of the website, but the backend-to-frontend was not implemented. The backend processes were thus run locally and the results presented in the websites are static.


Introduction
============

This is my submission to the [RIOT API challenge 2016](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1).

This entry uses the champion mastery points to create a graph (or map) of the champions : the closeness of the champions reflects their similarity.

Similarity of the champions are derived from their respective mastery scores for one given player: similar high scores mean they are close. Data of many players are then aggregated to create a large map.

This graph can be analyzed using graph and community-detection tools. The last one in particular shows the appearance of five groups, which are, as expected, the five in-game positions played. Further analysis would show which champions act as "bridges" between those groups.

Another use of the graph is to look at the neighbors of one champion, thus answering the question : which champions are the most similar to one chosen champion (based on player's willingness and ability to play those)? or, in other words : What would be easy to learn next after mastering champion X, Y or Z?

The following document is organised in five parts : First a very short "How To" guide on how to run the programs and what each does. Second the ideas behind this work are presented. Then the details of the implementations are explained. In the fourth part, the results are shown and discussed, and last I present ideas for further development.


How To
======

Everything was coded in Python, using Python 2.7.

How to sample data
------------------

Use 'sampleData.py'

_Python packages_ : requests, json, time, sys, datetime

_Program steps_ :
 * sample players id-s
 * sample their Champion Mastery and filter them
 * save the information in the folder "Data" :
  * name : '\<region\>_\<player-id\>.txt'
  * content : dictionary {"samplingTime" : , "masteries" : , "playerRank" :}
  * content : "mastery" is a list of dictionary {"championPoints" : , "championId" :}

_User steps_ :
 * the folder "Data" needs to be created ahead of time.
 * the document "RIOT_API_KEY.txt" needs to be present with your API key inside.
 * run 'python sampleData.py \<option1\> \<option2\>' 
  * '\<option1\>' can be "master" , "challenger", "other" : will sample master league, or challenger league, or will use feature games to access random leagues. Does not run if the option is missing.
  * '\<option2\>' can be "euw", "na", "jp", "br" (lower letter) to access the corresponding servers. Other regions might work but haven't been tested. Does not run if the option is missing.
 * the program will print general information (and error).

How to create the Graph 
-----------------------

Use 'createGraph.py'

_Python packages_ : sys, os, json, networkx, sampleData.py, cStringIO, urllib2, PIL, pickle

_Program steps_ :
 * load each data
 * for each data create the nodes and edges
 * add the champion images for each nodesm use "white_filler.png" if an error occurs
 * save the graph in 'graphname.txt'
 * save number of plaer in 'graphname_Nplayer.txt'

_User steps_ :
 * the folder "Data" must exist
 * the files in "Data" must have the same content as described in "Sample Data"
 * the name of the files in "Data" does not matter
 * a blank image named "white_filler.png" must exist
 * if another folder is used to store the data, change the 'FOLDER' variable
 * run 'python createGraph.py \<graphname\>' (graphname msut be without extention)

Remark : the function 'clearH' removes "weak" edges. The isolated nodes it creates are also removed. This function is not used for our results.

How to get the groups
---------------------

Use 'getGroups.py'

_Python packages_ : sys, networkx, pickle, community

_Program steps_ :
 * load the graph
 * apply the 'best_partition' function from the 'community' package
 * reorganize the result into 'values' : list of the group at which each corresponding node belongs (as listed by the graph)
 * reorganize the results into 'groups' : a dictionary \{ group_number : \[ list_of_nodes \] \}
 * save 'values' and 'groups' in '\<graphname\>_groups.txt'

_User steps_ :
 * the file "\<graphname\>.txt" must exist
 * run 'python getGroups.py \<graphname\>' (graphname must be without extention)


How to draw a graph
-------------------
Use 'drawGraphs.py'

_Python packages_ : sys, networkx, pickle, getGroups.py, copy, matplotlib.pyplot

_Program steps_ :
 * load the graph and additional information
 * calculate positions of nodes, or load older positions 
 * plot edges
 * plot nodes : either colored dots, or champion images
 * save figure and positions

_User steps_ :
 * the file "\<graphname\>.txt" must exist
 * run 'python grawGraphs.py \<graphname\> \<all,group\> \<img,dot\> \<pos:True,False\>'
  * \<graphname\> must be without extention.
  * \<all,groups\> : if all, then draw the whole graph. if groups, draw the graph for each group.
  * \<img,dot\> : if img, uses images for the nodes. if dot, uses color dots.
  * \<pos:True/False\> : use False the first time it is run, use True if you want to use former positions.

_Important Note_ : The layout of the graphs change with each call of the function. This is because the layout algorithm starts with random positions. For this reason positions are saved and using setting \<pos:True/False\> to True will laod those positions. Care that is one uses False, the old positions will be lost when the new one will be saved.

How to make the website:
------------------------

_User steps_ :
 * go to heroku cloud application platform
 * register and follow the instructions
 * tweek around to get more pages running

Comment : I chose to host on Heroku for two reasons : they could handle python programming (though I have not yet reached this stage of my project) and their beginner guide is very well made. Associated with django basic tutorial, it was possible for me to get by.


Ideas
=====

Masteries lead to champion pool
-------------------------------

Champion pools lead to similarity of champions
----------------------------------------------

The strenght of the link is the mastery values of the "weaker" champion relative to the "stronger" champion.

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


All codes are (somehow) commented. This allow us to focus here on the general ideas behind the code.


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

The sampling is performed through sending a request to the [API](https://developer.riotgames.com/api/methods#!/1071/3696) where for one player's id, her/his champion mastery data is returned.

In order to consider the change in the meta, or the evolution of a player, only champions played less than a month ago are kept. This filtering uses the information "lastPlayTime" for the champion.

Furthermore, only the champions with mastery level of 4 or above are taken into account. This is done to avoid forming strong links between less-played champions.

Because of those filters some champions may not appear, most likely those not favored by the current meta (April-May 2016).

Those filters are implemented directly after the sampling stage. Those two steps are coded in the 'getMastery' function in 'sampleData.py'.


Create Graphs
-------------

The python package 'networkx' is used for the graph creation and manipulation

The graph is created through iteration for each player data. For each player :
 * all champions are added as nodes
 * links between primary and primary champions are added
 * links between primary and secondary champions are added

The terminology used here is as follow :
 * main champion : the champion with the highest score
 * primary champions : the champions with a score larger than half the main champoin score
 * secondary champions : champions with a score smaller than half the main champion score
 * champion pool : all champions (as filtered previously)

For greater clarity, let's consider a fictive player who mastered the following champions (the mastery points are not indicative) :
 * Illaoi : 13000
 * Garen : 11000
 * Rek'Sai : 6300
 * Malphite : 6100
 * Sona : 50 

The mastery points clearly show that Sona is not part of this player's champion pool. She would be filtered in the previous step and is thus not considered at all. Illaoi and Garen have both a large amount of mastery points and form the primary champions. Rek'Sai and Malphire have less point but are still consnistantly played by the player. They are part of the secondary champions. In this example, the following links are created :
 * primary-primary : Illaoi - Garen, 11000/13000
 * primary-secondary : Illaoi - Rek'Sai, 6300/13000
 * primary-secondary : Illaoi - Malphite, 6100/13000
 * primary-secondary : Garen - Rek'Sai,  6300/11000
 * primary-secondary : Garen - Malphite,  6100/11000

No "secondary-secondary" links are considered so the link Rek'Sai-Malphite (strength of 6100/6300) is not created.

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
