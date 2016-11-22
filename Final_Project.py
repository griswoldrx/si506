## Class Programming project

import unittest
import json
import requests
import pickle
##Google Books API

API_KEY = 'AIzaSyAFP90pDmGT39w_eOrjHq3ZmNMWtXUJqmU-k'
baseurl = 'https://www.googleapis.com/books/v1/volumes'
url_parameters = {}


search = raw_input('\nEnter a search term: ')
url_parameters['q'] = search
#url_parameters['key'] = API_KEY
resp = requests.get(baseurl, params = url_parameters)
print resp.url
#print resp.text
books = json.loads(resp.text)
print books.keys()
print '\n\n'
print books['items'][0]['volumeInfo']['title']
try:
	print '\n', books['items'][0]['volumeInfo']['description']
except:
	print 'No description for this book is available...... read and find out what it is about!'



the_query = raw_input('\nEnter a City name or zip code: ')
user_query = the_query + '.json'
weather_baseurl = 'http://api.wunderground.com/api/11b5b9d1885870b0/conditions/q/'
wunderground_API_KEY = '11b5b9d1885870b0'
full_url = weather_baseurl + user_query
weather = requests.get(full_url)
current_weather = json.loads(weather.text)
print weather.url
#print weather.statuses
print weather.text
