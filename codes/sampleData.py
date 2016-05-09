#############################################
## sampleData.py
## by Lyunee
## 
## all the functions used to sample data
## from RIOT API 
## for the RIOT API challenge 2016
## 
#############################################


import requests
import json
import time
import sys
from datetime import timedelta



## global variables
	# API key
try :
	with open("RIOT_API_KEY.txt","r") as f:
		API_KEY = f.read()
except :
	print "Unable to get the API key."
	print "Terminate program."
	sys.exit()

	# create time variables
TODAY = timedelta(days = 30).total_seconds()*1000
# for time stamp of the sample
ONEMONTH = int(round(time.time() * 1000))
# to check if champion was recently palyed
		

def getRequest(the_request, error_msg):
## get the request from RIOT API
	
	time.sleep(1)  # let's not overload
	r = requests.get(the_request+ 'api_key=' + API_KEY)
	if r.status_code != 200:
		print "error with the request for " + error_msg + \
			" : " + str(r.status_code)
		return False
	return r


def getMasteries_mc(the_region,the_rank):
## get the masteries for rank master of challenger (the_rank)
##     for the region the_region

	# sample only solo queue
	the_type = 'RANKED_SOLO_5x5'

	# get the information
	the_request = 'https://' + the_region + \
		'.api.pvp.net/api/lol/' + the_region + \
		'/v2.5/league/' + the_rank + '?type=' + the_type +'&'
	r = getRequest(the_request, "region "+the_region+" and rank "+ the_rank)
	if not r :
	# if request fail, stop everything
		print "Terminate program"
		sys.exit()
	
	# count number of sampled players
	Ncount = 0
	
	# for each player sampled :
	for one_entry in r.json()['entries']:
	
		# get the player's id
		the_id = one_entry['playerOrTeamId']
		
		# get that players champion mastery saved directly to file
		if getMastery(the_id, the_region,the_rank):
			Ncount += 1

	print "For region "+ the_region + \
		" and the rank " + the_rank + \
		" we sampled " + str(Ncount) + " players."

def getMasteries_other(the_region):
## get the masteries for random ranks
##     using featured games
##     for the region the_region
	
	leagues_looked_at = []
	# to avoid looking twice at the same league
	
	## 1. Get Featured Games
	
	the_request = 'https://' + the_region + \
		'.api.pvp.net/observer-mode/rest/featured?'
	r = getRequest(the_request, "featured game in "+the_region)
	if not r: # if error
		print "Terminate program"
		sys.exit()
	featuredGames = r.json()
	if len(featuredGames['gameList']) == 0 :
		print 'no game in gameList for region ' + the_region
		print "Terminate program"
		sys.exit()
    
	## 2. Get Players Names
	sumNames = []
	for game in featuredGames['gameList'] : # for each game
		if len(game['participants'])==0: # check participants
			continue
		# add names to the list
		for player in game['participants']:
			sumNames.append(player['summonerName'])

	if len(sumNames)>40: # limite to 40 names (as ingle API call)
		sumNames = sumNames[0:40]
	if len(sumNames)==0:
		print "no summoner names for region " + the_region
		print "quit program"
		sys.exit()
		
	## 3. Turn names into IDs
	the_request = 'https://' + the_region + \
		'.api.pvp.net/api/lol/'+ the_region + \
		'/v1.4/summoner/by-name/' + ','.join(sumNames) + '?'
	r2 = getRequest(the_request, "from players names to ids")
	if not r2: # error in request
		print "Terminate program"
		sys.exit()
	summoners = r2.json()
	sumIds = []
	for k in summoners.keys():
		sumIds.append(summoners[k]['id'])
		# those are int, remember to convert to string !
	
	
	## 4. get League Info => rank + more ids
	for sumID in sumIds :        
		the_request = 'https://' + the_region + \
			'.api.pvp.net/api/lol/' + the_region + \
			'/v2.5/league/by-summoner/'+ str(sumID) + '?'
		r3 = getRequest(the_request, "League info for player "+str(sumID))
		if not r3 : # continue to the next player ID
			continue
		data = r3.json()
		if len(data.keys())==0:
			print 'no league data'
			continue
		data = data[data.keys()[0]][0]
		if data['name'] in leagues_looked_at:
			continue
		the_rank = data['tier']
		
	## 5. get Mastery Data
		Ncount = 0
		for summ in data['entries']:
		# for summoner in the league
			the_id = summ['playerOrTeamId']
			
			if getMastery(the_id, the_region,the_rank):
				Ncount += 1
		leagues_looked_at.append(data['name'])
		print "For league "+ data['name'] + \
			" of rank " + the_rank + \
			" we sampled " + str(Ncount) + " players"


def getMastery(the_id, the_region,the_rank):
## get the mastery for a given player id
## filter and save them
	
	# request the mastery data
	the_request = 'https://' + the_region + \
		'.api.pvp.net/championmastery/location/' + the_region.upper() + \
		'1/player/' + the_id + '/champions?'
	r_m = getRequest(the_request, "mastery of player "+the_id)
	if not r_m:
	#if request fail, move to next player
		print "Move on to next player"
		return False
	champions = r_m.json()
	# filter the champions
	filtered_champ = filter_champ(champions)
	# create the format of saved data
	the_info = {"playerRank":the_rank, \
		"masteries":filtered_champ, \
		"samplingTime":TODAY}
	# save the sampled data, in a json format
	with open('Data\\' + the_region + '_' + str(the_id) + '.txt', 'wb') as outfile:
		json.dump(the_info, outfile)
	return True
			
		
def filter_champ(champions):
## filter the champions 
## based on their mastery points
    filtered_champ = []
    # look at all champions
    for champ in champions :
    # only considered level 4 champs
        if champ["championLevel"]<4 :
            break
    # filter out those not played for a month
        if TODAY - champ["lastPlayTime"] > ONEMONTH :
            continue
        filtered_champ.append(
			{"championId" :champ['championId'],
			"championPoints":champ['championPoints']})
    return filtered_champ
		
if __name__ == "__main__":
	if sys.argv[1] == "master" or sys.argv[1] == "challenger":
		print "\nSampling starting for rank " + sys.argv[1] + \
			" in region " + sys.argv[2]
		getMasteries_mc(sys.argv[2],sys.argv[1])
	elif sys.argv[1] == "other" :
		print "\nSampling starting through featured games " +  \
			" in region " + sys.argv[2]
		getMasteries_other(sys.argv[2])
	else :
		print "\nfirst option is not correct"
		print "try 'master' , 'challenger' or 'other'"