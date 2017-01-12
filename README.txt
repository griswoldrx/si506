INTRODUCTION
------------This program will request user input to determine keywords for a book search query via the Google Books API.  The user will be presented with a list of 5 book recommendations which have been sorted to list the highest rated books.  The user can select one of the 5 recommended books to get a book description if it is available.  The user will then enter their zip code or City, State to create a query to the Underground Weather API.  They will get the current weather for their location.  Finally based on the location provided, an automatic query will be made to the Yelp API to generate a list of bookstores within 25 miles of the user’s location.  The user will select the bookstore they are interested in and the program will tell them how far away it is from their current location.  The user will also be provided guidance regarding any weather precautions needed.

HOW TO RUN THE PROGRAM
---------------------- * The user will need to execute Final_Project_Griswold.py in the terminal. * When asked to enter an interesting search term for a book, you can enter Harry Potter   as the search term to access cached data.
 * When asked which book looks interesting, you can select any choice 1 through 5 to get   
   the description from the cached data. * When asked to enter your zip code or City,State name, you can enter 48109 to access
   cached data. * When asked to which bookstore would you like to check, you can select any choice 1 
   through 5 to get the distance to the bookstore from cached data   first bookstore to access cached data. * The selections above will be necessary to pass all of the unittests provided at the end    of the program.  If you wish you can enter any other search terms or locations if you   want to access the APIs and get your own recommendation

FILES REQUIRED
--------------
 * Final_Project_Griswold.py  - python program * cached_results.txt  - contains cached data for testing * README.txt  - provides all information necessary to run the program

PYTHON MODULES REQUIRED
-----------------------
This program requires the following python modules: * unittest * json * requests * pickle * rauth   * sys * math  * colorama 

API SOURCES USED
---------------- * Google Books API    https://developers.google.com/books/docs/v1/reference/  * Wunderground Weather API    https://www.wunderground.com/weather/api/d/docs  * Yelp API    https://www.yelp.com/developers/documentation/v3/business_search 

REFERENCE LINE NUMBERS---------------------- * Sorting with a key function: line 209 * Use of list comprehension OR map OR filter: line 206 and line 257 * Class definition beginning 1: class Book- line 105 * Class definition beginning 2: class Business- line 163 * Creating instance of one class: line 206 creates book instances * Creating instance of a second class: line 257 creates business instances * Calling any method on any class instance (list all approx line numbers where this   happens, or line numbers where there is a chunk of code in which a bunch of methods are   invoked):
	1. readingtime method- line 135
	2. windchill method- line 155
	3. get_address method- line 179
	4. phonenumber method- line 182
 * Beginnings of function definitions outside classes:
	1. get_yelp_search_parameters- line 53
	2. distance function- line 271
	3. weather_advice- line 279
 * Beginning of code that handles data caching/using cached data:
	1. lines 43-49 will check to see if there is cached file, if not it will create a dictionary to save cached data.  lines 30-40, 76-87, and 91-101 will check if the url you are requesting is in the cached data file, if it is not the results of the query are added to the cached data file.
 * Test cases: beginning on line 303

RATIONALE FOR PROJECT---------------------This program was conceived of when confronted with a Final Project requirement for SI 506.  I chose to do a book recommendation program since it was a straightforward API and I felt that the output could be useful and/or interesting.  The part of the program that I am most proud of is the way that the latitude and longitude return values from the weather API are fed into a Yelp API request to get nearby bookstores.  Additionally I use the latitude and longitude values for the user’s location and the latitude/longitude values for the selected bookstore in a function which calculates the distance between the two locations.  Challenging, but very satisfying that I got it to work.

MAINTAINERS--------------------Current maintainers: * Jeremy GriswoldSections of code were copied from problem set 7 (canonical_order, get_with_caching, and requestURL functions)22 lines of code related to the OAuth2.0 request for Yelp was ‘borrowed’ from http://letstalkdata.com/2014/02/how-to-use-the-yelp-api-in-python/