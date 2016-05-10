# MasteryMakeMaps : How To#
Riot API Challenge 2016 (spring)

_by Lyunee_


This document explains how to use the programs in the "code" folder, and how to reproduce the analysis I have done for this challenge entry.


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

How to get website content:
---------------------------
Use 'textWeb.py'

_Python packages_ : getGroups.py, drawGraphs.py, sys, sampleData.py

_Program steps_ :
 * load the group information
 * load image links 
 * create and fill a .txt file with html content (mostly images)

_User steps_ :
 * the files "\<graphname\>.txt" and "\<graphname\>\_groups.txt" must exist
 * run __'python textWeb.py \<graphname\> \<option\>'__
 * \<graphname\> must be without extention.
 * \<option\> are as follow:
  * listGroups : to get the format for the main groups.
  * listSubGroups : to get the format for the sub-groups. <\graphname\> should be a group graph.
  * allSubGroups : to get all subGroups treated in the sub-group format. <\graphname\>_gr\<numberGroup\> should all exist.
  * listNeighbors : to get the closest neighbors for all node
  * bridges : to get the bridges between each group

The last two functions load the graph to find the naighbors and bridges respectively. The function `findBridges(G,group1,group2,N)` returns the N (or less if less) bridges between group1 and group2 (which are lists of nodes).


How to Do Everything
--------------------

 1.  check that all the packages are installed
 2.  create a folder for your study and import all programs
 3.  create the folder "Data"
 4.  create  the "RIOT_API_KEY.txt" file with your API key in it
 5.  open a terminal window and go to your study folder
 6.  run `python sampleData.py  <rank> <server>` for the ranks and servers you are interested in. This samples the data.
 7.  run `python createGraph.py <graphname>`. This creates and saves the graph from the data.
 8.  run `python getGroups.py <graphname>`. This identifies and saves the group in the Graph.
 9.  run `python drawGraphs.py <graphname> all img False`. This creates and saves a layout for the graph, then draws and saves the map with the champions images. 
 10. run `python drawGraphs.py <graphname> all dot True`. This uses the formely created position to draw and save the same map but with dots colored differently for each group.
 11. run `python drawGraphs.py <graphname> groups img False`. This draws and saves the map for each group, using the champions images. It also saves the graph of each group independantly.
 12. run `python getGroups.py <graphname>_<group_number>`. This analyses the group \<group_number\> , identifying and saving the subgroups.
 13. run `python drawGraphs.py <graphname>_<group_number> all dot True`. This draws the group map with dots color-coded to the subgroup found in the previous step.
 14. run `python drawGraphs.py <graphname>_<group_number> groups img False`. This draws and saves the map for each sub-group of the group \<group_number\>, using the champions images. It also saves the graph of each sub-group independantly.
 15. run `python textWeb.py <graphname> listGroups`. This creates a text files with the website content that presents the main groups.
 16. run `python textWeb.py <graphname> allSubGroups`. This creates text files with website content that describes the sub-groups of each group. The step number 12 must have been run for all groups for this step to work.
 17. run `python textWeb.py <graphname> listNeighbors`. This creates a text file with the website content of the closest neighbors page.
 18. run `python textWeb.py <graphname> bridges`. This creates a text file for the website with the bridges between each groups.
 19. use the pictures and text files generated to fill the website's pages
