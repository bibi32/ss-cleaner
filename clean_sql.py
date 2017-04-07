#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
import re
import shutil
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

source = config.get('PATH', 'romssource')
destination = config.get('PATH', 'romsclean')

db = sqlite3.connect('nointro.db')
cur = db.cursor()

exclus = config.items('EXCLUS')
exclus2 = config.items('EXCLUS2')
regions = config.items('REGION')
consoles = config.items('CONSOLES')
keptregions = config.items('KEPTREGION')


## Foction count nbr roms null
def count_null(console):
    cur.execute("SELECT COUNT(*) FROM "+console+" WHERE status IS NULL")
    result=cur.fetchone()
    return str(result[0])

## Fonction count nbr roms OK
def count_ok(console):
    sql = "SELECT COUNT(*) FROM "+console+" WHERE status=?"
    cur.execute( sql, ('OK',))
    result=cur.fetchone()
    return str(result[0])

## Fonction Supprimer doublons
def suppr_doublon(console):
    sql = "UPDATE "+console+" SET status=? WHERE status IS NULL"
    cur.execute( sql, ('KO',))

## Fonction marquer unique
def mark_unique(console,colonne):
    cur.execute("SELECT name, COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY "+colonne+" HAVING c = 1 ")
    rows = cur.fetchall()
    for row in rows:
	sql = "UPDATE "+console+" SET status=? WHERE name=?"
	cur.execute( sql, ('OK', row[0]))

## Fonction marquer doublons
def mark_doublons(console,colonne):
    cur.execute("SELECT "+colonne+", COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY "+colonne+" HAVING c > 1")
    rows = cur.fetchall()
    for row in rows:

	## Créé la commande sql pour classer par préférence des keptregions
	i = 0
	mysqlcmd = ""
	arguments = [row[0]]
	for key, keptregion in keptregions:
	    mysqlcmd += "WHEN name LIKE ? THEN "+str(i)+" "
	    arguments.append("%"+keptregion+"%")
	    i += 1
	mysqlcmd += "ELSE "+str(i)

	sql = "SELECT name FROM "+console+" WHERE status IS NULL AND "+colonne+"=? ORDER BY CASE "+mysqlcmd+" END LIMIT 1"
	cur.execute( sql, tuple(arguments))
	rows = cur.fetchall()
	for row in rows:
	    sql = "UPDATE "+console+" SET status=? WHERE name=?"
	    cur.execute( sql, ('OK', row[0]))

## Fonction copier résultat final
def copy_roms():
    sql = "SELECT * FROM "+console+" WHERE status=?"
    cur.execute( sql, ('OK',))
    rows = cur.fetchall()
    directory = destination + console

    if os.path.exists(directory):
	shutil.rmtree(directory)

    for row in rows:
	if not os.path.exists(directory):
	    os.makedirs(directory)

	file_source = source + console + '/' + os.path.splitext(row[1])[0] + '.zip'
	file_destination = destination + console + '/' + os.path.splitext(row[1])[0] + '.zip'

	shutil.copy(file_source, file_destination)

## Fonction marquer exclus et region entre parentheses
def mark_exclude(console,variable):
    cur.execute("SELECT name FROM "+console)
    rows = cur.fetchall()
    for row in rows:
	parentheses = re.findall(r'\(.*?\)',row[0])
	for content in parentheses:
	    contenu = re.sub('[(){}<>]', '', content)
	    if variable in contenu:
		sql = "UPDATE "+console+" SET status=? WHERE name=?"
		cur.execute( sql, ('KO', row[0]))


for key, console in consoles:
    print console

## Reset status
    cur.execute("UPDATE "+console+" SET status = NULL")

## Count nbr roms
    print "nbr roms : " + count_null(console)

## Marquer exclus
    for key, exclu in exclus:
	mark_exclude(console,exclu)

## Marquer regions exclus
    for key, region in regions:
	mark_exclude(console,region)

## Marquer exclus2
    for key, exclu2 in exclus2:
	cur.execute("UPDATE "+console+" SET status=? WHERE name LIKE ? ",('KO', '%'+exclu2+'%',))

## Count nbr roms clean
    print "nbr roms clean : " + count_null(console)

## Mettre a jour noms
    cur.execute("SELECT * FROM "+console+" WHERE nom IS NULL")
    rows = cur.fetchall()
    for row in rows:
	description = row[0]
	nom = re.sub(" [\(].*?[\)]", "", description)
	sql = "UPDATE "+console+" SET nom=? WHERE description=?"
	cur.execute( sql, (nom, description))

## Marquer unique
    mark_unique(console,'nom')

## Count nbr roms non unique
    print "nbr roms non unique : " + count_null(console)

## Marquer doublons
    mark_doublons(console,'nom')

## Supprimer doublons
    suppr_doublon(console)

## Count nbr roms OK
    print "nbr roms OK : " + count_ok(console)

## Count nbr nom_ss manquant
    sql = "SELECT COUNT(*) FROM "+console+" WHERE status=? AND nom_ss IS NULL"
    cur.execute( sql, ('OK',))
    result=cur.fetchone()
    print "nbr roms nom_ss manquant : " + str(result[0])

## Stopper si nom_ss manquant
    manquant = count_null(console)
    if result[0] != 0 :

	db.commit()
	db.close()
	sys.exit("Error message")
    else :

## Marquer OK en NULL
	sql = "UPDATE "+console+" SET status = NULL WHERE status=?"
	cur.execute( sql, ('OK',))

## Marquer unique nom_ss
	mark_unique(console,'nom_ss')

## Count nbr roms non unique
	print "nbr roms non unique : " + count_null(console)

## Marquer doublons noms_ss
	mark_doublons(console,'nom_ss')

## Supprimer doublons nom_ss
	suppr_doublon(console)

## Count nbr roms OK
	print "nbr roms OK : " + count_ok(console)

## Copier resultat final
# 	copy_roms()

    db.commit()
db.close()
