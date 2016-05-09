# MasteryMakeMaps #
Riot API Challenge 2016 (spring)

 * This is my submission to the [RIOT API challenge 2016](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1), following the [API terms and condition ](https://developer.riotgames.com/terms#statement)
 * The website [Mastery Makes Maps](https://championsmaps.herokuapp.com/) presents this entry's results.
 * The present documentation contains the detailed ideas and processes.
 * This entry was written in python.

Those programs were written to run as a python backend of the website, but the backend-to-frontend was not implemented. The backend processes were thus run locally and the results presented in the websites are static.


Introduction
============

This is my submission to the [RIOT API challenge of April 2016](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1).

This entry uses the champion mastery points to create a graph (or map) of the champions : the closeness of the champions reflects their similarity.

Similarity of the champions are derived from their respective mastery scores for one given player: similar high scores mean they are close. Data of many players are then aggregated to create a large map.

This graph can be analyzed using graph and community-detection tools. The last one in particular shows the appearance of five groups, which are, as expected, the five in-game positions played. Further analysis would show which champions act as "bridges" between those groups.

Another use of the graph is to look at the neighbors of one champion, thus answering the question : which champions are the most similar to one chosen champion (based on player's willingness and ability to play those)? or, in other words : What would be easy to learn next after mastering champion X, Y or Z?

The following document is organised in four parts : First a short "How To" guide on how to run the programs and what each does. Second the ideas behind this work are presented. Then the details of the implementations are explained. And in the fourth part, I present some small research done and ideas for further development. The results are presented on the website: [Mastery Makes Maps](https://championsmaps.herokuapp.com/)


How To
======

Everything was coded in [Python](https://www.python.org/), using Python 2.7.

I recommend using `pip` to install packages that are not already included within your python. 

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
 * run __'python sampleData.py \<option1\> \<option2\>'__ 
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
 * run __'python createGraph.py \<graphname\>'__ (graphname msut be without extention)

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
 * run __'python getGroups.py \<graphname\>'__ (graphname must be without extention)


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
 * save the groups graph as "\<graphname\>\_gr\<group_number\>.txt" so the drawGraphs function can be called for each group separately
 
_User steps_ :
 * the file "\<graphname\>.txt" must exist
 * run __'python drawGraphs.py \<graphname\> \<all,groups\> \<img,dot\> \<pos:True,False\>'__
  * \<graphname\> must be without extention.
  * \<all,groups\> : if all, then draw the whole graph. if groups, draw the graph for each group.
  * \<img,dot\> : if img, uses images for the nodes. if dot, uses color dots.
  * \<pos:True/False\> : use False the first time it is run, use True if you want to use former positions.

__Important Note__ : The layout of the graphs change with each call of the function. This is because the layout algorithm starts with random positions. For this reason positions are saved and using setting \<pos:True/False\> to True will laod those positions. Care that is one uses False, the old positions will be lost when the new one will be saved.

How to make the website:
------------------------

_User steps_ :
 * go to heroku cloud application platform
 * register and follow the instructions
 * tweek around to get more pages running

_Comment_ : I chose to host on Heroku for two reasons : they could handle python programming (though I have not yet reached this stage of my project) and their beginner guide is very well made. Associated with django basic tutorial, it was possible for me to get by.


Ideas
=====

In this part I expose my thought process for the creation of this project.

Champion Mastery leads to Champion Pool
---------------------------------------

Champion mastery points are gained through playing the champion. Moreover, good plays are rewarded with more points. Thus a champion with a high mastery score was either played a lot or played very well, or both (the two being usually related : the more you play one champion, the better you play it). In other words, the mastery points of a champion represents the player's willingness and ability to play the champion.

Hence, I consider the champion with the highest score the player's _main_, and the group of champions with high score the player's _champion pool_. In practice we consider champions with a mastery grade of 4 or higher to be part of the champion pool.

Let us also remark that those champion mastery data are more reliable than sampling the champion pool from ranked games. Indeed it also takes into account normal (as opposed to ranked) games and it attributes points based on the performance of the player rather than on quantity alone.


Champion pools lead to similarity of champions
----------------------------------------------

From the perspective of the players, some champions are more intuitive to play while others are more challenging. I expect that the champion pools reflect those tendencies: they show which champions are similar from the point of view of the players.

Considering one given player, two champions with similar number of mastery points present the same interest to the player. I thus define the "closeness" of the two champions (for that player) as the relative mastery value : the mastery values of the "weaker" champion divided by the points of the "stronger" champion. Such values are only considered for the champions forming the champion pool.

Graph of Champions
------------------

A graph is composed of nodes and of egdes linking those nodes. In this study the champions are the nodes of the graph, and the edges exist when the two champions belong to the same champion pools. The "closeness" of two champions as defined above is used to weight the link.

Such a graph for one player would show every champions in the champion pool linked together with varying "closeness". The interest for one player is thus limited. However if many players are considered a larger graph is created which shows the different champion pools of the players and how those link or add together. To do that I simply "sum" the graphs of individual players.

Summing the graphs, and in particular the weight of the edges might introduce a bias. Indeed, if many players tend to play top lane for example, links with top laners will be much stronger. Our aim is to explore the similarity of the champions from the player point-of-view, rather than the __sampled__ players' preferences for one in-game position. To avoid this potential bias, the edges' values should be the "mean". _[not implemented for the presented results, refer to "Test Mean Weight" in "Discussion" to learn more on this subject]_


Neighbors and recommendations
-----------------------------

Now that the graph is built, one can eploit it. In particular one can now answer the question "What would be easy to learn next after mastering champion C?"

Indeed the graph presents the "similarity" of champions from the player's point-of-view. The closest neighbors of one champion are the champions most often found in the same champion pool. _That_ would be the answer to the above questions.

This could be developped further with considering a player's own champion pool: using the map, one extracts the champions which are the closest to the current pool. Those extracted champions could then be suggested to the player as way to expand her/his champion pool. _[this has not yet been implemented]_

Another idea is to use the shortest path between two champions C1 and C2 which are not close neighbors. This path would thus define a soft learning strategy to earn champion C2 from champion C1. _[This has yet to be implemented and tested. It is possible that this idea of shortest path is not applicable]_


Community detection
-------------------

Community detection is a widely used tool for the study of graphs, in particular graphs of networks such as facebook friends. Such tools can also be applied to the Champion Graph. Groups of champions are automatically detected based on the similarity.

We expect to see five groups appear for the five in-game positions. Indeed a player tend to specialize in one or two (or three) positions and this can be seen through her/his champion pool. Such specialization is even encouraged with the new dynamic queue as one can select the same positions for each and every game.

Let us remark that this method associates one champion to one group in a strong sense (belongs or not, 0 or 1). As a next study step, it would be interesting to develop a "soft" attribution where champions can belong to many groups with a certain proportionality. Such attribution would most lilkely be closer to the true use of the champions.

The detection of community can be run for the whole graph but also for the sub-graphs made with those communities. For example, two sub-groups are detected for the support group. They are roughly composed of the  tanky / defensive supports on the one hand and  mage / aggressive supports on the other hand.

Bridges between groups
----------------------

As groups are defined through community detection, an interesting question would be : wich champions stand at the border between two groups? which links between those groups are stronger and could such be considered as bridges?

Such information would again allow a player who wants to diversify her/his champion pool or to learn a new position, to know the path of less resistance for her/his endeavor. _[This has yet to be implemented]_


Implementations
===============


All codes are (somehow) commented. This allows us to focus here on the general ideas behind the code.


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
 
The first two points are used to create the file name so I avoid considering twice the same player (if a player is sampled a second time, the former information is replaced by the more recent one). Those data are not made available here but were used to create the champion graph (main result of this work). They can be gathered using the program `sampleData.py` in the "program" folder. Such programs would ideally be run as the backend of the website to keep up-to-date graphs. In the current setting, the "backend" was run locally and the  [website](https://championsmaps.herokuapp.com/) presents the results.


Sample and Filter Masteries
---------------------------

The sampling is performed through sending a request to the [API](https://developer.riotgames.com/api/methods#!/1071/3696) where for one player's id, her/his champion mastery data is returned.

In order to consider the change in the meta, or the evolution of a player, only champions played less than a month ago are kept. This filtering uses the information "lastPlayTime" for the champion.

Furthermore, only the champions with mastery level of 4 or higher are taken into account. This is done to avoid forming strong links between less-played champions. This step is discussed and reconsidered in "Discussion and additional ideas".

Because of those filters some champions may not appear, most likely those not favored by the current meta (April-May 2016).

Those filters are implemented directly after the sampling stage. Those two steps are coded in the `getMastery` function in `sampleData.py`.


Create Graphs
-------------

The python package `networkx` is used for the graph creation and manipulation

The graph is created through iteration for each player data. For each player :
 * all champions are added as nodes
 * links between primary and primary champions are added
 * links between primary and secondary champions are added

The terminology used here is as follow :
 * main champion : the champion with the highest score
 * primary champions : the champions with a score larger than half the main champion score
 * secondary champions : champions with a score smaller than half the main champion score
 * champion pool : all champions (as filtered previously)

For greater clarity, let's consider a fictive player who mastered the following champions (the mastery points are attributed randomly and not indicative of true Mastery Scores) :
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

The python package `community` was created for this purpose of community detection in graphs. The main work once this package is used is to reorganise the information into easy-to-use format.

First a list is created. Its order corresponds to the order of the graph's nodes and it contains the value of the group to which the corresponding node belongs to :
 * nodes_list  =  [n1, n2, n3, n4, n5, ...]
 * values_list =  [ 0,  1,  0,  0,  2, ...]

where the nodes n1, n3 and n4 belongs to the group 0; the node n2 belongs to the group 1; and the node n5 to the group 2. This list is used to color the nodes according to their beloging to one group when the maps are drawn.

Second a dictionary is created where each group is associated to its list of nodes :
`groups_dit = { 0 : [n1, n3, n4, ...]  ;
               1 : [n2, ...] ; 
               2 : [n5, ...] ; 
               ... }`

This allows one to consider only one group for further analysis or visualization.

Visualization
-------------

The `spring` layout of the `networkx` python package is used. This layout is automatically generated starting with random positions. Due to that, a same graph can lead to different layouts but still has the same intrasec properties. The node-positions used to draw the graph are saved each time the `drawGraph` function is called so one can redraw the exact same graph if necessary.

A direct consequence is that one should be carefull when drawing conclusions from the visual of the graph. For example, an isolated Rengar can means that :
 * maybe Rengar is rarely played (meta influence) and has thus week links to every other champions,
 * maybe he is a strong main with weak links to other champions : Rengar-mains only play Rengar, 
 * maybe it is an artifact of the layout.


Creating the website
--------------------

The aim was to create an interactive website with a python backend. To do so, I planned to use `django`.

However, at the current stage of the project, a static website is sufficient to present the results.

I followed the [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) guide to set up the website, and added some pages. I recommand following the first four Django tutorial to know how to modify the main files so additional pages are properly considered.

I used python to generate some of my website content, in particular the list of champions belonging to each groups (which is actually a list of images).


Discussion and additional ideas
===============================

_What is dicussed here may have used programs that are not included in this git repository. Those steps are more research oriented and shared here in this sense._

Less is More
------------

Less sampled players makes for a more visualy pleasing graph. I stumbled on that information while testing my (cleaned) codes on a small set of data (1205 sampled players).

_add image_

This may be explained by the fact that there are generally less links. Thus champions that are rarelly in the same champion pools appear as not linked at all.

Following this discovery I tried to lessen the number of links with restricting the champion pool to Mastery grades of 5 instead of 4 and 5. The strength of the links are still considered in a similar way.

_add images_

The maps with less link appear very similar to the one previously built. It is thus uncertain that considering less links leads to a more pleasing visualization of the graph. Let us note that the general caracteristic (like the five groups) are consistent between those two maps. In conclusion, when sampling many players, the exact size of the champion pool does not seem to matter (though "main", "primary" ad "secodnary" champions are still considered in both cases).

Test "mean" Weight
------------------

As explained in "Ideas - Graph of Champions" (see above), simply summing the graphs when considering multiple players might introduce a bias due to some in-game position(s) being favored by a largepopulation of the sampled players. To avoid such bias I use a mean weight : weight = sum(weight) / Nplayers . where Nplayers is the number of players who contributes to the link. This mean that if the couple of champions are not part of the player champion pool, this playyer does not contribute to the edge at all and is not accounted for in Nplayers. Let us remark than using the total number of sampled players to calculate the mean would simply resquale the sum.

This should allow for the value of the weight to have more sense. But because we consider only strong links already, applying a mean operation puts every link "strength" to a similar value. This can be seen through the following histogram.

__include histograms here__

The map and groups derived from this graph brings little insight as every champions have the same "closeness".

To truly use the "mean" weight, one would need to consider every links in the wider champion pool. My next step in such a study would be to not remove the filter based on champion mastery levels thus extending strongly the group of _secondary_ champions. Weak links would thus be considered, and the "mean" would make more sensee (but as remarked above a "mean"  for all sampled players is simply a "sum" resqualed)

Modify the weight
-----------------

An idea is to consider squared weight. This should accentuate the similarity and dissimmilarity values of the champions nd may lead to a clearer map.


CONCLUSION
==========

I have shown here how to sample the Champion Mastery Data to create graphs of the champions. Those graphs are based on the "similarity" of the champions from the player point-of-view. It can be analysed to find champions closest neighbors (champions that are the most similar) in order to facilitate the widdening of a player's champion pool.

Groups of similar champions are also found in this graph. The groups represent the in-game positions. They can also be analysed : either on how they linked together (bridges between groups) or how they can be divided into more detailed subgroups. 
