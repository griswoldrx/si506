import unittest
import json
import requests
import pickle
import rauth  ##used for yelp oauth2.0 authentication
import sys
reload(sys)
sys.setdefaultencoding('utf8')  ## had trouble with google API returning
                                ## mixed unicode and string responses
from math import cos, asin, sqrt
from colorama import *
from colorama import init

### Used caching code from Problem Set 7 ###
### creating a cache file for book responses ###
def canonical_order(d):
    alphabetized_keys = sorted(d.keys())
    res = []
    for k in alphabetized_keys:
        res.append((k, d[k]))
    return res

def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
    prepped = req.prepare()
    return prepped.url

def get_with_caching(base_url, params_diction, cache_diction, cache_fname):
    full_url = requestURL(base_url, params_diction)
    if full_url in cache_diction:
        print "\n*** RETRIEVING data from the cached file for book request ***"
        return cache_diction[full_url]
    else:
        response = requests.get(base_url, params=params_diction)
        print "\n*** ADDING saved data to cache file for book request ***"
        cache_diction[full_url] = response.text
        fobj = open(cache_fname, "wb")
        pickle.dump(cache_diction, fobj)
        fobj.close()
        return response.text

## Check for cached results file
cache_fname = "cached_results.txt"
try:
    fobj = open(cache_fname, 'rb')
    saved_cache = pickle.load(fobj)
    fobj.close()
except:
    saved_cache = {}

## building and generating a query for Yelp API
#### The next 22 lines of code were 'borrowed' from http://letstalkdata.com/2014/02/how-to-use-the-yelp-api-in-python/ ###
def get_yelp_search_parameters(lat,long):
   params = {}
   params["term"] = "book"
   params["ll"] = "{},{}".format(str(lat),str(long))
   params["radius_filter"] = "40000"
   params["limit"] = "20"
   params['category_filter'] = 'bookstores'
   params['sort'] = '1'  ## sorts by distance from given location
   return params

def get_yelp_results(base_url, params_diction, cache_diction, cache_fname):
	consumer_key = 'wHy4mUc2jyscey_Rj1nKgQ'
	consumer_secret ='JLXpn8qNHu79JdHx1fL1bRUDR3M'
	token = 'BXIvgx6CLPn5UM8whbexdCk6IPG0HDPM'
	token_secret = 'ZCaJ05-yW7MW76q4EHoljngNAk4'

  	session = rauth.OAuth1Session(
    consumer_key = consumer_key
    ,consumer_secret = consumer_secret
    ,access_token = token
    ,access_token_secret = token_secret)

	yelp_full_url = requestURL(base_url, params_diction)
	if yelp_full_url in cache_diction:
		print "\n*** RETRIEVING data from the cached file for yelp request ***"
		return cache_diction[yelp_full_url]
	else:
		request = session.get(base_url, params = params_diction)
		print "\n*** ADDING saved data to cache file for yelp request ***"
		cache_diction[yelp_full_url] = request.text
		session.close()
		fobj = open(cache_fname, "wb")
		pickle.dump(cache_diction, fobj)
		fobj.close()
		return request.text

## Function to retrieve cached data for weather or save the data in cache file
def weather_get_with_caching(full_url, cache_diction, cache_fname):
    if full_url in cache_diction:
        print "\n*** RETRIEVING data from the cached file for weather request ***"
        return cache_diction[full_url]
    else:
        response = requests.get(full_url)
        print "\n*** ADDING saved data to cache file for weather request ***"
        cache_diction[full_url] = response.text
        fobj = open(cache_fname, "wb")
        pickle.dump(cache_diction, fobj)
        fobj.close()
        return response.text

## create a class Book to create instance variables
## try/except clauses used because not all books have all information gathered
class Book():
	""" Class to contain instances of books retrieved from Google Book API """
	def __init__(self, book_dict):
		self.title = each['volumeInfo']['title'] 
		try:
			## Many books have more than one author- had to create a list
			## and join them together as a string to have it come out right.
			self.author = []
			for author in each['volumeInfo']['authors']:
				self.author.append(author)
			self.author = ", ".join(self.author)
			
		except:
			self.author = 'NONE LISTED'
		try:
			self.length = each['volumeInfo']['pageCount']
		except:
			self.length = 'NO PAGE COUNT LISTED'
		try:
			self.rating = each['volumeInfo']['averageRating']
		except:
			self.rating = 3.0
		try:
			self.description = each['volumeInfo']['description']
		except:
			self.description = "Unfortunately no description is available"

	def __str__(self):
		return "Title: {}, Author: {}, Page Count: {}, Rating: {}".format(self.title, self.author, self.length, self.rating)

	def readingtime(self):
		try:
			x = int(self.length)//60
			y = int(self.length)%60
			return 'It will take you {} hours and {} minutes to read this book (Averaging 1 page per minute'.format(x, y)
		except:
			return 'It is impossible to determine how long this book will take to read'


## create weather condition class and create instance variables
class Weather():
	""" Class to contain instances of weather for a given location """
	def __init__(self, weather_dict):
		self.location = current_weather['current_observation']['display_location']['full']
		self.weather = current_weather['current_observation']['weather']
		self.temp = current_weather['current_observation']['temp_f']
		self.wind = current_weather['current_observation']['wind_mph']
		self.lat = current_weather['current_observation']['display_location']['latitude']
		self.lon = current_weather['current_observation']['display_location']['longitude']

	def wind_chill(self):
		self.wind_chill = float(self.temp) - (1.5 * float(self.wind))
		return self.wind_chill

	def __str__(self):
		return 'In {} it is currently {} degrees Fahrenheit and {}.'.format(self.location, self.temp, self.weather)

## create business class for yelp response and create instance variables
class Business():
	""" Class to contain instances of bookstores near a given location """
	def __init__(self, yelp_data):
		self.name = each['name']
		self.location = Business.get_address(self)
		self.rating = each['rating']
		try:
			self.phone = Business.phonenumber(self)
		except:
			self.phone = "NO NUMBER LISTED"
		self.lat = each['location']['coordinate']['latitude']
		self.lon = each['location']['coordinate']['longitude']

	def __str__(self):
		return '{} is a bookstore at {}, their phone number is: {}'.format(self.name, self.location, self.phone)
	
	def get_address(self):
		return ", ".join(each['location']['display_address'])

	def phonenumber(self):
		digits = [digit for digit in each['phone'].encode('utf-8')]
		x = "(" + "".join(digits[:3]) + ')'
		y = ' ' + "".join(digits[3:6]) + '-'
		z = "".join(digits[6:])
		return x + y + z

## First printed statement that user sees
print(Fore.BLUE + "\nI am a resource to ensure you get a great book to read this weekend!")
print "\nEnter in some basic information and I'll help you get started."


##generating a query for Google Books API
baseurl = 'https://www.googleapis.com/books/v1/volumes'
API_KEY = 'AIzaSyAFP90pDmGT39w_eOrjHq3ZmNMWtXUJqmU-k'
url_parameters = {}
url_parameters['maxResults'] = 40
url_parameters['printType'] = 'books'
search = raw_input('\nEnter an interesting search term for a book: ')
url_parameters['q'] = search
bookresp = get_with_caching(baseurl, params_diction = url_parameters, cache_diction= saved_cache, cache_fname= cache_fname)
books = json.loads(bookresp)

## generating a list of instances for the class Book using the request response
book_insts = [Book(each) for each in books['items']]

## sort book instances to determine the highest rated books
bookrec = sorted(book_insts, key = lambda x: x.rating, reverse= True)

## generating an output of the 5 highest rated books
count = 1
print '\nI have located several books that you might like based on your search term:' 
for each in bookrec[:5]:
	print '\n'
	print count, ":", each
	print Book.readingtime(each)
	count +=1

pick = raw_input('\nWhich book looks most interesting? (Enter the number of the book)\n')
descrip = bookrec[int(pick)-1].description
print '\n Book Description:'
print '\n', descrip

# Getting users location to determine the weather
the_query = raw_input(Fore.RED + '\nEnter your zip code or City,State name: ')
user_query = the_query + '.json'
weather_baseurl = 'http://api.wunderground.com/api/11b5b9d1885870b0/conditions/q/'
wunderground_API_KEY = '11b5b9d1885870b0'
full_wurl = weather_baseurl + user_query
weather_data = weather_get_with_caching(full_wurl, cache_diction = saved_cache, cache_fname = cache_fname)
current_weather = json.loads(weather_data)

## generating a print out of the current weather
print '\n*** Current Weather ***\n'
print Weather(current_weather)
mph = Weather(current_weather).wind
windchill = Weather.wind_chill(Weather(current_weather))
print "The wind is blowing at {} miles per hour".format(mph)
print "Factoring in the wind, it feels like {} degrees Fahrenheit".format(windchill)
# location = Weather(current_weather).location

## saving variables of latitude and longitue of the location the user entered
loclat = float(Weather(current_weather).lat)
loclon = float(Weather(current_weather).lon)

## Using latitude/longitude of user entry to perform a yelp search of nearby bookstores
location = [(loclat, loclon)]
baseurl = 'http://api.yelp.com/v2/search'
for lat,long in location:
	params = get_yelp_search_parameters(lat,long)
	yelp_data = get_yelp_results(baseurl, params_diction = params, cache_diction= saved_cache, cache_fname= cache_fname)
	yelp_data_json = json.loads(yelp_data)

##### Printed output of nearest 5 bookstores (query parameters specifies closet)
print(Fore.CYAN + '\n*** Nearby bookstores ***')
business_inst = [Business(each) for each in yelp_data_json['businesses']]
count = 1
for each in business_inst[:5]:
	print '\n', count, ':', each
	count +=1

selection = raw_input(Fore.MAGENTA + "\nWhich bookstore would you like to check out? (Type the number): \n")
choice = int(selection) - 1

## setting the chosen location for the selected bookstore
booklat = float(business_inst[choice].lat)
booklon = float(business_inst[choice].lon)

#Calculate the distance to the nearest book store using the Haversine formula.
def distance(lat1, lon1, lat2, lon2):
	p = 0.017453292519943295
	a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
	dist=  12742 * asin(sqrt(a))
	totaldist = dist * 0.621371
	return '%.1f' %totaldist

## Based on current weather conditions various user suggestions are provided
def weather_advice(string):
	if 'Rain' in string:
		advice = "Looks like its raining, better bring an umbrella\n"
	else:
		advice = "It's not raining.  No need for an umbrella\n"
	if Weather(current_weather).temp <40:
		advice2 = "It looks like it's cold! BRRRR, If you're walking, bundle up!\n"
	else:
		advice2 = "Thankfully its not too cold.  You could walk if you wanted to!\n"
	if mph >= 8:
		advice3 = "Damn, it's windy!\n"
	else:
		advice3 = "It doesn't appear to be very windy today.\n"
	return advice + advice2 + advice3 + "Enjoy the store and your book!\n"

###### Give distance to chosen bookstore and weather advice #######
print "\nThe bookstore you chose is", distance(loclat, loclon, booklat, booklon), "miles away!"
print weather_advice(Weather(current_weather).weather)




################ TESTS BELOW, DO NOT CHANGE #########################
print '********* UNIT TESTS **********'
class test_Final_Project1(unittest.TestCase):
    def test_one(self):
        self.assertEqual(len(bookrec), 40, 'Checking that 40 instances of Book were created')
    def test_two(self):
        self.assertEqual(bookrec[0].rating, 5.0, 'Checking that highest recommended book has a 5.0 rating')
    def test_three(self):
        self.assertEqual(type(books), type({}), 'Checking that json.loads() of a response from Google Book API query is a dictionary')
 	
class test_Final_Project2(unittest.TestCase):
 	def test_four(self):
 		self.assertIsInstance(business_inst[3], Business, "Testing that elements of yelp data Business_inst are Business instances")
	def test_five(self):
		self.assertEqual(bookrec[2].readingtime(), 'It will take you 33 hours and 21 minutes to read this book (Averaging 1 page per minute', 'checking readingtime function' )
	def test_six(self):
		(test1lat, test1lon, test2lat, test2lon) = (42.34000015, -83.88999939, 42.3178442686, -84.0212259759)
		self.assertEqual(distance(test1lat, test1lon, test2lat, test2lon), '6.9', 'testing distance function with known lat/lon coordinates')

class test_Final_Project3(unittest.TestCase):
	def test_seven(self):
		self.assertEqual(business_inst[0].phone, '(734) 369-4345', 'testing phonenumber function on a specific business instance')
	def test_eight(self):
		self.assertEqual(type(business_inst), type([]), "testing that business_inst is a list")
    


unittest.main(verbosity=2)