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
database = config.get('MYSQL', 'database')

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=database)
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

def saveConfig():
    global config
    config.set('CONSOLES', 'console', console_btn.get())
    config.write(open('config.ini','w'))

def alert():
    showinfo("alerte", "Bravo!")


def demande():

    def saisie():
	global config
	config.set('ID', 'devid', ask_devid.get())
	config.set('ID', 'devpassword', ask_devpassword.get())
	config.set('ID', 'ssid', ask_ssid.get())
	config.set('ID', 'sspassword', ask_sspassword.get())

	config.set('MYSQL', 'host', ask_host.get())
	config.set('MYSQL', 'user', ask_user.get())
	config.set('MYSQL', 'passwd', ask_passwd.get())
	config.set('MYSQL', 'database', ask_database.get())

	config.write(open('config.ini','w'))



    fen = Tk()
    titre = Label(fen,text="Paramètres")
    titre.grid(row=1,column=1,columnspan=4)
         
    label_devid = Label(fen,text="devid : ")
    label_devpassword = Label(fen,text="devpassword : ")
    label_ssid = Label(fen,text="ssid : ")
    label_sspassword = Label(fen,text="sspassword : ")

    label_host = Label(fen,text="host : ")
    label_user = Label(fen,text="user : ")
    label_passwd = Label(fen,text="passwd : ")
    label_database = Label(fen,text="database : ")


    value_devid = StringVar(fen, value=devid)
    value_devpassword = StringVar(fen, value=devpassword)
    value_ssid = StringVar(fen, value=ssid)
    value_sspassword = StringVar(fen, value=sspassword)

    value_host = StringVar(fen, value=host)
    value_user = StringVar(fen, value=user)
    value_passwd = StringVar(fen, value=passwd)
    value_database = StringVar(fen, value=database)


    ask_devid = Entry(fen, textvariable=value_devid)
    ask_devpassword = Entry(fen, textvariable=value_devpassword)
    ask_ssid = Entry(fen, textvariable=value_ssid)
    ask_sspassword = Entry(fen, textvariable=value_sspassword)

    ask_host = Entry(fen, textvariable=value_host)
    ask_user = Entry(fen, textvariable=value_user)
    ask_passwd = Entry(fen, textvariable=value_passwd)
    ask_database = Entry(fen, textvariable=value_database)

         
    bouttonValider = Button(fen,text="Valider",command=saisie)
    bouttonQuit = Button(fen,text="Quitter",command=quit)



    label_devid.grid(row=2,column=1)
    ask_devid.grid(row=2,column=2,columnspan=3)
    label_devpassword.grid(row=3,column=1)
    ask_devpassword.grid(row=3,column=2,columnspan=3)
    label_ssid.grid(row=4,column=1)
    ask_ssid.grid(row=4,column=2,columnspan=3)
    label_sspassword.grid(row=5,column=1)
    ask_sspassword.grid(row=5,column=2,columnspan=3)


    label_host.grid(row=6,column=1)
    ask_host.grid(row=6,column=2,columnspan=3)
    label_user.grid(row=7,column=1)
    ask_user.grid(row=7,column=2,columnspan=3)
    label_passwd.grid(row=8,column=1)
    ask_passwd.grid(row=8,column=2,columnspan=3)
    label_database.grid(row=9,column=1)
    ask_database.grid(row=9,column=2,columnspan=3)


    bouttonValider.grid(row=10,column=1)
    bouttonQuit.grid(row=10,column=2)
 
    fen.mainloop()



fenetre = Tk()
fenetre.title("Ss_cleaner")
Canvas(fenetre, width=250, height=100, bg='ivory').pack(side=TOP, padx=5, pady=5)

console_btn = StringVar()


menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=alert)
menu1.add_command(label="Paramètres", command=demande)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_radiobutton(label="gamegear", value = "gamegear", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="gb", value = "gb", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="gba", value = "gba", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="gbc", value = "gbc", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="lynx", value = "lynx", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="mastersystem", value = "mastersystem", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="megadrive", value = "megadrive", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="n64", value = "n64", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="nes", value = "nes", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="sega32x", value = "sega32x", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="snes", value = "snes", command=saveConfig, variable = console_btn)
menu2.add_radiobutton(label="virtualboy", value = "virtualboy", command=saveConfig, variable = console_btn)
menubar.add_cascade(label="Consoles", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Importer DAT", command=alert)
menu3.add_command(label="Mise à jour ss", command=ss_update)
menu3.add_command(label="Nettoyer liste roms", command=clean_roms)
menu3.add_command(label="Verifier roms", command=alert)
menubar.add_cascade(label="Actions", menu=menu3)

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu4)

fenetre.config(menu=menubar)


fenetre.mainloop()
