#! /usr/bin/env python
import json
import urllib2
import time
import os
'''This script will call Google Maps to calculate the time to walk between every combination of bus stops and the time to drive between every combination of bus stops. We can't do this live in the app because of rate limiting and because Google requires you show a map, which I don't want to do. '''

#We'll have to go through each of the 17 stops with one origin and all 16 other stops as destinations. So we'll end up with fitten.json, mcm8th.json, etc. Then we can access the json for the specific starting point, find the destination, and get the travel time. Rate limiting prevents doing this in a more elegant way with fewer API calls.

places = ["33.7782,-84.4041","33.7795,-84.4041","33.7796,-84.4029","33.7784,-84.4009","33.7782,-84.3994","33.7782,-84.3975","33.7772,-84.3956","33.7769,-84.3938","33.7797,-84.3921","33.7752,-84.392","33.774,-84.3919","33.7715,-84.3919","33.7701,-84.3917","33.7722,-84.3955","33.7728,-84.397","33.7735,-84.3991","33.7754,-84.4025"]

name = ["fitten", "mcm8th", "8thhemp", "fershemrt", "fersstmrt", "fersatmrt", "ferschmrt", "5thfowl", "tech5th", "tech4th", "techbob", "technorth", "nortavea_a", "ferstcher", "hubfers", "centrstud", "765femrt"]
print "This will take about 10 minutes, so sit tight."

# Make the driving directory if it does not exist
if not os.path.exists("data/driving"):
	os.makedirs("data/driving")

get_times(false)

# Make the walking directory if it does not exist
if not os.path.exists("data/walking"):
	os.makedirs("data/walking")

get_times(true)

def get_times(walking):
	"""Get the travel time either walking or driving to all the bus stops."""

	index = 0

	mode = "walking" if walking else "driving"

	for i in places:
		print "Fetching " + name[index] + " walk times..."

		url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=" + i + "&destinations=33.7782,-84.4041|33.7795,-84.4041|33.7796,-84.4029|33.7784,-84.4009|33.7782,-84.3994|33.7782,-84.3975|33.7772,-84.3956|33.7769,-84.3938|33.7797,-84.3921|33.7752,-84.392|33.774,-84.3919|33.7715,-84.3919|33.7701,-84.3917|33.7722,-84.3955|33.7728,-84.397|33.7735,-84.3991|33.7754,-84.4025&sensor=false&mode=" + mode

		# Write the data to the file
		json_response = json.load(urllib2.urlopen(url))

		with open("data/" + mode + "/" + name[index] + ".json", 'w') as output_file:
			json.dump(json_response, output_file)

		index = index + 1

		# Wait for rate limit
		time.sleep(15)

'''
fitten: 33.7782, 84.4041
33.7795, 84.4041
33.7796, 84.4029
33.7784, 84.4009
33.7782, 84.3994
33.7782, 84.3975
33.7772, 84.3956
33.7769, 84.3938
33.7797, 84.3921


33.7752, 84.392
33.774, 84.3919
33.7715, 84.3919
33.7701, 84.3917
33.7722, 84.3955
33.7728, 84.397
33.7735, 84.3991
33.7754, 84.4025 (CRC)

'''
