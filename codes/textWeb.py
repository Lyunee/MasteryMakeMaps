#############################################
## textWeb.py
## by Lyunee
## 
## writes part of the website content
## and saves them
## for the RIOT API challenge 2016
## 
#############################################


from getGroups import loadH
from drawGraphs import loadGroups
import sys
from sampleData import getRequest


def getImgLinks():
	the_request = "https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion?dataById=True&champData=image&"
	r = getRequest(the_request, "get image links")
	if not r : # if request error, terminate program
		print "Terminate program"
		sys.exit()
	return r.json()["data"]

def listGroups(graphname,the_data,groups):
	with open( graphname+'_listGroups.txt' , 'w' ) as f:
		for k in groups.keys():
			f.write( "<a href=\"/group" + str(k) + "/\">\n" )
			f.write( "<h2 class=\"group" + str(k) + "\"> group " + str(k) + " </h2>\n")
			f.write( "<p>\n" )
			for n in groups[k]:
				f.write( textImg(the_data,n) )
			f.write( "</p>\n</a>\n\n")
	print "\nFile " + graphname+"_listGroups.txt created and filled"


def listSubGroups(graphname,the_data,groups):
	with open( graphname+'_listSubGroups.txt' , 'w' ) as f:
		for k in groups.keys():
			f.write( "<div class=\"sgp" + str(k)+ "\"> \n<p> \n" )
			for n in groups[k]:
				f.write( "\t<img src='" + \
					"http://ddragon.leagueoflegends.com/cdn/6.9.1/img/champion/" +\
					the_data[str(n)]['image']['full']  + "'>\n" )
			f.write( "</p>\n</div>\n\n")
	print "\nFile " + graphname+"_listSubGroups.txt created and filled"

def textImg(the_data,n):
	text =  "\t<img src='" + \
		"http://ddragon.leagueoflegends.com/cdn/6.9.1/img/champion/" +\
		the_data[str(n)]['image']['full']  + "'>\n"
	return text
	
def listClosestNeighbors(graphname,the_data,N):
## list the N closest neighbors of all champions in the graph
## save the list in image form

	f = open(graphname+'_neighbors.txt','w')
	f.write("<table>")
	
	## 1. load graph
	print "\nLoad the graph " + graphname
	H = loadH(graphname)
	## 2. for each node
	for n in H.nodes():
		neighbors = []
		weight = []
		for neigh in H[n].keys() : # dic of neighbors
			neighbors.append(neigh)
			weight.append(H[n][neigh]["weight"])
		# sort the list
		weight, neighbors = zip( *sorted( zip(weight,neighbors), reverse=True ) )
		f.write("\n<tr> <td> " + textImg(the_data,n)  + "  </td> <td>")
		for i in range(min(N,len(neighbors))):
			f.write( textImg(the_data,neighbors[i]) + " &nbsp ")
		f.write("</td> </tr>" )
	f.write("\n</table>")
	f.close()
	print "\nFile " + graphname+"_neighbors.txt created and filled"

	
def findBridges(G,gr1,gr2,N):
## G is the graph, gr1 and gr2 lists of the node of each group
## return the N first bridges between the groups
	
	# 1. collect all edges between the two groups,
	# and their weights
	edges = []
	weights = []
	for n1 in gr1:
		for n2 in gr2:
			# check if they are neighbors
			if n2 in G.neighbors(n1) :
				edges.append((n1,n2))
				weights.append(G[n1][n2]["weight"])
	# 2. sort by descending weights
	weights, edges = zip( *sorted( zip(weights,edges), reverse=True ) )
	# 3. get the bridges 
	bridges = edges[:min(N,len(edges))]
	return bridges
	
def bridges(graphname,the_data,groups,N):
## find the bridges bewteen all the groups
	
	## 1. load graph
	print "\nLoad the graph " + graphname
	G = loadH(graphname)
	
	for i,gp1 in enumerate(groups.keys()) :
		for gp2 in groups.keys()[i+1:] :
		
			print "\t find bridges for groups " + str(gp1) + " and " + str(gp2)
			bridges = findBridges(G,groups[gp1],groups[gp2],N)
			with open(graphname + "_gr" + str(gp1) +\
					"-gr"+str(gp2)+"_bridges.txt","w") as f :
				f.write("<p>The " + str(N) + " main bridges are : </br>\n")
				for (n1,n2) in bridges :
					f.write("\t ( " + textImg(the_data,n1)+" , " +\
						textImg(the_data,n2) + ") &nbsp &nbsp \n")
				f.write("</p>")
	

	
if __name__ == "__main__":
	
	graphname = sys.argv[1]
	

	print "\nLoad the groups "
	values, groups = loadGroups(graphname)
	
	print "\nGet images links from RIOT API"
	champ_data = getImgLinks()
	
	if sys.argv[2] == "listGroups":
## for the main groups
		listGroups(graphname,champ_data,groups)
	elif sys.argv[2] == "subGroups":
## for one sub-group (the graphname must be the group graph name)
		listSubGroups(graphname,champ_data,groups)
	elif sys.argv[2] == "allSubGroups":
## sub-groups for all groups (the groups must have been generated before)
		for k in groups.keys():
			print "\t\t For Group "+str(k)
			print "Load groups"
			sub_values, sub_groups = loadGroups(graphname+"_gr"+str(k))
			listSubGroups(graphname+"_gr"+str(k),champ_data,sub_groups)
	elif sys.argv[2] == "listNeighbors":
		listClosestNeighbors(graphname,champ_data,5)
		
	elif sys.argv[2] == "bridges":
		bridges(graphname,champ_data,groups,3)
	else :
		print "that entry name is not valide," +\
			" please use : mainGroups, subGroups,"+\
			" allSubGroups, listNeighbors or bridges"
		
		
	print "\nAll done !"
