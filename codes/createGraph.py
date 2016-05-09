#############################################
## createGraph.py
## by Lyunee
## 
## creates the graph from the data in Data folder
## and saves it
## for the RIOT API challenge 2016
## 
#############################################

import sys
import os
import json
import networkx as nx
from sampleData import getRequest
import cStringIO, urllib2
from PIL import Image
import pickle

FOLDER = "Data"

def createGraph():

## initialisation steps
	# read through the files in FOLDER
	players = next(os.walk(FOLDER))[2]
	# create empty graph
	G=nx.Graph()
	# initialise number of player sampled
	number_of_players = 0


	for p in players : 
	# for every player in the folder(s) considered

		full_path = os.path.join(FOLDER, p)
		with open(full_path, 'rb') as infile:
			the_info = json.load(infile)
		champions = the_info["masteries"]
		# this is a list of dict : {"championId": , "championPoints":}
		# those are already filtered

		# if no champion after the filter
		if len(champions)<1:
			continue
		
		# identify main champion
		main_champ = champions[0]

## add the nodes
		for champ in champions:
			G.add_node(champ['championId'])
		
## add the edges
		for i,champ in enumerate(champions):
			# only the primary champions will create a link
			if champ["championPoints"]<main_champ["championPoints"]/2. :
				break
		# second champion :
			for champ2 in champions[i+1:] :
			# we order the ids, to easily find the edges
				id1 = min(champ['championId'],champ2['championId'])
				id2 = max(champ['championId'],champ2['championId'])
				wei = 1. * champ2['championPoints'] / champ['championPoints']
				if (id1,id2) not in G.edges():
					G.add_edge(id1,id2,weight = wei)
				else :
				# if the edge already exist, sum the weights
					G.add_edge(id1,id2,weight = G[id1][id2]["weight"]+wei)

		number_of_players += 1
	return G,number_of_players


def addIm(H):
## add images option to the node
## in order to draw the maps

	## 1. get the image name
	the_request = \
		"https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion?dataById=True&champData=image&"
	r = getRequest(the_request,"static data for chamion images")
	if not r :
		"Terminate program"
		sys.exit()
	the_data = r.json()["data"]

	## 2. add the information to each node
	for node in H.nodes():

		the_url = \
			"http://ddragon.leagueoflegends.com/cdn/6.9.1/img/champion/" + \
			the_data[str(node)]['image']['full']

		try :
			the_file = cStringIO.StringIO(urllib2.urlopen(the_url).read())
			the_img = Image.open(the_file)
		except :
			print "problem with getting file for node : " + str(node) + " _ " + the_data[str(node)]['key']
			print "a white filler is used"
			the_img = Image.open("white_filler.PNG")

		H.add_node(node,image = the_img)	

	return H

def clearH(H,number_of_players):
## removes weak edges
## then remove isolated nodes
## this function is not used

	edge_co = []
	N_edge_removed = 0
	for u,v,d in H.edges(data=True):
		new_wei = d['weight']/number_of_players
		if new_wei < 0.01:
			#edge_co.append(0)
			H.remove_edge(u,v)
			N_edge_removed += 1
		else :
			edge_co.append(new_wei**2)
	print "removed " + str(N_edge_removed) + " edges"
	
	# there is an easier way to do this
	# with remove_isolated_nodes()
	node_removed = []
	for n in H.nodes():
		if len(H.neighbors(n))<2 :
			node_removed.append(n)

	H.remove_nodes_from(node_removed)
	print "removed " + str(len(node_removed)) + " nodes"

	return H,node_removed

if __name__ == "__main__":

	graphname = sys.argv[1]
	print "\nCreating graph"
	G,number_of_players = createGraph()
	print "\t" + str(number_of_players) + " player-data were used to create the graph"
	print "\nAdding Images to Graph"
	G = addIm(G)
	print "\nSaving graph in " + graphname
	nx.write_gpickle(G, graphname+'.txt')
	with open(graphname+'_Nplayer.txt', "w") as f:
			pickle.dump(number_of_players, f)
	print "\nAll done !"