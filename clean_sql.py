#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import sys
import re
import zipfile
import shutil
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

host = config.get('MYSQL', 'host')
user = config.get('MYSQL', 'user')
passwd = config.get('MYSQL', 'passwd')
db = config.get('MYSQL', 'db')

source = config.get('PATH', 'romssource')
missing = config.get('PATH', 'romsmissing')
destination = config.get('PATH', 'romsclean')

db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
cur = db.cursor()

list = config.items('EXCLUS')
consoles = config.items('CONSOLES')

for key, console in consoles:
    print console

## Reset status
#    cur.execute("UPDATE "+console+" SET status = NULL")

## Count nbr roms
    cur.execute("SELECT COUNT(*) FROM "+console+" WHERE status IS NULL")
    result=cur.fetchone()
    print "nbr roms : " + str(result[0])

## Marquer exclus
    for key, variable in list:
	cur.execute("UPDATE "+console+" SET status=%s WHERE name LIKE %s ",('KO', '%'+variable+'%',))

## Count nbr roms clean
    cur.execute("SELECT COUNT(*) FROM "+console+" WHERE status IS NULL")
    result=cur.fetchone()
    print "nbr roms clean : " + str(result[0])

## Mettre a jour noms
    cur.execute("SELECT * FROM "+console+" WHERE status IS NULL")
    rows = cur.fetchall()
    for row in rows:
	description = row[1]
	nom = re.sub(" [\(].*?[\)]", "", description)
	sql = "UPDATE "+console+" SET nom=%s WHERE description=%s"
	cur.execute( sql, (nom, description))

## Marquer unique
    cur.execute("SELECT name, COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY nom HAVING c = 1 ")
    rows = cur.fetchall()
    for row in rows:
	sql = "UPDATE "+console+" SET status=%s WHERE name=%s"
	cur.execute( sql, ('OK', row[0]))

## Count nbr roms non unique
    cur.execute("SELECT COUNT(*) FROM "+console+" WHERE status IS NULL")
    result=cur.fetchone()
    print "nbr roms non unique : " + str(result[0])

## Marquer doublons
    cur.execute("SELECT nom, COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY nom HAVING c > 1")
    rows = cur.fetchall()
    for row in rows:
	sql = "SELECT name FROM "+console+" WHERE status IS NULL AND nom=%s ORDER BY CASE WHEN name LIKE %s THEN 0 WHEN name LIKE %s THEN 1 WHEN name LIKE %s THEN 2 WHEN name LIKE %s THEN 3 ELSE 4 END LIMIT 1"
	cur.execute( sql, (row[0],'%France%', '%Europe%', '%World%', '%USA%'))
	rows = cur.fetchall()
	for row in rows:
	    sql = "UPDATE "+console+" SET status=%s WHERE name=%s"
	    cur.execute( sql, ('OK', row[0]))

## Supprimer doublons
    sql = "UPDATE "+console+" SET status=%s WHERE status IS NULL"
    cur.execute( sql, ('KO',))

## Count nbr roms OK
    sql = "SELECT COUNT(*) FROM "+console+" WHERE status=%s"
    cur.execute( sql, ('OK',))
    result=cur.fetchone()
    print "nbr roms OK : " + str(result[0])

## Count nbr nom_ss manquant
    sql = "SELECT COUNT(*) FROM "+console+" WHERE status=%s AND nom_ss IS NULL"
    cur.execute( sql, ('OK',))
    result=cur.fetchone()
    print "nbr roms nom_ss manquant : " + str(result[0])

## Copier manquant
    if result[0] != 0 :
	directory = missing + console 

	sql = "SELECT * FROM "+console+" WHERE status=%s AND nom_ss IS NULL"
	cur.execute( sql, ('OK',))
	rows = cur.fetchall()

	if os.path.exists(directory):
	    shutil.rmtree(directory)

	for row in rows:
	    if not os.path.exists(directory):
		os.makedirs(directory)

	    file_source = source + console + '/' + row[1] + '.zip'
	    file_destination = missing + console + '/' + row[1] + '.zip'

#	    shutil.copy(file_source, file_destination)

	db.commit()
#	db.close()
	sys.exit("Error message")
    else :

## Marquer OK en NULL
	sql = "UPDATE "+console+" SET status = NULL WHERE status=%s"
	cur.execute( sql, ('OK',))

## Marquer unique nom_ss
	cur.execute("SELECT name, COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY nom_ss HAVING c = 1 ")
	rows = cur.fetchall()
	for row in rows:
	    sql = "UPDATE "+console+" SET status=%s WHERE name=%s"
	    cur.execute( sql, ('OK', row[0]))

## Count nbr roms non unique
	cur.execute("SELECT COUNT(*) FROM "+console+" WHERE status IS NULL")
	result=cur.fetchone()
	print "nbr roms non unique : " + str(result[0])

## Marquer doublons noms_ss
	cur.execute("SELECT nom_ss, COUNT(*) c FROM "+console+" WHERE status IS NULL GROUP BY nom_ss HAVING c > 1")
	rows = cur.fetchall()
	for row in rows:
	    sql = "SELECT name FROM "+console+" WHERE status IS NULL AND nom_ss=%s ORDER BY CASE WHEN name LIKE %s THEN 0 WHEN name LIKE %s THEN 1 WHEN name LIKE %s THEN 2 WHEN name LIKE %s THEN 3 ELSE 4 END LIMIT 1"
	    cur.execute( sql, (row[0],'%France%', '%Europe%', '%World%', '%USA%'))
	    rows = cur.fetchall()
	    for row in rows:
		sql = "UPDATE "+console+" SET status=%s WHERE name=%s"
		cur.execute( sql, ('OK', row[0]))

## Supprimer doublons nom_ss
	sql = "UPDATE "+console+" SET status=%s WHERE status IS NULL"
	cur.execute( sql, ('KO',))

## Count nbr roms OK
	sql = "SELECT COUNT(*) FROM "+console+" WHERE status=%s"
	cur.execute( sql, ('OK',))
	result=cur.fetchone()
	print "nbr roms OK : " + str(result[0])

## Copier resultat final
	directory = destination + console
	sql = "SELECT * FROM "+console+" WHERE status=%s AND nom_ss IS NOT NULL"
	cur.execute( sql, ('OK',))
	rows = cur.fetchall()

	if os.path.exists(directory):
	    shutil.rmtree(directory)

	for row in rows:
	    if not os.path.exists(directory):
		os.makedirs(directory)

	    file_source = source + console + '/' + row[1] + '.zip'
	    file_destination = destination + console + '/' + row[1] + '.zip'

#	    shutil.copy(file_source, file_destination)


    db.commit()
db.close()
