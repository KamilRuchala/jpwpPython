import urllib
import urllib2
from pyquery import PyQuery
import re
from pymongo import MongoClient
import os
import ImageChops
import math, operator
import Image

## Klasa reprezentujaca kraj
class Country:

	## nazwa kraju
	name = ""
	## opis kraju pochodzacy z wikipedii
	text = ""
	## link do flagi kraju
	flag_link = ""
	## Konstruktor
	def __init__(self, name1, text1, flaglink):
		self.name = name1
		self.text = text1
		self.flag_link = flaglink

## Klasa reprezentujaca flage kraju (przydatna przy przetwarzaniu)
class Flag:
	## nazwa kraju dla danej flagi
	name = ""
	## link bazowy flagi
	link = ""
	## Konstruktor
	def __init__(self, name1, link, origin):
		self.name = name1
		self.text = link
		self.original = origin
  
adres = 'http://en.wikipedia.org/wiki/'

## metoda pobierajaca i parsujaca HTML z wikipedii
# @param country nazwa zadanego kraju 
def getHtml(country):
        adress = adres + str(country)
        response = urllib2.urlopen(adress)
        html1 = response.read()
        pq = PyQuery(html1)
        tag = pq('div#mw-content-text.mw-content-ltr')
        v = tag.text()
	html1 = re.sub("<!--.*?-->", "", v) # nie dziala na debianie a powinno http://www.dotnetperls.com/remove-html-tags-python
        result1 = re.sub("<.*?>", "", html1)
	return result1
       
## metoda zwracajaca link do flagi danego kraju
# @param country nazwa danego kraju 
def getCountryFlag(country):
        address = "http://www.mapsofworld.com/images/world-countries-flags/"+country+"-flag.gif"
	return address

## metoda zwracajaca liste zdan z danym slowem
# @param text sparsowany text danego kraju
# @param word szukane slowo
def getSentenceWith(text, word):
        lista = text.split('.')
	li = []
	regexp = ".*\s" + word + ".*\s"
	for i in xrange(len(lista)):
		if re.search(regexp, lista[i]) != None:
			li.append(lista[i])
	return li
 

## polaczenie z baza danych
def dbConnect():
	client = MongoClient('mongodb://kamil:miszcz@ds045978.mongolab.com:45978/jpwp')
	return client

## funkcja sprawdzajaca czy dany kraj jest w bazie
# @param country szukany kraj
def dbCheck(country):
	client = dbConnect() 
	db = client.jpwp
	posts = db.countries
	return posts.find_one({"name": country})

## funkcja umieszczajaca dany kraj w bazie
# @param countryObj obiekt Country
def dbInsert(countryObj):
	client = dbConnect() 
	db = client.jpwp
	db.countries.insert({
   "name": countryObj.name, 
   "text": countryObj.text,
   "flag_link": countryObj.flag_link,
})

## funkcja sprawdzajaca czy szukany link pokrywa sie z linkiem z bazy
# @param link szukany link
def dbCheckFlag(link):
	client = dbConnect() 
	db = client.jpwp
	posts = db.flags
	return posts.find_one({"link": link})

## funkcja wstawiajaca flage do bazy (poczatkowo koncepcja przewidywala historie wpisow)
# @param flagObj obiekt Flag
def dbInsertFlag(flagObj):
	client = dbConnect() 
	db = client.jpwp
	db.flags.insert({
   "name": flagObj.name, 
   "link": flagObj.text,
   "original": flagObj.original,
})

## funkcja zwracajaca kolekcje flag
def dbGetFlagCollection():
	client = dbConnect() 
	collection = client.jpwp.flags
	return collection

## funkcja porownujaca obrazki
# @param link1 link nr 1 do porownania
# @param link2 link nr 2 do porownania
def compareImages(link1, link2):
	urllib.urlretrieve(link1, "1")
	urllib.urlretrieve(link2, "2")
	im1 = Image.open("1")
	im2 = Image.open("2")

	h = ImageChops.difference(im1, im2).histogram()

	# calculate rms
	rms = math.sqrt(reduce(operator.add,map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))

	myfile1="1"
	myfile2="2"
	if os.path.isfile(myfile1):
        	os.remove(myfile1)
	else:    ## Show an error ##
        	return("Error: %s file not found" % myfile1)
	if os.path.isfile(myfile2):
        	os.remove(myfile2)
	else:    ## Show an error ##
        	return("Error: %s file not found" % myfile2)
	return rms
 
