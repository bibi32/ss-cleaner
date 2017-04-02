#!/usr/bin/python
# -*- coding: utf-8 -*- 

from Tkinter import *
import tkFileDialog as filedialog
import MySQLdb
import urllib
import urllib2
import json
import cgi
import re
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

host = config.get('MYSQL', 'host')
user = config.get('MYSQL', 'user')
passwd = config.get('MYSQL', 'passwd')
db = config.get('MYSQL', 'db')

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
cur = db.cursor()

devid = config.get('ID', 'devid')
devpassword = config.get('ID', 'devpassword')
ssid = config.get('ID', 'ssid')
sspassword = config.get('ID', 'sspassword')

exclus = config.items('EXCLUS')
exclus2 = config.items('EXCLUS2')
regions = config.items('REGION')
keptregions = config.items('KEPTREGION')
consoles = config.items('CONSOLES')

def ss_update():
    execfile("ss.py")

def clean_roms():
    execfile("clean_sql.py")



def alert():
    showinfo("alerte", "Bravo!")


fenetre = Tk()
fenetre.title("Ss_cleaner")
Canvas(fenetre, width=250, height=100, bg='ivory').pack(side=TOP, padx=5, pady=5)

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=alert)
menu1.add_command(label="Editer", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command=alert)
menu2.add_command(label="Copier", command=alert)
menu2.add_command(label="Coller", command=alert)
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="gamegear", command=alert)
menu3.add_command(label="gb", command=alert)
menu3.add_command(label="gba", command=alert)
menu3.add_command(label="gbc", command=alert)
menu3.add_command(label="lynx", command=alert)
menu3.add_command(label="mastersystem", command=alert)
menu3.add_command(label="megadrive", command=alert)
menu3.add_command(label="n64", command=alert)
menu3.add_command(label="nes", command=alert)
menu3.add_command(label="sega32x", command=alert)
menu3.add_command(label="snes", command=alert)
menu3.add_command(label="virtualboy", command=alert)
menubar.add_cascade(label="Console", menu=menu3)

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="Importer DAT", command=alert)
menu4.add_command(label="Mise à jour ss", command=ss_update)
menu4.add_command(label="Nettoyer liste roms", command=clean_roms)
menu4.add_command(label="Verifier roms", command=alert)
menubar.add_cascade(label="Actions", menu=menu4)

menu5 = Menu(menubar, tearoff=0)
menu5.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu5)

fenetre.config(menu=menubar)


fenetre.mainloop()
