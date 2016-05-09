#############################################
## drawGraphs.py
## by Lyunee
## 
## draw the graph or sub-graphs
## and saves them
## for the RIOT API challenge 2016
## 
#############################################



import sys
import networkx as nx
import pickle
from getGroups import loadH
import copy
import matplotlib.pyplot as plt


def loadGroups(graphname):
	with open(graphname+"_groups.txt", "r") as f:
		values = pickle.load(f)
		groups = pickle.load(f)
	return values, groups

def getPositions(getOld,graphname,H):
	if getOld == "True": # if re-use old positions
		print "\nLoad positions"
		with open(graphname + "_pos.txt","r") as f:
			pos = pickle.load(f)
	else :
		print "\nDetermine positions"
		pos = nx.spring_layout(H)
	return pos

def drawDots(H,pos,values,graphname) :
	fig=plt.figure(figsize=(20,20))
	nx.draw_networkx_edges(H,pos,edge_color = "y")
	nx.draw_networkx_nodes(H,pos,node_color = values)
	ax=plt.gca()
	plt.axis('off')
	plt.savefig(graphname+"_dots",bbox_inches='tight', transparent=True)
	print "\t saved "+graphname+"_dots"
	

def drawImgs(H,pos,values,graphname,img_size) :
	fig=plt.figure(figsize=(20,20))
	nx.draw_networkx_edges(H,pos,edge_color = "y")
	ax=plt.gca()
	plt.axis('off')
	trans=ax.transData.transform
	trans2=fig.transFigure.inverted().transform
	piesize=img_size # this is the image size
	p2=piesize/2.0
	for n in H:
		xx,yy=trans(pos[n]) # figure coordinates
		xa,ya=trans2((xx,yy)) # axes coordinates
		a = plt.axes([xa-p2,ya-p2, piesize, piesize])
		a.set_aspect('equal')
		a.imshow(H.node[n]['image'])
		a.axis('off')
	plt.savefig(graphname+"_imgs",bbox_inches='tight', transparent=True)
	print "\t saved "+graphname+"_imgs"
	
def allDraw(H,graphname,getOldPos,dotORimg) :
# get positions
	pos = getPositions(getOldPos,graphname,H)	
	
	if dotORimg == "dot":
		print "\nDraw the graph with colored dots"
		drawDots(H,pos,values,graphname)
	elif dotORimg == "img":
		print "\nDraw the graph with images"
		drawImgs(H,pos,values,graphname,0.02)
	else :
		print "\nProblem with dots or images : draw with images"
		drawImgs(H,pos,values,graphname,0.02)
		
	print "\nSave the positions"
	with open(graphname + "_pos.txt","w") as f:
		pickle.dump(pos,f)

	
	
if __name__ == "__main__":
	
	graphname = sys.argv[1]
	print "\nLoad the graph " + graphname
	H = loadH(graphname)
	print "\nLoad the groups "
	values, groups = loadGroups(graphname)
	
## the whole graph
	if sys.argv[2] == "all":
		print "\t\t The whole graph"
		allDraw(H,graphname,sys.argv[4],sys.argv[3])
## groups
	if sys.argv[2] == "groups":
	# for each group
		for gr in groups.keys():
			print "\t\t The group " + str(gr)
			G = copy.deepcopy(H)
			for k in groups.keys():
				if k != gr :
					G.remove_nodes_from(groups[k])
			# G is now the graph of the group gr
			allDraw(G,graphname+"_gr"+str(gr),sys.argv[4],sys.argv[3])
		

