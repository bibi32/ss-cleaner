#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
import shutil
import hashlib
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')

db = sqlite3.connect('nointro.db')
cur = db.cursor()

source = config.get('PATH', 'romstoclean')
destination = config.get('PATH', 'romssource')

consoles = config.items('CONSOLES')

for key, console in consoles:

#    cur.execute("UPDATE "+console+" SET exist = NULL")

    cur.execute("SELECT * FROM "+console+" WHERE exist IS NULL")
    rows = cur.fetchall()

    directory = destination + console 
    if not os.path.exists(directory):
	os.makedirs(directory)

    for row in rows:
	name = row[1]
	md5 = row[6]

	files = source + console + '/' + name
	files_clean = destination + console + '/' + name

	if (os.path.isfile(files)):
	    f = open(files, 'rb')
	    extension = os.path.splitext(files)[1][1:]
	    if extension == 'nes':
		f.seek(16) # skip the first 16 bytes for nes
	    rest = f.read()
	    m = hashlib.md5()
	    m.update(rest)
	    files_md5 = m.hexdigest().upper()

	    if md5 == files_md5:
 		shutil.move(files, files_clean)
		sql = "UPDATE "+console+" SET exist=? WHERE name=?"
		cur.execute( sql, ('OK', name))
    db.commit()


    src_files = os.listdir(source + console)
    src_files.sort()
    for file in src_files:
	full_file_name = (os.path.join(source + console + '/' + file))

	f = open(full_file_name, 'rb')
	extension = os.path.splitext(full_file_name)[1][1:]
	if extension == 'nes':
	    f.seek(16) # skip the first 16 bytes for nes
	rest = f.read()
	m = hashlib.md5()
	m.update(rest)
	files_md5 = m.hexdigest().upper()

	cur.execute("SELECT * FROM "+console+" WHERE exist IS NULL")
	rows = cur.fetchall()

	for row in rows:
	    if row[6] == files_md5 :
		file_name = row[1]

		print "Trouvé : " + file
		dest = destination + console + '/' + file_name

		if (os.path.isfile(full_file_name)):
		    shutil.move(full_file_name, dest)
		    sql = "UPDATE "+console+" SET exist=? WHERE name=?"
		    cur.execute( sql, ('OK', file_name))
	else:
	    if (os.path.isfile(full_file_name)):
		os.remove(full_file_name)

	db.commit()
db.close()
