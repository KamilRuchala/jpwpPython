import urllib
import urllib2
from pyquery import PyQuery
import re
from pymongo import MongoClient
import os
import ImageChops
import math, operator
import Image


class Country:
	name = ""
	text = ""
	flag_link = ""
	def __init__(self, name1, text1, flaglink):
		self.name = name1
		self.text = text1
		self.flag_link = flaglink

class Flag:
	name = ""
	link = ""
	def __init__(self, name1, link, origin):
		self.name = name1
		self.text = link
		self.original = origin
  
adres = 'http://en.wikipedia.org/wiki/'
 
def getHtml(country):
        adress = adres + str(country)
        response = urllib2.urlopen(adress)
        html = response.read()
        pq = PyQuery(html)
        tag = pq('div#mw-content-text.mw-content-ltr')
        v = tag.text()
        result1 = re.sub("<.*?>", "", v)
	result1 = re.sub("NewPP.*", "", result1)
	f = open('dupa.txt', 'w')
	result1 = result1.encode('utf-8')
	f.write(result1)
	f.close()
	return result1
       
 
def getCountryFlag(country):
        address = "http://www.mapsofworld.com/images/world-countries-flags/"+country+"-flag.gif"
	return address

def getSentenceWith(text, word):
        lista = text.split('.')
	li = []
	regexp = ".*\s" + word + ".*\s"
	for i in xrange(len(lista)):
		if re.search(regexp, lista[i]) != None:
			li.append(lista[i])
	return li
 
def generateQuery(adres, port, typ, tresc):
        post = {"address": adres,
"port": port,
"type": typ,
"content": tresc}
        return post

def dbConnect():
	client = MongoClient('mongodb://kamil:miszcz@ds045978.mongolab.com:45978/jpwp')
	return client

def dbCheck(country):
	client = dbConnect() 
	db = client.jpwp
	posts = db.countries
	return posts.find_one({"name": country})

def dbInsert(countryObj):
	client = dbConnect() 
	db = client.jpwp
	db.countries.insert({
   "name": countryObj.name, 
   "text": countryObj.text,
   "flag_link": countryObj.flag_link,
})

def dbCheckFlag(link):
	client = dbConnect() 
	db = client.jpwp
	posts = db.flags
	return posts.find_one({"link": link})

def dbInsertFlag(flagObj):
	client = dbConnect() 
	db = client.jpwp
	db.flags.insert({
   "name": flagObj.name, 
   "link": flagObj.text,
   "original": flagObj.original,
})

def dbGetFlagCollection():
	client = dbConnect() 
	collection = client.jpwp.flags
	return collection

def compareImages(link1, link2): # http://effbot.org/zone/pil-comparing-images.htm
	urllib.urlretrieve(link1, "1.gif")
	urllib.urlretrieve(link2, "2.gif")
	im1 = Image.open("1.gif")
	im2 = Image.open("2.gif")
	(width, height) = im1.size
	im2 = im2.resize((width, height), Image.BICUBIC)
	h = ImageChops.difference(im1, im2).histogram()

	# calculate rms
	print math.sqrt(reduce(operator.add,map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))
	myfile1="1.gif"
	myfile2="2.gif"
	if os.path.isfile(myfile1):
        	os.remove(myfile1)
	else:    ## Show an error ##
        	return("Error: %s file not found" % myfile1)
	if os.path.isfile(myfile2):
        	os.remove(myfile2)
	else:    ## Show an error ##
        	return("Error: %s file not found" % myfile2)
 
