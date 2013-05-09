#!/usr/bin/python
# Uit een centrale databank per node de nodige gegevens ophalen om aan de hand van deze gegevens de nagios config files weg te schrijven op de puppet master (puppet module nagios) 

import MySQLdb

conn = MySQLdb.connect (host = "192.168.255.84",
			user = "puppet",
			passwd = "puppet",
			db = "puppet")
cursor = conn.cursor ()
cursor.execute("SELECT * FROM `nodes`")
row = cursor.fetchone ()
print row [0]


# hosts.cfg

#define host{
#  host_name  google
#  alias      Internet Connection
#  address    www.google.com
#  use        generic-host
#}

# file aanmaken
cursor.execute("SELECT hostname FROM `nodes`")
row = cursor.fetchone ()
hosts = open("hosts.cfg", "w")
strDefHost=("define host { \r\t host_name \t google \r\t alias \t\t Internet Connection \r\t address \t www.google.com \r\t use \t\t generic-host \r}")
strDefHost2=("define host { \r\t host_name \t " + row[0] + " \r\t alias \t\t " + row[0] + " \r\t address \t " " \r\t parents \t\t google \r\t use \t\t generic-host \r}")
hosts.write(strDefHost+strDefHost2)
hosts.close()
cursor.close ()
conn.close ()

