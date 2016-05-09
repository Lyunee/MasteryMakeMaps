#############################################
## getGroups.py
## by Lyunee
## 
## finds the subgroup of the graph
## and saves them
## for the RIOT API challenge 2016
## 
#############################################



import sys
import networkx as nx
import pickle
import community


def loadH(graphname):
## read the graph 
	H = nx.read_gpickle(graphname + '.txt')
# load the number_of_players : unecessary 
#	with open(graphname+'_Nplayer.txt', "r") as f:
#		number_of_players = pickle.load(f)
#	return H,number_of_players
	return H


def get_best_partition(H):
## uses the comminity package to get subgroups

	parts = community.best_partition(H)  
	values = [parts.get(node) for node in H.nodes()]  
# values : list of the group at which the node belongs
	groups = { i:[] for i in list(set(parts.values()))}
# groups : dictionary with group as keys and list of nodes as elements
	for n in parts.keys():
		groups[parts[n]].append(n)
	return values,groups	


	
	
if __name__ == "__main__":
	
	graphname = sys.argv[1]
	print "\nLoad the graph " + graphname
	H= loadH(graphname)
	print "\nFind the groups"
	values,groups = get_best_partition(H)
	print "\nSaves the groups values in " + graphname +"_groups.txt"
	with open(graphname +"_groups.txt", "w") as f:
		pickle.dump(values, f)
		pickle.dump(groups, f)
	print "\nAll done !"
	
	

