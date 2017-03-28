import urllib2
import json

# rom = "Sonic The Hedgehog 2 (World).md"
# crc = "24AB4C3A"
# romtaille = "1048576"

ssid = 'test'
sspassword = 'test'

rom = "Sonic The Hedgehog 2 (World).zip"
romtaille = '749652'
crc = '50ABC90A'

romnom = rom.replace(" ", "%20").replace("(", "%28").replace(")", "%29")


url = "https://www.screenscraper.fr/api/jeuInfos.php?devid=xxx&devpassword=yyy&softname=zzz&output=json&ssid="+ssid+"&sspassword="+sspassword+"&crc="+crc+"&systemeid=1&romtype=rom&romnom="+romnom+"&romtaille="+romtaille
req = urllib2.Request(url)
opener = urllib2.build_opener()
f = opener.open(req)

try:
    json = json.loads(f.read())

    nom_ss =  json["response"]["jeu"]["nom"]
    system_ss = json["response"]["jeu"]["systemenom"]

    print nom_ss
    print(nom_ss.upper())

    print system_ss

    print url

except ValueError, f:
#    print f
    print "ERROR"
