"""
CS 5306: Project 1
(reb343)
"""

import requests
import json
from datetime import datetime
import bisect
import time

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
		using list of all apps; filter games and save IDs to file (maybe other relevant info...)
	"""
	file = open("all_app_data.json")
	allApps = json.loads(file.read())
	file.close()
	games = {}
	dateList = []
	idByRelease = []
	count = -1
	for app in allApps['applist']['apps']:
		count += 1
		# TODO check with API to see if app is game
		appid = app['appid']
		url =  "http://store.steampowered.com/api/appdetails?appids=" + str(appid)
		data = requests.get(url)
		if data.status_code == 429:
			# rate limiting
			while data.status_code == 429:
				print "waiting"
				print count
				time.sleep(120)
				data = requests.get(url)
		if data.status_code != 200:
			print data
			print "GET failed on game " + app['name']
			continue # skip this app
		resultJson = json.loads(data.content)
		if resultJson[str(appid)]['success']:
			apptype = resultJson[str(appid)]['data']['type']
			# check type is game
			if apptype == "game":
				releaseDate = resultJson[str(appid)]['data']['release_date']['date']
				# TODO convert release date to a more useable form
				# TODO maybe save a list of ids sorted by release date?
				try:
					dateobj = datetime.strptime(releaseDate, '%b %d, %Y') # <- This won't matter in saved file, do later
				except:
					try:
						dateobj = datetime.strptime(releaseDate, '%d %b, %Y')
					except:
						continue # skip if no date
				index = bisect.bisect(dateList, dateobj)
				idByRelease.insert(index, appid)
				# save release date and name
				games[appid] = {"name": app['name'], "release": releaseDate}
	# TODO save all games
	try:
		file = open("all_game_ids.json", 'w')
		file.write(json.dumps(games))
		file.close
	except:
		print "writing games failed"
	try:
		file = open("all_game_ids_by_date", 'w')
		file.write(json.dumps({"ids": idByRelease, "dates": dateList}))
		file.close()
	except:
		print "writing dates failed"
	return games, idByRelease, dateList


def load_in_games():
	"""
		TODO: load in game ids from file
	"""
	file = open("all_game_ids.json")
	data = json.loads(file.read())
	file.close()
	return data


def get_all_review_data():
	"""
		TODO: grab all game ids, grab all review data for game ids
	"""
	game_ids = load_in_games()
	print "debug check"
	review_data = get_selected_games_steam(game_ids.keys())	
	return review_data


def small_batch_helpfullness(saveto):
	"""
		TODO: look at n games, released withing d days of each other
		look at reviews from 0-m days after release
		compare helpfullness to user quality
		also save reviews to file
	"""
	start = 100
	n = 200
	d = 10
	m = 10
	# get sorted ids
	file = open("all_game_ids_by_date.json")
	ids_by_date = json.loads(file.read())["ids"]
	file.close()
	file = open("all_game_ids.json")
	ids_and_dates = json.loads(file.read())
	file.close()
	# TODO get n ids, released within d days of each other (0 is most recent release)
	startdate = ids_and_dates[ids_by_date[start]]['release']
	count = 0
	index = start
	lookahead = True
	ids_to_use = [ids_by_date[start]]
	while count < n:
		if lookahead:
			index += 1
			nextid = ids_by_date[index]
			nextdate = ids_and_dates[nextid]['release'] 
			try:
					nextdate = datetime.strptime(nextdate, '%b %d, %Y') 
			except:
				try:
					nextdate = datetime.strptime(nextdate, '%d %b, %Y')
				except:
					continue # skip if no date
			if abs(startdate - nextdate) < d:
				ids_to_use.append(nextid)
				count += 1
			else:
				index = start
				lookahead = False
		else:
			index -=1
			nextid = ids_by_date[index]
			nextdate = ids_and_dates[nextid]['release']
			try:
					nextdate = datetime.strptime(nextdate, '%b %d, %Y') 
			except:
				try:
					nextdate = datetime.strptime(nextdate, '%d %b, %Y')
				except:
					continue # skip if no date
			if abs(startdate - nextdate) < d:
				ids_to_use.append(nextid)
				count += 1
			else:
				# can't find anymore dates withing d
				break
	# TODO get reviews for ids
	reviews = get_selected_games_steam(ids_to_use, saveto)
	# TODO compare helpfullness and reviewer experience


def get_selected_games_steam(ids, saveto):
	"""
		TODO: read in data from steam and save to file
	"""
	file = open(saveto, 'w')
	allGameData = {}
	current = 0
	if ids is None:
		ids = GAME_IDS.keys()
	for gid in ids:
		current += 1
		gid = int(gid)
		allGameData[gid] = {}
		url = "http://store.steampowered.com/appreviews/" + str(gid) + "?json=1&filter=all&language=all&review_type=all&purchase_type=all&day_range=9223372036854775807"
 		data = requests.get(url)
 		# assert data.status_code == 200, "GET failed on game " + GAME_IDS[gid]
 		if data.status_code == 429:
 			while data.status_code == 429:
				print "waiting"
				print current
				time.sleep(120)
				data = requests.get(url)
 		elif data.status_code != 200:
 			continue
 		resultJson = json.loads(data.content)
 		total = resultJson['query_summary']['total_reviews']
 		# store resultJson in file so only have to do this once late on
 		allGameData[gid][0] = resultJson
 		count = None
 		# print GAME_IDS[gid]
 		print current
 		for count in xrange(20, total, 20):
 			url = "http://store.steampowered.com/appreviews/" + str(gid) + "?json=1&filter=all&language=all&review_type=all&purchase_type=all&day_range=9223372036854775807&start_offset=" + str(count)
 			# store results in file
 			try:
 				allGameData[gid][count] = json.loads(requests.get(url).content)
 			except:
 				pass
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