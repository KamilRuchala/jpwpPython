#http://docs.python-requests.org/en/latest/index.html
#http://www.travel-images.com/russia.gif

from wszystko import *
import json
import ast

#jstring = '{"address": "localhost", "port": "0", "type": "text", "content": "country(russia)"}'
jstring = '{"address": "localhost", "port": "0", "type": "text", "content": "checkflag(http://www.travel-images.com/germany.gif)"}'

data = json.loads(jstring)



def odpowiedz(content):
	#zapytanie = data["content"].split(';')
	zapytanie = content.split(';')

	regexp1 = "country.*"
	regexp2 = "checkflag.*"
	regexp3 = "tag.*"
	regexp4 = "^getflag$"

	if re.search(regexp1, zapytanie[0]) != None:
		country = re.sub("country\(", "", zapytanie[0])
		country = re.sub("\)", "", country)
		country = country.lower()
		if dbCheck(country) == None:
			kraj = Country(country, getHtml(country), getCountryFlag(country))
			flag = Flag(country, kraj.flag_link, '1')
			dbInsert(kraj)
			#dbInsertFlag(flag)
			
		else:
			tmp = dbCheck(country)
			kraj = Country(tmp['name'], tmp['text'], tmp['flag_link'])
			
	
		if len(zapytanie) == 1:
			return kraj.text
		elif len(zapytanie) == 2:	
			if re.search(regexp3, zapytanie[1]) != None:
				tag = re.sub("tag\(", "", zapytanie[1])
				tag = re.sub("\)", "", tag)
				aaa = getSentenceWith(kraj.text, tag)
				str1 = ''.join(aaa)
				return str1
			elif re.search(regexp4, zapytanie[1]) != None:
				return kraj.flag_link
			else:
				return "bad_query"
		else:
			return "bad_query"

	elif re.search(regexp2, zapytanie[0]) != None:
		uri = re.sub("checkflag\(", "", zapytanie[0])
		uri = re.sub("\)", "", uri)
		if dbCheckFlag(uri) != None:
			tmp = dbCheckFlag(uri)
			country = tmp['name']
			return country
		else:	
			col = dbGetFlagCollection()
			size = col.count()
			for i in xrange(size):
				tmp = col.find({"original": '1'},{'link':1})[i]
				compareImages(uri, tmp['link'])
	else:
		return "bad_query"


print odpowiedz(data['content'])
