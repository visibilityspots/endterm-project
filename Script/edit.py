#!/usr/bin/python

import MySQLdb, sys, optparse, re

#MySQL Connection
#db = MySQLdb.connect(host="192.168.255.84", user="puppet", passwd="puppet", db="puppet")
db = MySQLdb.connect(host="localhost", user="root", passwd="pek", db="puppet")
cursor = db.cursor()

from optparse import OptionParser
parser=OptionParser()

group = OptionGroup(parser, "Edit")
group.add_option("-g", action="store_true", help="Group option.")
group.add_option("-e", "--enable-module",dest="enable",help="Name of the module to enable")
group.add_option("-d", "--disable-module",dest="disable",help="Name of the module to disable")
group.add_option("-d", "--disable-module",dest="disable",help="Name of the module to disable")
group.add_option("-r", "--reset-module",dest="reset",help="Name of the module to reset")

parser.add_option_group(group)



parser.add_option("-n", "--hostname",dest="hostname",help="Hostname")
parser.add_option("-e", "--enable-module",dest="enable",help="Name of the module to enable")
parser.add_option("-d", "--disable-module",dest="disable",help="Name of the module to disable")
parser.add_option("-r", "--reset-module",dest="reset",help="Name of the module to reset")

(options,args)=parser.parse_args()

apache = 0
nagios = 0
php = 0
mysql = 0
bind = 0

hostname = options.hostname

if options.enable NOT "":
	if options.enable=="apache":
	    apache = int("1")
	elif options.enable=="nagios":
	    nagios = int("1")
	elif options.enable=='php':
	    php = int("1")
	elif options.enable=='mysql':
	    mysql = int("1")
	elif options.enable=='bind':
	    bind = int("1")
	else:
	    print "Module "+options.enable+" not supported by this script"
else:
	if options.disable != "":
		if options.disable=="apache":
		    apache = int("-1")
		elif options.disable=="nagios":
		    nagios = int("-1")
		elif options.disable=='php':
		    php = int("-1")
		elif options.disable=='mysql':
		    mysql = int("-1")
		elif options.disable=='bind':
		    bind = int("-1")
		else:
		    print "Module "+options.disable+" not supported by this script"
	else:
		if options.reset != "":
			if options.reset=="apache":
			    apache = int("0")
			elif options.reset=="nagios":
			    nagios = int("0")
			elif options.reset=='php':
			    php = int("0")
			elif options.reset=='mysql':
			    mysql = int("0")
			elif options.reset=='bind':
			    bind = int("0")
			else:
			    print "Module "+options.disable+" not supported by this script"
		else:
			print "Parameter needed"	

cursor.execute("SELECT `nodeid` FROM `nodes` WHERE `hostname` = %s",(hostname))
row = cursor.fetchone ()
nodeid = row[0]

cursor.execute("UPDATE `nodes` SET `module_apache` = %s, `module_nagios` = %s, `module_php` = %s, `module_mysql` = %s, `module_bind` = %s WHERE `nodeid` = %s",(apache,nagios,php,mysql,bind,nodeid))
