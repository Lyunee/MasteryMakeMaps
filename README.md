# MasteryMakeMaps #
Riot API Challenge 2016 (spring)

_by Lyunee_


 * This is my submission to the [RIOT API challenge 2016](https://developer.riotgames.com/discussion/announcements/show/eoq3tZd1), following the [API terms and condition ](https://developer.riotgames.com/terms#statement)
 * The website [Mastery Makes Maps](https://championsmaps.herokuapp.com/) presents this entry's results.
 * The [documentation](https://github.com/Lyunee/MasteryMakeMaps/raw/master/Documentation.md) contains the detailed ideas and processes.
 * The [HowTo document](https://github.com/Lyunee/MasteryMakeMaps/raw/master/HowTo.md) presents the steps to follow in order to reproduce the results.
 * The codes are in the "code" folder
 * The folder "output" contains the files generated through the analysis of the data, as well as the files used for the presentation of the results in the website.
 * The folder "images" contains a few additional images used in the documentation.
 * The programs were written in python, and run using python 2.7.10

_Those programs were written to run as a python backend of the website, but the backend-to-frontend was not implemented. The backend processes were thus run locally and the results presented in the website [Mastery Makes Maps](https://championsmaps.herokuapp.com/) are static._

----------------------------------------------

This entry uses the champion mastery points to create a graph (or map) of the champions. This graph is based on the "similarity" of the champions from the players' point-of-view.

It can be analyzed to extract groups of similar champions. This is achieved using community detection. The groups correspond to in-game positions and are further analysed : is there sub-groups? (yes except for the ADC group), can we find bridges between the groups? (yes) 

The graph can also be exploited to suggest ways to expand a player's champion pool. In particular, using closest neighbors,  we can answer the question "What would be easy to learn next after mastering a given champion?"


