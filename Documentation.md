# MasteryMakeMaps : Documentation#
[RIOT API challenge 2016 (spring)](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1)

_by Lyunee_


Introduction
============

This is my submission to the [RIOT API challenge of April 2016](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1).

This entry uses the champion mastery points to create a graph (which is visuaalized as a map) of the champions : the closeness of the champions reflects their similarity.

Similarity of the champions are derived from their respective mastery scores for one given player: similar high scores mean they are close. Data of many players are then aggregated to create a large graph.

This graph can be analyzed using graph and community-detection tools. The last one in particular shows the appearance of five groups, which are, as expected, the five in-game positions played. Further analysis would show which champions act as "bridges" between those groups.

Another use of the graph is to look at the neighbors of one champion, thus answering the question : which champions are the most similar to one chosen champion (based on player's willingness and ability to play those)? or, in other words : What would be easy to learn next after mastering champion X, Y or Z?

The following document is organised in three parts : First the ideas behind this work are presented. Then the details of the implementations are explained. And in the last part, I present some small research and ideas for further development.
The results are presented on the website: [Mastery Makes Maps](https://championsmaps.herokuapp.com/)


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

Now that the graph is built, one can exploit it. In particular one can now answer the question "What would be easy to learn next after mastering champion C?"

Indeed the graph presents the "similarity" of champions from the player's point-of-view. The closest neighbors of one champion are the champions most often found in the same champion pool. _That_ would be the answer to the above questions.

This could be developped further with considering a player's own champion pool: using the map, one extracts the champions which are the closest to the current pool. Those extracted champions could then be suggested to the player as way to expand her/his champion pool. _[this has not yet been implemented]_

Another idea is to use the shortest path between two champions C1 and C2 which are not close neighbors. This path would thus define a soft learning strategy to earn champion C2 from champion C1. _[This has yet to be implemented and tested. It is possible that this idea of shortest path is not applicable]_


Community detection
-------------------

Community detection is a widely used tool for the study of graphs, in particular graphs of networks such as facebook friends. Such tools can also be applied to the Champion Graph. Groups of champions are automatically detected based on the similarity.

We expect to see five groups appear for the five in-game positions. Indeed a player tend to specialize in one or two (or three) positions and this can be seen through her/his champion pool. Such specialization is even encouraged with the new dynamic queue as one can select the same positions for each and every game.

Let us remark that this method associates one champion to one group in a strong sense (belongs or not, 0 or 1). As a next study step, it would be interesting to develop a "soft" attribution where champions can belong to many groups with a certain proportionality. Such attribution would most lilkely be closer to the true use of the champions.

The detection of community can be run for the whole graph but also for the sub-graphs made with those communities. For example, three sub-groups are detected for the support group. They are roughly composed of the  tanky supports, the mage-healer supports and the damage dealer / aggressive supports.

Bridges between groups
----------------------

As groups are defined through community detection, an interesting question would be : wich champions stand at the border between two groups? which links between those groups are stronger and could such be considered as bridges?

Such information would again allow a player who wants to diversify her/his champion pool or to learn a new position, to know the path of less resistance for her/his endeavor.

Looking at the bridges found in this study, it appears that each group has one or two champions which are important bridging champoins :
 * SUP : Thresh
 * TOP : more variety but with Fiora and Gangplank more present
 * MID : Yasuo
 * ADC : Lucian and Vayne
 * JNG : Lee Sin

This can be partly explained by the fact that Thresh and Lee Sin for example are "play-making" champions and thus are interesting to master. Another explanation could be that the champions that form the bridges are actually the champions favored by the current meta so "everyone" learns them. It is likely a mix of those elements as well as the true sense of the bridges : those champions stand between the groups.


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

I followed the [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) guide to set up the website, and added some pages. I recommend following the first four Django tutorial to know how to modify the main files so additional pages are properly considered.

I used python to generate some of my website content, in particular the list of champions belonging to each groups (which is actually a list of images).


Discussion and additional ideas
===============================

_What is dicussed here may have used programs that are not included in this git repository. Those steps are more research oriented and shared here in this sense._

Less is More
------------

Less sampled players makes for a more visualy pleasing graph. I stumbled on that information while testing my (cleaned) codes on a small set of data (1205 sampled players).

![Map when 1205 players are sampled](https://github.com/Lyunee/MasteryMakeMaps/raw/master/images/1205_imgs.png "Map when 1205 players are sampled")

This may be explained by the fact that there are generally less links. Thus champions that are rarelly in the same champion pools appear as not linked at all.

Following this discovery I tried to lessen the number of links with restricting the champion pool to Mastery grades of 5 instead of 4 and 5. The strength of the links are still considered in a similar way.

![Map when only grade 5 champions are considered](https://github.com/Lyunee/MasteryMakeMaps/raw/master/images/lesslinks_imgs.png "Map when 1205 players are sampled")


This map with less link is very similar to the one originally built. Thus, considering less links does not lead to a more pleasing visualization of the graph. Let us note that the general caracteristic (like the five groups) are consistent between those two maps. In conclusion, when sampling many players, the exact size of the champion pool does not seem to matter (though "main", "primary" ad "secondary" champions are still considered in both cases).

Test "mean" Weight
------------------

As explained in "Ideas - Graph of Champions" (see above), simply summing the graphs when considering multiple players might introduce a bias due to some in-game position(s) being favored by a largepopulation of the sampled players. To avoid such bias I use a mean weight : weight = sum(weight) / Nplayers . where Nplayers is the number of players who contributes to the link. This mean that if the couple of champions are not part of the player champion pool, this playyer does not contribute to the edge at all and is not accounted for in Nplayers. Let us remark than using the total number of sampled players to calculate the mean would simply resquale the sum.

This should allow for the value of the weight to have more sense. But because we consider only strong links already, applying a mean operation puts every link "strength" to a similar value. This can be seen through the following histogram.

![Histogram of the "mean" weight](https://github.com/Lyunee/MasteryMakeMaps/raw/master/images/Hist_mean_weight.png)
![Histogram of the "sum" weight](https://github.com/Lyunee/MasteryMakeMaps/raw/master/images/Hist_sum_weight.png)


The map and groups derived from this graph brings little insight as every champions have the same "closeness".

To truly use the "mean" weight, one would need to consider every links in the wider champion pool. My next step in such a study would be to not remove the filter based on champion mastery levels thus extending strongly the group of _secondary_ champions. Weak links would thus be considered, and the "mean" would make more sensee (but as remarked above a "mean"  for all sampled players is simply a "sum" resqualed)

Modify the weight
-----------------

An idea is to consider squared weight. This should accentuate the similarity and dissimmilarity values of the champions and may lead to a clearer map.


CONCLUSION
==========

I have shown here how to sample the Champion Mastery Data to create graphs of the champions. Those graphs are based on the "similarity" of the champions from the players' point-of-view. It can be analyzed to extract groups of similar champions, or to suggest ways to expand a player's champion pool. The last is achieved using the closest neighbors mastered champoins.

The groups of similar champions represent the in-game positions. They can also be analysed : either on how they linked together (bridges between groups) or how they can be divided into more detailed subgroups. 
