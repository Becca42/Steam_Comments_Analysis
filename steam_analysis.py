"""
CS 5306: Project 1
(reb343)
"""

import requests
import json
from datetime import datetime
import bisect

 # TODO choose games to analyzie
   # - how many
   # - which ones
from keys import *

GAME_IDS = {582160: "Assassin's Creed Origins", 107200: "Space Pirates and Zombies"}

 # TODO decide if certain date-range (e.g. first n days after release), and if so, what n?


def get_all_apps():
	"""
		get all apps from steam,save to file
	"""
	file = open("all_app_data.json", 'w')
	url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=" + STEAM_KEY + "&format=json"
	data = requests.get(url)
	assert data.status_code == 200, "APP RETRIEVAL FAILED"
	resultJson = json.loads(data.content)
	file.write(json.dumps(resultJson))
	file.close()
	return resultJson


def filter_games_from_apps():
	"""
		TODO: using list of all apps; filter games and save IDs to file (maybe other relevant info...)
	"""
	file = open("all_app_data.json")
	allApps = json.loads(file.read())
	file.close()
	games = {}
	dateList = []
	idByRelease = []
	for app in allApps['applist']['apps']:
		# TODO check with API to see if app is game
		appid = app['appid']
		url =  http://store.steampowered.com/api/appdetails?appids= + str(appid)
		data = requests.get(url)
		assert data.status_code == 200, "GET failed on game " + app['name']
		resultJson = json.loads(data.content)
		apptype = resultJson['data']['type']
		# check type is game
		if apptype == "game":
			releaseDate = resultJson['release_date']['date']
			# TODO convert release date to a more useable form
			# TODO maybe save a list of ids sorted by release date?
			dateobj = datetime.strptime(releaseDate, '%b %d, %Y') # <- This won't matter in saved file, do later
			index = bisect.bisect(dateList, dateobj)
			idByRelease.insert(index, appid)
			# save release date and name
			games[appid] = {{"name": app['name']}, {"release": releaseDate}}
	# TODO save all games
	file = open("all_game_ids.json", 'w')
	file.write(json.dumps(games))
	file.close
	file = open("all_game_ids_by_date", 'w')
	file.write(json.dumps({"ids": idByRelease, "dates": dateList}))
	file.close()
	return games


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