import json
import requests
import locale
from configparser import ConfigParser

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

CONFIG_FILE = "trafiklab.conf"

parser = ConfigParser()
parser.read(CONFIG_FILE)

API_KEY_PLATSUPPSLAG = parser.get('trafiklab','api_key_sl_platsuppslag')
API_KEY_REALTIDSINFORMATION = parser.get('trafiklab','api_key_sl_realtidsinformation')
API_KEY_HALLPLATSEROCHLINJER = parser.get('trafiklab','api_key_sl_hallplatserochlinjer')


# Find stations based on search string
def findstation(station):
   onlystations = "True"
   maxreplies = 20
   urlstation = "https://api.sl.se/api2/typeahead.json?key={0}&searchstring={1}&stationsonly={2}&maxresults={3}".format(API_KEY_PLATSUPPSLAG, station, onlystations, maxreplies)
   print(urlstation)
   response = requests.get(urlstation)
#   print(response.json())

   for row in response.json()['ResponseData']: 
      name = (row['Name'])
      siteid = (row['SiteId'])
      types = (row['Type'])
      x = (row['X'])
      y = (row['Y'])
      print(name + ", " + siteid + ", " + types + ", " + x + ", " + y)
   return


# Real-time info for a given station id
def realtimeinfo(stationid):
   timewindow = "30"
   urlrealtimeinfo = "http://api.sl.se/api2/realtimedeparturesV4.json?key={0}&siteid={1}&timewindow={2}".format(API_KEY_REALTIDSINFORMATION, stationid, timewindow)

   response = requests.get(urlrealtimeinfo)
   print(response.json())
   print("Buses")
   for row in response.json()['ResponseData']['Buses']:
      name = (row['StopAreaName'])
      whentable = (row['DisplayTime'])
      number = (row['LineNumber'])
      whereto = (row['Destination'])
	  
      print(number + " avgår om: " + whentable + " mot: " + whereto + " (" + name + ")")

   print("Metros")
   for row in response.json()['ResponseData']['Metros']:
      name = (row['StopAreaName'])
      whentable = (row['DisplayTime'])
      number = (row['LineNumber'])
      whereto = (row['Destination'])
	  
      print(number + " avgår om: " + whentable + " mot: " + whereto + " (" + name + ")")


	  
   return


#findstation("Fridhemsplan")

#Fridhemsplan = 9115
#Polhemsgatan = 1202
#Pontonjärparken = 1207
realtimeinfo(1202) # 1202, 1207

