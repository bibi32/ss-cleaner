#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import sys
import re
import shutil
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

host = config.get('MYSQL', 'host')
user = config.get('MYSQL', 'user')
passwd = config.get('MYSQL', 'passwd')
db = config.get('MYSQL', 'db')

source = config.get('PATH', 'romssource')
destination = config.get('PATH', 'romsclean')

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
cur = db.cursor()

list = config.items('EXCLUS')
consoles = config.items('CONSOLES')


## Foction count nbr roms null
def count_null(console):
    cur.execute("SELECT COUNT(*) FROM "+console+" WHERE status IS NULL")
    result=cur.fetchone()
    return str(result[0])

## Fonction count nbr roms OK
def count_ok(console):
    sql = "SELECT COUNT(*) FROM "+console+" WHERE status=%s"
    cur.execute( sql, ('OK',))
    result=cur.fetchone()
    return str(result[0])

## Fonction Supprimer doublons
def suppr_doublon(console):
    sql = "UPDATE "+console+" SET status=%s WHERE status IS NULL"
    cur.execute( sql, ('KO',))

## Fonction marquer unique
def mark_unique(console,colonne):
    cur.execute("SELECT name, COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY "+colonne+" HAVING c = 1 ")
    rows = cur.fetchall()
    for row in rows:
	sql = "UPDATE "+console+" SET status=%s WHERE name=%s"
	cur.execute( sql, ('OK', row[0]))

## Fonction marquer doublons
def mark_doublons(console,colonne):
    cur.execute("SELECT "+colonne+", COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY "+colonne+" HAVING c > 1")
    rows = cur.fetchall()
    for row in rows:
	sql = "SELECT name FROM "+console+" WHERE status IS NULL AND "+colonne+"=%s ORDER BY CASE WHEN name LIKE %s THEN 0 WHEN name LIKE %s THEN 1 WHEN name LIKE %s THEN 2 WHEN name LIKE %s THEN 3 ELSE 4 END LIMIT 1"
	cur.execute( sql, (row[0],'%France%', '%Europe%', '%World%', '%USA%'))
	rows = cur.fetchall()
	for row in rows:
	    sql = "UPDATE "+console+" SET status=%s WHERE name=%s"
	    cur.execute( sql, ('OK', row[0]))

## Fonction copier résultat final
def copy_roms():
    sql = "SELECT * FROM "+console+" WHERE status=%s"
    cur.execute( sql, ('OK',))
    rows = cur.fetchall()

    directory = destination + console

    if os.path.exists(directory):
	shutil.rmtree(directory)

    for row in rows:
	if not os.path.exists(directory):
	    os.makedirs(directory)

	file_source = source + console + '/' + os.path.splitext(row[2])[0] + '.zip'
	file_destination = destination + console + '/' + os.path.splitext(row[2])[0] + '.zip'

	shutil.copy(file_source, file_destination)


for key, console in consoles:
    print console

## Reset status
    cur.execute("UPDATE "+console+" SET status = NULL")

## Count nbr roms
    print "nbr roms : " + count_null(console)

## Marquer exclus
    for key, variable in list:
	cur.execute("UPDATE "+console+" SET status=%s WHERE name LIKE %s ",('KO', '%'+variable+'%',))

## Count nbr roms clean
    print "nbr roms clean : " + count_null(console)

## Mettre a jour noms
    cur.execute("SELECT * FROM "+console+" WHERE nom IS NULL")
    rows = cur.fetchall()
    for row in rows:
	description = row[1]
	nom = re.sub(" [\(].*?[\)]", "", description)
	sql = "UPDATE "+console+" SET nom=%s WHERE description=%s"
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
    print "nbr roms nom_ss manquant : " + count_null(console)

## Stopper si nom_ss manquant
    manquant = count_null(console)
    if int(manquant) != 0 :

	db.commit()
	db.close()
	sys.exit("Error message")
    else :

## Marquer OK en NULL
	sql = "UPDATE "+console+" SET status = NULL WHERE status=%s"
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
#	copy_roms()

    db.commit()
db.close()
