from wszystko import *
import json
import ast

## funkcja przetwarzajaca dane zapytanie, zwraca odpowiedni wynik
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
			
		else:
			tmp = dbCheck(country)
			kraj = Country(tmp['name'], tmp['text'], tmp['flag_link'])
			
	
		if len(zapytanie) == 1:
			return kraj.text.encode('utf8')
		elif len(zapytanie) == 2:	
			if re.search(regexp3, zapytanie[1]) != None:
				tag = re.sub("tag\(", "", zapytanie[1])
				tag = re.sub("\)", "", tag)
				aaa = getSentenceWith(kraj.text, tag)
				str1 = ''.join(aaa)
				return str1.encode('utf8')
			elif re.search(regexp4, zapytanie[1]) != None:
				return kraj.flag_link.encode('utf8')
			else:
				return "bad_query"
		else:
			return "bad_query"

	#### sekcja przetwarzania obrazow ####
	elif re.search(regexp2, zapytanie[0]) != None:
		uri = re.sub("checkflag\(", "", zapytanie[0])
		uri = re.sub("\)", "", uri)
		if dbCheckFlag(uri) != None: # jesli jest link w bazie - zwroc nazwe, nie porownuj
			tmp = dbCheckFlag(uri)
			country = tmp['name']
			return country
		else:				# jesli nie to porownanie  
			col = dbGetFlagCollection()
			size = col.count() 
			tmpName = None # nazwa kraju z najmniejszym rms
			tmpRMS = 300 # aktualny najmniejszy RMS
			for i in xrange(size):
				tmp = col.find({"original": '1'},{'link':1, 'name' : 1})[i]
				rms = compareImages(uri, tmp['link'])
				print tmp['name'] + str(rms)	
				if rms < tmpRMS:
					tmpName = tmp['name']
					tmpRMS = rms
			return tmpName
	else:
		return "bad_query"

