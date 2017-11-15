"""
CS 5306: Project 1
(reb343)
"""

import requests
import json

 # TODO choose games to analyzie
   # - how many
   # - which ones
from keys import *

GAME_IDS = {582160: "Assassin's Creed Origins", 107200: "Space Pirates and Zombies"}

 # TODO decide if certain date-range (e.g. first n days after release), and if so, what n?


def get_all_apps():
	"""
		TODO: get all apps from steam,save to file
	"""
	pass


def filter_games_from_apps():
	"""
		TODO: using list of all apps; filter games and save IDs to file (maybe other relevant info...)
	"""
	# TODO get a steam key
	url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=" + STEAM_KEY + "&format=json"
	pass


def get_selected_games_steam():
	"""
		TODO: read in data from steam and save to file
	"""
	file = open("steam_data.json", 'w')
	allGameData = {}
	for gid in GAME_IDS.keys():
		allGameData[gid] = {}
		url = "http://store.steampowered.com/appreviews/" + str(gid) + "?json=1&filter=all&language=all&review_type=all&purchase_type=all&day_range=9223372036854775807"
 		data = requests.get(url)
 		assert data.status_code == 200, "GET failed on game " + GAME_IDS[gid]
 		resultJson = json.loads(data.content)
 		total = resultJson['query_summary']['total_reviews']
 		# store resultJson in file so only have to do this once late on
 		allGameData[gid][0] = resultJson
 		count = None
 		print GAME_IDS[gid]
 		print total
 		for count in xrange(20, total, 20):
 			url = "http://store.steampowered.com/appreviews/" + str(gid) + "?json=1&filter=all&language=all&review_type=all&purchase_type=all&day_range=9223372036854775807&start_offset=" + str(count)
 			# store results in file
 			allGameData[gid][count] = json.loads(requests.get(url).content)
 	file.write(json.dumps(allGameData))
 	file.close()
 	return allGameData


def get_data_from_file(path="steam_data.json"):
	"""
		read in steam data from path
		Parameters:
			path - string - path of file to read in
		Returns
			dict - dictionary representation of json data from steam API
	"""
	file = open(path)
	result = json.loads(file.read())
	file.close
	return result

 # TODO parse data

def get_average_review_field(key, game, data):
  	"""
 		TODO: return the average value for the given key
 	"""
 	all_ = []
 	gameData = data[game]
 	numReviews = gameData[str(0)]['query_summary']['total_reviews']
 	for r in range(0, numReviews, 20):
 		reviewSet = gameData[str(r)]['reviews']
 		for i in range(0, len(reviewSet)): # TODO why is reviewset always len 3??
 			# print i
 			review = reviewSet[i]
 			# TODO try to convert to float; if fails, return error message
 			try:
 				all_.append(float(review[key]))
 			except Exception as e:
 				print "Incompatible value type for average"
 				raise e
 	return all_ # TODO all zeros for 107200 (space pirates) but not assasin's creed?
 	# return sum(all_)/len(all_)



def get_average_author_field(key, game, data):
	"""
		TODO: return the average value for the given key from author field of reviews
	"""
	pass


 # TODO run analysis