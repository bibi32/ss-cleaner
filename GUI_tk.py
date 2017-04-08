#!/usr/bin/python
# -*- coding: utf-8 -*- 

from Tkinter import *
import Tkinter as tk
from tkFileDialog import askopenfilename
import ttk
import os
import urllib
import urllib2
import json
import cgi
import re
import time

from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

ssid = config.get('ID', 'ssid')
sspassword = config.get('ID', 'sspassword')
consoles = config.items('CONSOLES')
destination = config.get('PATH', 'romssource')

liste = []
for key, console in consoles:
    if os.path.exists(destination + console):
	liste.append(console)
consoles = liste

def ss_update():
    execfile("ss.py")

def clean_roms():
    execfile("clean_sql.py")

def saveConfig():
    global config
    config.set('CONSOLES', 'console', console_btn.get())
#    config.write(open('config.ini','w'))

def alert():
    showinfo("alerte", "Bravo!")


def demande():
    def saisie():
	global config

	config.set('ID', 'ssid', ask_ssid.get())
	config.set('ID', 'sspassword', ask_sspassword.get())

	config.write(open('config.ini','w'))

    fileName = ''
    def openFile():
	fileName = askopenfilename()
	print fileName

    fen = Tk()
    titre = Label(fen,text="Paramètres")
    titre.grid(row=1,column=1,columnspan=4)
         
    label_ssid = Label(fen,text="ssid : ")
    label_sspassword = Label(fen,text="sspassword : ")

    value_ssid = StringVar(fen, value=ssid)
    value_sspassword = StringVar(fen, value=sspassword)

    ask_ssid = Entry(fen, textvariable=value_ssid)
    ask_sspassword = Entry(fen, textvariable=value_sspassword)

    dat_ = {}
    ask_btn_ = {}
    value_dat_ = {}
    ask_dat_ = {}
    i = 4
    for console in consoles:

	dat_[console] = config.get('DAT', console)
	ask_btn_[console] = Button(fen,text="dat "+console,command=openFile)
	value_dat_[console] = StringVar(fen, value=dat_[console])
	ask_dat_[console] = Entry(fen, textvariable=value_dat_[console])
	ask_btn_[console].grid(row=i,column=1)
	ask_dat_[console].grid(row=i,column=2,columnspan=3)
	i += 1

    bouttonValider = Button(fen,text="Valider",command=openFile)
    bouttonQuit = Button(fen,text="Quitter",command=quit)

    label_ssid.grid(row=2,column=1)
    ask_ssid.grid(row=2,column=2,columnspan=3)
    label_sspassword.grid(row=3,column=1)
    ask_sspassword.grid(row=3,column=2,columnspan=3)

    bouttonValider.grid(row=i,column=1)
    bouttonQuit.grid(row=i,column=3)

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
for console in consoles:
    menu2.add_radiobutton(label = console, value = console, command=saveConfig, variable = console_btn)
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
