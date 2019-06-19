# mapengine.py - Beta 0.1

import os
import sys
import time
import json
import base64
import requests
import datetime
import responses

# Required for IEC API
from requests.auth import HTTPBasicAuth

# We use examples from: https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/datasets.md
from mapbox.services.datasets import Datasets


# To run this script as a Daemon set this to True
# https://en.wikipedia.org/wiki/Daemon_(computing)
ENGINE = True

# A pause so we dont hit API Rate Limits
# How long to pause in seconds between API calls
# Values between: 5 and 20
# To stress test the API set this to 0
PAUSE = 0


# https://api.elections.org.za/
# Change this to populate the map with 2019 election data

EVENT_ID = "848"
ELURL = "https://api.elections.org.za/"

# dry-run national ID: 848
# dry-run provincial ID: 849

# 2019 National event ID: 699
# 2019 Provincial event ID: 827

# 2014 National event ID: 291
# 2014 Provincial event ID: 292

# 2016 Local event ID: 402

# Some Python Dictionaries
# We will be using these to refresh the ID's in our old tile set
# Here we move the dictionaries to RAM to save on the number of API calls
provinceDict = {} 
munisDict = {}


# Mapbox API credentials can be created here https://account.mapbox.com/
# The token must provide CRUD (create read update delete) privileges 
username = '{insert your own Mapbox username here}'
access_token = '{insert your own Mapbox API here}'


# IEC API credentials
ELusername = '{insert your own IEC API username here}'
ELpassword = '{insert your own IEC API password here}'
ELaccess_token = '{insert your own IEC API token here}'


# Set the HTTP Basic Auth header for the IEC API
headers = {'Authorization': 'bearer ' + ELaccess_token}


# Lets see how many datasets we have at Mapbox and ensure our credentials work
# https://docs.mapbox.com/api/maps/#datasets
datasets = Datasets(access_token=access_token)
listing_resp = datasets.list()
if listing_resp.status_code != 200:
    raise ApiError('GET dataset failed {}'.format(resp.status_code))
for dataset in listing_resp.json():
    print('Found Mapbox dataset: {}'.format(dataset['name']))

	# Now lets create a test feature in Cape Town for each of our datasets
	# This can be any GeoJson object - http://geojson.org/
	#feature = {'type': 'Feature', 'id': '100001', 'properties': {'name': 'Just a Test Feature with fake ID'}, 
	#			'geometry': {'type': 'Point', 'coordinates': [18.4, -33.9]}}
	#resp = datasets.update_feature(dataset['id'], '100001', feature)
	#print('Created feature response: {} '.format(str(resp.status_code)))


# While testing your environment - we stop the engine here
# When ready comment these two lines out to run the actual engine
print ( 'It works!' )
# sys.exit()


# Main Execution Loop for our Map Engine
# 
while True:


	# Assuming we use the last Dataset found above
	# 
	# Get features and decode the json object
	# https://docs.mapbox.com/api/maps/#the-feature-object
	collection = datasets.list_features(dataset['id']).json()

	found = len(collection['features'])
	if found == 0:
		print ('No features found in dataset {}'.format(dataset['name']))
		sys.exit()
	else:
		print ('Found {} features in dataset {}'.format(str(found), dataset['name']))


	# We need a dictionary of provinces
	#
	# We only load it once and keep it in RAM until the script is killed
	if (0 == len(provinceDict)):

		# http request and decode json object
		provResp = requests.get(ELURL + 'api/v1/Delimitation?ElectoralEventID=' + EVENT_ID, headers=headers)

		if provResp.status_code != 200:
		    raise Exception('Loading provinces failed with {}'.format(provResp.status_code))

		# decode the json object
		provinces = provResp.json()
		print ( 'Saving {} provinces in RAM'.format(str(len(provinces))) )


		# Populate dictionary in RAM
		for provs in provinces:

			# We Skip the Foreign country
			if provs['ProvinceID']== 99:		
				continue

			provinceDict[provs['ProvinceID']] = provs['Province']

			# We also need a dictionary of municipalities
			munisResp = requests.get(ELURL + 'api/v1/Delimitation?ElectoralEventID=' + EVENT_ID + '&ProvinceID='+ str(provs['ProvinceID']), headers=headers)

			if munisResp.status_code != 200:
				print (ELURL+'api/v1/Delimitation?ElectoralEventID=' + EVENT_ID + '&ProvinceID='+ str(provs['ProvinceID']))
				raise Exception('Loading municipalities failed with {}'.format(munisResp.status_code))

			# decode the json object
			municipalities = munisResp.json()
			print ( 'Saving {} municipalities in RAM'.format(str(len(municipalities))) )

			# Populate dictionary in ram
			for munis in municipalities:

				munisDict[munis['MunicipalityID']] = munis['Municipality']


	# Some basic checks
	if (0 == len(provinceDict)) or (0 == len(munisDict)):
		sys.exit('Coud not load required dictionaries')


	# Lets get the votes for each geoJson feature 
	# and update its properties with a new field we call PopupData
	#
	# View the updated data here: https://studio.mapbox.com/datasets/mgdev/cjszui2th0x392ws5gx6s3uac/edit/

	for feature in collection['features']:

		if not feature['id']:
			sys.exit('Can not update a feature without its ID')


		# Our current Tile Set dont have the municipal and Province IDs so this part is a temporary hack
		# We try and get the IDs from the dictionary by extracting it from the Municipal name
		# Most municipal names have the ID prefixed
		# If we succeed we save the features IDs for re-use on subsequent updates
		# WARNING this only works about 95% of the time 
		# On the map you will see areas without data AND watch the output of this code
		# The only remedy is to manually update the ID's for those few records where this method failed
		# Please edit the ID's here: https://studio.mapbox.com/datasets/mgdev/cjszui2th0x392ws5gx6s3uac/edit/


		# Does the feature already have updated IDs?
		#
		# If yes then we skip the dictionary lookup
		provID = munID = False
		for haystack in feature['properties']:
			if haystack == 'provID':
				provID = feature['properties']['provID']
			if haystack == 'munID':
				munID = feature['properties']['munID']

		# Lookup the province ID in the dictionary		
		if not provID:
			try:
		  		provID = list(provinceDict.keys())[list(provinceDict.values()).index(feature['properties']['ProvinceNa'])]
			except:
		  		print("Province not found: " + feature['properties']['ProvinceNa'])
		  		sys.exit(provinceDict)

		# Lookup the municipaluty ID in the dictionary
		if not munID:	

			if (0 == len(feature['properties']['LocalMunic'])):
				print(feature['properties']['LocalMun_1'] + " has no province code ")
				continue

			# Split the municipality name into seperate strings / words
			#
			# The first string might give us a Municipality ID
			for key,val in munisDict.items():
	  			x = val.split(" ")
	  			if ( x[0].strip() == feature['properties']['LocalMunic'].strip() ):
	  				munID = key

		if not munID or not provID:

			print("Can not update geoJson feature for: " + feature['properties']['LocalMun_1'])
			continue

		else:

			# Ok so we have the ID's needed for the IEC API endpoint
			# Then lets get the votes for this feature
			votesResp = requests.get(ELURL + 'api/v1/NPEBallotResults?ElectoralEventID=' + EVENT_ID +'&ProvinceID=' + str(provID) + '&MunicipalityID=' + str(munID), headers=headers)

			if votesResp.status_code != 200:
			    raise Exception('Loading votes failed with {}'.format(votesResp.status_code))

			# decode json object
			vote = votesResp.json()

			# Summarise the Votes for this Feature's Popup
			Info = '<br>Registered: ' + str(vote['RegisteredVoters']) + ' Voted: ' + str(vote['TotalVotesCast'])
			PopupData = ''
			otherData = 0
			otherPerc = 100
			leadingParty = letters = ''

			# Loop through the results and extract the votes
			for i in vote['PartyBallotResults']:

				# We can combine the smaller party results
				# Lets say the ones that got less than 3%
				if i['PercOfVotes'] > 3:

					otherPerc -= i['PercOfVotes']

					# Build the Initialism - no need for the full name of the party
					
					# words = i['Name'].split()
					# letters = [word[0] for word in words]

					letters = i['Abbreviation']

					# Build the popup info
					PopupData = PopupData + letters + ': ' + str(round(i['ValidVotes'])) + ' (' + str(round(i['PercOfVotes'])) + '%)<br>'

				else:

					otherData = otherData + i['ValidVotes']

				# Relies on IEC sorting the results Descending (leading party first)
				# Change this code if this assumption is not reliable
				if not leadingParty:
					 leadingParty = letters


			# We timestamp the Popups so we can see when we got the results
			dataTime = datetime.datetime.now()
			formatTime = dataTime.strftime("%d %b %H:%M")

			# Now save the Municipal ID of this feature
			feature['properties']['munID'] = munID

			# And the Province ID also
			feature['properties']['provID'] = provID

			# Update our new PopupData field with the votes
			feature['properties']['PopupData'] = PopupData + ' Other: ' + str(round(otherData)) + ' (' + str(round(otherPerc)) + '%)<br>Updated: ' + formatTime + Info

			# We also give our feature a label
			feature['properties']['label'] = 'Voting data by IEC'

			# and a geo description (Supposing nobody will drive there in the real world - hahaha)
			feature['properties']['amenity'] = 'Voting Information Centre'

			# and finally lets track the Party leading the race
			feature['properties']['leading'] = leadingParty


			# Add whatever other data you want to attach to the feature here
			# When adding fields here remember to run the export to tileset function
			# In the Mapbox Studio dashboard - click on the menu next to the dataset name
			# Choose Export to Tileset - then - Update a connected stylesheet (ignore the time warning)
			# https://studio.mapbox.com/datasets/ dataset is called: municipal-data



			# Now update this feature on our map
			try:
		  		update = datasets.update_feature(dataset['id'], feature['id'], feature).json()
		  		print (feature['properties']['LocalMun_1'] + ' UPDATED')
			except:
				print (feature['properties']['LocalMun_1'] + ' FAILED')
			
			
			# Uncomment below to view the update response
			print(update)


			# No need to exceed API rate limit
			time.sleep (PAUSE)

	if ENGINE == False:
		break

# You read upto here: well done! - heres a reward - check out these goodies
# https://docs.mapbox.com/help/tutorials/building-a-store-locator/ - give our maps interactive menu's
# https://github.com/mapbox/mapbox-cli-py - lets you interact with a map from the command line - very cool
# https://docs.mapbox.com/mapbox-gl-js/api/ - take ultimate control of the user experience with this JS	API
# The JS API will also give us more control over the caching issue - give it a try