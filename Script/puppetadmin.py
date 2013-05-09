#!/usr/bin/python

import MySQLdb, getopt, sys, optparse, re, array
from optparse import OptionParser

# MySQL Connection
#db = MySQLdb.connect(host="192.168.255.84", user="puppet", passwd="puppet", db="puppet")
db = MySQLdb.connect(host="localhost", user="root", passwd="pek", db="puppet")
cursor = db.cursor()

# Function for checking right ip address format
def ipFormatChk(ip):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, ip):
       return True
    else:
       return False	

# Menu with the different options that can be used to configure the puppet database
parser=OptionParser()

# Options
parser.add_option("-n", "--node",dest="node",help="Hostname of the node")
parser.add_option("-e", "--enable-module",dest="enable",help="Enable a module (name of the module)")
parser.add_option("-d", "--disable-module",dest="disable",help="Disable a module (name of the module)")
parser.add_option("-r", "--reset-module",dest="reset",help="Reset a module (name of the module)")
parser.add_option("-c", "--clear-modules",dest="clear",help="Clear all modules from a node (-c all)")
parser.add_option("-C", "--create",dest="create",help="Create new node")
parser.add_option("-D", "--delete",dest="delete",help="Delete a node")
parser.add_option("-a", "--apache-virtual-host",dest="virtualhost",help="Edit virtual hosts (add/disable/delete/enable)")
parser.add_option("-b", "--domain",dest="domain",help="Edit domains (add/disable/delete/enable)")
parser.add_option("-s", "--subdomain",dest="subdomain",help="Edit subdomains (add/delete)")
parser.add_option("-S", "--sum",dest="summary",help="Give a summary of the existing nodes (-S all)")

(options,args)=parser.parse_args()

# Initializing part ****************************************************************************************************************************************

# Get node id comparing to given hostname from database
if options.create == None:
	if options.delete == None:
		if options.node != None:
			hostname = options.node	
			try:
				cursor.execute("SELECT `nodeid` FROM `nodes` WHERE `hostname` = %s",(hostname))
			except MySQLdb.Error, e:
				print "Error %d: %s" % (e.args[0], e.args[1])
				sys.exit (1)	
			row = cursor.fetchone ()

			# Check if the node exists in the database
			try:
				nodeid = row[0]
			except:
				print hostname.upper() +" does not exist in the database, try -S/--sum for a summary of the nodes"
				sys.exit (1)
		else:
			print "Required argument -n/--node hostname of the node wasn't given"
			sys.exit (1)


# Fetching module data from database for given node
if options.create == None:
	if options.delete == None:
		if options.summary == None:
			try:
				cursor.execute("SELECT `module_apache`, `module_nagios`, `module_php`, `module_mysql`, `module_bind` FROM `nodes` WHERE `nodeid` = %s",(nodeid))
			except MySQLdb.Error, e:
				print "Error %d: %s" % (e.args[0], e.args[1])
				sys.exit (1)

			# Check if the node exists in the database
			try:
				row = cursor.fetchone ()
			except:
				print "Unexpected error, please check the parameters and try again (-h/--help)"
				sys.exit (1)			
			

			# Parse the fetched module data into variables
			apache = row[0]
			nagios = row[1]
			php = row[2]
			mysql = row[3]
			bind = row[4]

			# List of names for variables
			varList = ("apache","nagios","php","mysql","bind")
			zero = int(0)

# Program code part ****************************************************************************************************************************************

# -n/--node
# Get status from given node

if options.node != None:
	if options.enable == None:
		if options.disable == None:
			if options.reset == None:	
				if options.clear == None:
					if options.create == None:
						if options.delete == None:
							if options.virtualhost == None:
								if options.domain == None:	
									if options.subdomain == None:
										if options.summary == None:
											try:
												cursor.execute("SELECT * FROM `nodes` WHERE `hostname` = %s",(hostname))
											except MySQLdb.Error, e:
												print "Error %d: %s" % (e.args[0], e.args[1])
												sys.exit (1)
											row = cursor.fetchone ()
											stringLength = len(hostname) + 9
											i=1
											lijn = ""
											while i<=stringLength:
				 								lijn = lijn + "-"
												i=i+1
				 							print lijn
											print "|Status "+hostname.upper()+"|"
											print lijn
							
											print "* Ip address: "+row[2]
											print "* Netmask: "+ "   " +row[3]
											print "* Gateway: "+ "   " +row[4]
											if row[5] == 0:
												print "* Apache:     disabled"
											elif row[5] == -1:
												print "* Apache:     resetted"
											else:
												print "* Apache:     enabled"
											if row[6] == 0:
												print "* Nagios:     disabled"
											elif row[6] == -1:
												print "* Nagios:     resetted"
											else:
												print "* Nagios:     enabled"
											if row[7] == 0:
												print "* Php:        disabled"
											elif row[7] == -1:
												print "* Php:        resetted"
											else:
												print "* Php:        enabled"
											if row[8] == 0:
												print "* Mysql:      disabled"
											elif row[8] == -1:
												print "* Mysql:      resetted"
											else:
												print "* Mysql:      enabled"
											if row[9] == 0:
												print "* Bind:       disabled"
											elif row[9] == -1: 
												print "* Bind:       resetted"
											else:
												print "* Bind:       enabled"
											sys.exit (1)

# -e/--enable-module | -d/--disable-module | -r/--reset-module
# Edit modules from given node (enable, disable or reset - 1, -1 or 0)

# Check required argument -n/--node
if options.create == None:
	if options.delete == None:
		if options.clear == None:
			if options.virtualhost == None:
				if options.domain == None:	
					if options.subdomain == None:
						if options.summary == None:
							if options.node != None:

								# Enabling given module to node	
								if options.enable != None:
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
										# Module isn't supported		
										print "Module "+options.enable+" not supported by this script"
	
								# Disabling given module to node	
								if options.disable != None:
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
										# Module isn't supported
										print "Module "+options.disable+" not supported by this disable script"

								# Resetting given module to node
								if options.reset != None:
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
										# Module isn't supported
										print "Module "+options.reset+" not supported by this reset script"

								# Execute mysql command from the modifications to given node	
								try:
									cursor.execute("UPDATE `nodes` SET `module_apache` = %s, `module_nagios` = %s, `module_php` = %s, `module_mysql` = %s, `module_bind` = %s WHERE `nodeid` = %s",(apache,nagios,php,mysql,bind,nodeid))
									print "Node "+options.node.upper()+" has been modified"
									sys.exit (1)
								except MySQLdb.Error, e:
									print "Error %d: %s" % (e.args[0], e.args[1])
									sys.exit (1)
							else:
								print "Required argument -n/--node hostname of the node wasn't given"
								sys.exit (1)

# Clear all modules from given node (set -1 to 0)
# Check required argument -n/--node
if options.clear != None:
	if options.create == None:
		if options.delete == None:
			if options.virtualhost == None:
				if options.domain == None:	
					if options.subdomain == None:
						if options.summary == None:	
							if options.node != None:	
								for var in range(len(row)):
									if row[var] == -1:
										if varList[var] == "apache":
											apache = int(0)
										elif varList[var] == "nagios":
											nagios = int(0)
										elif varList[var] == "php":
											php = int(0)
										elif varList[var] == "mysql":
											mysql = int(0)
										elif varList[var] == "bind":
											bind = int(0)

								# Execute mysql command to clear all the modules from given node	
								try:
									cursor.execute("UPDATE `nodes` SET `module_apache` = %s, `module_nagios` = %s, `module_php` = %s, `module_mysql` = %s, `module_bind` = %s WHERE `nodeid` = %s",(apache,nagios,php,mysql,bind,nodeid))
									print "Node "+options.node.upper()+" has been cleared"
									sys.exit (1)
								except MySQLdb.Error, e:
									print "Error %d: %s" % (e.args[0], e.args[1])
									sys.exit (1)
							else:
								print "Required argument -n/--node hostname of the node wasn't given"
								sys.exit (1)

# -C/--create 
# Create a new node
# Check required argument -n/--node
if options.create != None:
	if options.delete == None:
		if options.virtualhost == None:
			if options.domain == None:	
				if options.subdomain == None:
					if options.summary == None:
						if options.node != None:
							if (len(sys.argv) == 7):
								#if (hostnameFormatChk(sys.argv[1])==True):
								hostname = options.node
								#else:
								#print "Hostname argument is not a valid hostname ([a-z].[a-z].[a-z]{2,4})"

								# Check format for ip address
								if (ipFormatChk(sys.argv[4])==True):
									ip = sys.argv[4]
								else:
									print "Ip argument is not a valid ip address"
									sys.exit (1)

								# Check format for netmask address
								if (ipFormatChk(sys.argv[5])==True):
									netmask = sys.argv[5]
								else:
									print "Netmask argument is not a valid netmask"	
									sys.exit (1)

								# Check format for gateway address	
								if (ipFormatChk(sys.argv[6])==True):				
									gateway = sys.argv[6]
								else:
									print "Gateway argument is not a valid ip address"
									sys.exit (1)
		
								try:
									cursor.execute("INSERT INTO `puppet`.`nodes` (`hostname`,`ip`,`netmask`,`gateway`)VALUES (%s, %s, %s, %s)",(hostname,ip,netmask,gateway))
									print "Node "+options.node.upper()+" has been created"
									sys.exit (1)
								except MySQLdb.Error, e:
									print "Error %d: %s" % (e.args[0], e.args[1])
									sys.exit (1)
							else:
								print "3 required arguments for create parameter (-C/--create): ip netmask gateway"
								sys.exit (1)
						else:
							print "Required argument -n/--node hostname of the node wasn't given"
							sys.exit (1)


# -D/--delete
# Delete node from database
if options.node == None:
	if options.delete != None:
		if options.virtualhost == None:
			if options.domain == None:	
				if options.subdomain == None:
					if options.summary == None:
						hostname = options.delete
						try:
							cursor.execute("SELECT `nodeid` FROM `nodes` WHERE `hostname` = %s",(hostname))
						except MySQLdb.Error, e:
							print "Error %d: %s" % (e.args[0], e.args[1])
							sys.exit (1)
	
						row = cursor.fetchone ()
		
						# Check if the node exists in the database
						try:
							nodeid = row[0]
						except:
							print hostname.upper() +" does not exist in the database, try -S/--sum for a summary of the nodes"
							sys.exit (1)

						try:
							cursor.execute("DELETE FROM `nodes` WHERE `nodeid` = %s",(nodeid))
							cursor.execute("DELETE FROM `apache_virtualhosts` WHERE `nodeid` = %s",(nodeid))
							cursor.execute("SELECT `bind_domid` FROM `bind_domains` WHERE `nodeid` = %s",(nodeid))
							print hostname.upper() + " has been deleted"

						except MySQLdb.Error, e:
							print "Error %d: %s" % (e.args[0], e.args[1])
							sys.exit (1)	

						row = cursor.fetchone ()
						if row != None:
							bindid = row[0]
							try:
								cursor.execute("DELETE FROM `bind_subdomains` WHERE `bind_domid` = %s",(bindid))
								cursor.execute("DELETE FROM `bind_domains` WHERE `nodeid` = %s",(nodeid))
								print hostname.upper() + " has also been deleted from bind domains & subdomains."
								sys.exit (1)

							except MySQLdb.Error, e:
								print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)

# -a/--apache-virtual-host
# Edit virtual hosts
if options.virtualhost != None:
	if options.domain == None:	
		if options.subdomain == None:
			if options.summary == None:
				if options.node != None:
					hostname = options.node
		
					if apache == 1:
						try:
							cursor.execute("SELECT `nodeid` FROM `nodes` WHERE `hostname` = %s",(hostname))
						except MySQLdb.Error, e:
							print "Error %d: %s" % (e.args[0], e.args[1])
							sys.exit (1)
		
						row = cursor.fetchone ()
		
						# Check if the node exists in the database
						try:
							nodeid = row[0]
						except:
							print hostname.upper() +" does not exist in the database, try -S/--sum for a summary of the nodes"
							sys.exit (1)

						if options.virtualhost=="add":
							statusViHost = int("1")
							try:
								cursor.execute("SELECT `apache_vhid` FROM `apache_virtualhosts` WHERE `nodeid` = %s",(nodeid))
							except MySQLdb.Error, e:
								print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)
				
							row = cursor.fetchone ()
							if row == None:
								statusViHost = int("1")
								try:			
									cursor.execute("INSERT INTO `apache_virtualhosts` (`nodeid`,`status`,`hostname`)VALUES (%s,%s,%s)",(nodeid,statusViHost,hostname))
									print "A virtual host for "+hostname.upper()+" has been created"
									sys.exit (1)
								except MySQLdb.Error, e:
									print "Error %d: %s" % (e.args[0], e.args[1])
									sys.exit (1)
							else:
								print "A virtual host for "+hostname.upper()+" is already defined"
								sys.exit (1)

						elif options.virtualhost=="disable":
							statusViHost = int("0")
							try:
								cursor.execute("UPDATE `apache_virtualhosts` SET `nodeid` = %s, `status` = %s, `hostname` = %s WHERE `nodeid` = %s",(nodeid,statusViHost,hostname,nodeid))
								print "The virtual host for "+hostname.upper()+ " has been disabled"
								sys.exit (1)
							except MySQLdb.Error, e:
								print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)
						elif options.virtualhost=="delete":
							statusViHost = int("-1")
							try:
								cursor.execute("UPDATE `apache_virtualhosts` SET `nodeid` = %s, `status` = %s, `hostname` = %s WHERE `nodeid` = %s",(nodeid,statusViHost,hostname,nodeid))
								print "The virtual host for "+hostname.upper()+ " has been deleted"
								sys.exit (1)
							except MySQLdb.Error, e:
								print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)
						elif options.virtualhost=="enable":
							statusViHost = int("1")
							try:
								cursor.execute("UPDATE `apache_virtualhosts` SET `nodeid` = %s, `status` = %s, `hostname` = %s WHERE `nodeid` = %s",(nodeid,statusViHost,hostname,nodeid))
								print "The virtual host for "+hostname.upper()+ " has been enabled"
								sys.exit (1)					
							except MySQLdb.Error, e:
								print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)
		
					else:
						print "The apache module is not enabled for node "+hostname.upper()+ ". Check help to enable the module"
						sys.exit (1)
				else:
					print "Required argument -n/--node hostname of the node wasn't given"
					sys.exit (1)
# -b/--domain
# Edit domains
if options.domain != None:	
	if options.subdomain == None:
		if options.summary == None:
			if options.node != None:
				if bind == 1:		
					hostname = options.node
					try:
						cursor.execute("SELECT `nodeid` FROM `nodes` WHERE `hostname` = %s",(hostname))
					except MySQLdb.Error, e:
						print "Error %d: %s" % (e.args[0], e.args[1])
						sys.exit (1)		
					row = cursor.fetchone ()
					# Check if the node exists in the database
					try:
						nodeid = row[0]
					except:
						print hostname.upper() +" does not exist in the database, try -S/--sum for a summary of the nodes"
						sys.exit (1)
					try:
						cursor.execute("SELECT `bind_domid` FROM `bind_domains` WHERE `nodeid` = %s",(nodeid))
					except MySQLdb.Error, e:
						print "Error %d: %s" % (e.args[0], e.args[1])
						sys.exit (1)
			
					row = cursor.fetchone ()
	
					splitted = hostname.rsplit('.')
					domain = splitted[1]+"."+splitted[2]

					if options.domain=="add":
						status = int("1")
						try:
							cursor.execute("SELECT `bind_domid` FROM `bind_domains` WHERE `nodeid` = %s",(nodeid))
						except MySQLdb.Error, e:
							print "Error %d: %s" % (e.args[0], e.args[1])
							sys.exit (1)
			
						row = cursor.fetchone ()				
						if row == None:
							try:
								cursor.execute("INSERT INTO `bind_domains` (`nodeid`,`status`,`domain`)VALUES (%s,%s,%s)",(nodeid,status,domain))
								print "The domain "+domain.upper()+" has been added for node "+hostname.upper()
								sys.exit (1)
							except MySQLdb.Error, e:
				     				print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)
						else:
							print "A domain for "+hostname.upper()+" is already defined"
							sys.exit (1)

					elif options.domain=="disable":
						status = int("0")
						try:			
							cursor.execute("UPDATE `bind_domains` SET `nodeid` = %s, `status` = %s, `domain` = %s WHERE `nodeid` = %s",(nodeid,status,domain,nodeid))
							print "The domain for node "+hostname.upper()+" has been disabled"
							sys.exit (1)

						except MySQLdb.Error, e:
							print "Error %d: %s" % (e.args[0], e.args[1])
							sys.exit (1)	
					elif options.domain=="delete":
						status = int("-1")
						try:
							cursor.execute("UPDATE `bind_domains` SET `nodeid` = %s, `status` = %s, `domain` = %s WHERE `nodeid` = %s",(nodeid,status,domain,nodeid))
							print "The domain for node "+hostname.upper()+" has been deleted"
							sys.exit (1)
						except MySQLdb.Error, e:
							print "Error %d: %s" % (e.args[0], e.args[1])
							sys.exit (1)
					elif options.domain=="enable":
						status = int("1")
						try:
							cursor.execute("UPDATE `bind_domains` SET `nodeid` = %s, `status` = %s, `domain` = %s WHERE `nodeid` = %s",(nodeid,status,domain,nodeid))
							print "The domain for node "+hostname.upper()+" has been enabled"
							sys.exit (1)
						except MySQLdb.Error, e:
							print "Error %d: %s" % (e.args[0], e.args[1])
							sys.exit (1)
				else:
					print "The bind module is not enabled for node "+hostname.upper()+ ". Check help to enable the module"
					sys.exit (1)	
			else:
				print "Required argument -n/--node hostname of the node wasn't given"
				sys.exit (1)

# -s/--subdomain
# Edit subdomains
if options.subdomain != None:
	if options.summary == None:
		if options.node != None:
			if (len(sys.argv) == 7):
				#if (hostnameFormatChk(options.node)==True):
				hostname = options.node
				#else:
				#print "Hostname argument is not a valid hostname ([a-z].[a-z].[a-z]{2,4})"

				# Check format for ip address
				if (ipFormatChk(sys.argv[5])==True):
					ip = sys.argv[5]
				else:
					print "Ip argument is not a valid ip address"
					sys.exit (1)
				
				try:
					cursor.execute("SELECT `nodeid` FROM `nodes` WHERE `hostname` = %s",(hostname))
				except MySQLdb.Error, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					sys.exit (1)		
				row = cursor.fetchone ()

				# Check if the node exists in the database
				try:
					nodeid = row[0]
				except:						
					print hostname.upper() +" does not exist in the database, try -S/--sum for  summary of the nodes"
					sys.exit (1)
				
				try:
					cursor.execute("SELECT `bind_domid` FROM `bind_domains` WHERE `nodeid` = %s",(nodeid))
				except MySQLdb.Error, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					sys.exit (1)
				row = cursor.fetchone ()
				bind_domid = row [0]
				
				if bind_domid != None:
					hostnameSub = sys.argv[6]
					splitted = hostnameSub.rsplit('.')
					subHostname = splitted[0]
					if bind == 1:
						if options.subdomain=="add":
							status = int("1")
							try:
								cursor.execute("INSERT INTO `bind_subdomains` (`bind_domid`,`status`,`hostname`,`ip`)VALUES (%s,%s,%s,%s)",(bind_domid,status,subHostname,ip))
								print "Subdomain added for node "+hostname.upper()
								sys.exit (1)
							except MySQLdb.Error, e:
				     				print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)
						elif options.subdomain=="delete":
							status = int("0")
							try:			
								cursor.execute("UPDATE `bind_subdomains` SET `bind_domid` = %s, `status` = %s, `hostname` = %s, `ip` = %s WHERE `nodeid` = %s",(bind_domid,status,subHostname,ip))
								print "Subdomain deleted for node "+hostname.upper()
								sys.exit (1)
							except MySQLdb.Error, e:
								print "Error %d: %s" % (e.args[0], e.args[1])
								sys.exit (1)						
					else:
						print "The bind module is not enabled for node "+hostname.upper()+ ". Check help to enable the module"
						sys.exit (1)
			else:
				print "3 required arguments for subdomain parameter (-s/--subdomain): (add/delete) ip & subhostname"
				sys.exit (1)
		else:
			print "Required argument -n/--node hostname of the node wasn't given"
			sys.exit (1)

# -S/--sum
# summary extracted from the nodes table

if options.node == None:
	if options.summary != None:
		try:
			cursor.execute("SELECT COUNT(*) FROM `nodes`")
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit (1)
		row = cursor.fetchone ()
		numberRows = row[0]

		try:
			cursor.execute("SELECT `hostname` FROM `nodes` WHERE `nodeid` > '0'")
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit (1)

		row = cursor.fetchall ()
		print "-----------"		
		print "|HOSTNAMES|"
		print "-----------"
		for i in range(0, numberRows):
			print `i+1` + " " + `row[i]`
		sys.exit (1)
