#!/usr/bin/python
import collections
import MySQLdb, getopt, sys, optparse, re, array, os
from optparse import OptionParser
 
#################
# CONFIGURATION #
#################
 
# MySQL configuration
mysql_hostname = 'localhost'
mysql_database = 'puppet'
mysql_username = 'puppet'
mysql_password = 'puppet'
 
modules = ['*', 'apache', 'nagios', 'php', 'mysql', 'bind']
 
#############
# FUNCTIONS #
#############
 
# Function for checking correct IP address format
def ipFormatChk(ip):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, ip):
       return True
    else:
       return False
 
def getStatus(s):
	if (s == 0):
		return "cleared (0)"
	elif (s == -1):
		return "disabled (-1)"
	else:
		return "enabled (1)"
 
# Function to change the status of a module
def set_module(module, status):
	if (module == "*"):
		for m in modules:
			if m != "*":
				node['module_' + m] = int(status)
				print "Module " + m + " set to " + getStatus(status)
	else:
		found = False	
		for m in modules:
			if m == module:
				found = True
				node['module_' + m] = int(status)
				print "Module " + m + " set to " + getStatus(status)
				break
 
		if found == False:
			print_warning("Unknown module " + module)
 
# Function to print a warning
def print_warning(message):
	print "\033[33m[WARNING]\033[0m " + message
 
# Function to print an error
def print_error(message):
	print "\033[31m[ERROR]\033[0m " + message
 
# Function to fetch the domid of a domain
def getDomId(domain):
	try:
		cursor.execute("SELECT bind_domid FROM bind_domains WHERE domain = %s", (domain))
		row = cursor.fetchone()
	except MySQLdb.Error, e:
		print_error("%d: %s" % (e.args[0], e.args[1]))
		sys.exit(1)
 
	if cursor.rowcount > 0:
		return row[0]
	else:
		return 0
 
# Function to exit the script and update the configuration
def exitAndUpdate():
	os.system("/usr/local/bin/mysql-to-puppet.py")
	os.system("/usr/local/bin/mysql-to-nagios.py")
	sys.exit(0)
 
################
# START SCRIPT #
################
 
# Open MySQL connection
try:
	db = MySQLdb.connect(mysql_hostname, mysql_username, mysql_password, mysql_database)
except MySQLdb.Error, e:
	print_error("%d: %s" % (e.args[0], e.args[1]))
	sys.exit(1)
 
cursor = db.cursor()
 
# Menu with the different options that can be used to configure the Puppet database
usage = "usage: %prog -C -n <FQDN> -I <IP> -N <netmask> -G <gateway>\nusage: %prog -D -n <FQDN>\nusage: %prog -n <FQDN> [-e|-d|-c module] [-I IP] [-N netmask] [-G gateway]\nusage: %prog -n <FQDN> -M <module> [options]"
parser = OptionParser(usage = usage)
 
# Options
parser.add_option("-n", "--node", dest = "node", help = "FQDN of the node")
 
parser.add_option("-C", "--create", dest = "create", action = "store_true", help = "Create node", default = False)
parser.add_option("-D", "--delete", dest = "delete", action = "store_true", help = "Delete node", default = False)
parser.add_option("-I", "--ip", dest = "ip", help = "IP address")
parser.add_option("-N", "--netmask", dest = "netmask", help = "Netmask")
parser.add_option("-G", "--gateway", dest = "gateway", help = "Gateway")
 
parser.add_option("-M", "--module", dest="module", help = "Do something with a module, leave optionless for a list of options")
 
parser.add_option("-e", "--enable-module", dest = "enable_module", help = "Enables module for node: " + "|" . join(modules))
parser.add_option("-d", "--disable-module", dest = "disable_module", help = "Disables module for node: " + "|" . join(modules))
parser.add_option("-c", "--clear-module", dest = "clear_module", help = "Clears module for node: " + "|" . join(modules))
 
(options, args) = parser.parse_args()
 
# If the (required) -n (--node) was not given
if options.node == None:
	if len(sys.argv) > 1:
		print_error("Invalid options! Use -h (--help) for a list of options")
		print ""
 
	try:
		cursor.execute("SELECT nodeid, hostname, ip, module_apache, module_nagios, module_php, module_mysql, module_bind FROM nodes")
		result_set = cursor.fetchall()
	except MySQLdb.Error, e:
		print_error("%d: %s" % (e.args[0], e.args[1]))
		sys.exit(1)
 
	if cursor.rowcount > 0:
		print "NODE SUMMARY:\n\033[1m%4s %20s %19s %7s %7s %4s %6s %5s\033[0m" % ("#", "FQDN", "IP", "Apache", "Nagios", "PHP", "MySQL", "Bind")
		for row in result_set:
			print "%4s %20s %19s %7s %7s %4s %6s %5s" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
	else:
		print_warning("No nodes in database")
 
# Else if the -n (--node) was given
else:
	# If you want to create the node
	if options.create == True:
		if options.node != None and options.ip != None and options.netmask != None and options.gateway != None:
			# Check hostname format
			#if (hostnameFormatChk(options.node) == False):
				#print_error("Hostname argument is not a valid hostname ([a-z].[a-z].[a-z]{2,4})")
				#sys.exit(1)
 
			# Check IP address format
			if (ipFormatChk(options.ip) == False):
				print_error(options.ip + " is not a valid IP address!")
				sys.exit(1)
 
			# Check netmask address format
			if (ipFormatChk(options.netmask) == False):
				print_error(options.netmask + " is not a valid netmask!")
				sys.exit(1)
 
	 		# Check gateway address format
			if (ipFormatChk(options.gateway) == False):				
				print_error(options.gateway + " is not a valid gateway!")
				sys.exit (1)
 
	 		try:
				cursor.execute("INSERT INTO nodes (hostname, ip, netmask, gateway) VALUES (%s, %s, %s, %s)", (options.node, options.ip, options.netmask, options.gateway))
				print "Node " + options.node + " created"
				exitAndUpdate()
			except MySQLdb.Error, e:
				print_error("%d: %s" % (e.args[0], e.args[1]))
				sys.exit(1)
		else:
			print_error("Required arguments for -C (--create) parameter: -n (--node), -I (--ip-address), -N (--netmask), -G (--gateway)")
			sys.exit(1)
	# Else, do something with an existing node
	else:
		###############
		# SEARCH NODE #
		###############
 
		try:
			cursor.execute("SELECT * FROM nodes WHERE hostname = %s", options.node)
 
			row = cursor.fetchone()
 
			if cursor.rowcount > 0:
				# Create node dictionary
				node = { 'nodeid':row[0], 'hostname':row[1], 'ip':row[2], 'netmask':row[3], 'gateway':row[4], 'module_apache':row[5], 'module_nagios':row[6], 'module_php':row[7], 'module_mysql':row[8], 'module_bind':row[9] }
			else:
				print_error(options.node + " does not exist")
				sys.exit(1)
		except MySQLdb.Error, e:
			print_error("%d: %s" % (e.args[0], e.args[1]))
			sys.exit(1)
 
		################
		# NODE OPTIONS #
		################
 
		# Delete node
		if options.delete == True:
			try:
				# Delete the node
				cursor.execute("DELETE FROM nodes WHERE nodeid = %s", node['nodeid'])
 
				# Delete all the node's Virtual Hosts
				cursor.execute("DELETE FROM apache_virtualhosts WHERE nodeid = %s", node['nodeid'])
 
				# Delete all the node's domains
				cursor.execute("DELETE FROM bind_domains WHERE nodeid = %s", node['nodeid'])
				cursor.execute("DELETE FROM bind_subdomains WHERE nodeid = %s", node['nodeid'])
 
				print "Node " + node['hostname'] + " deleted"
				exitAndUpdate()
			except MySQLdb.Error, e:
				print_error("%d: %s" % (e.args[0], e.args[1]))
				sys.exit(1)
 
		elif options.module != None:
			##################
			# MODULE OPTIONS #
			##################
 
			# Make sure no summary is printed (see below)
			update_node = True
 
			# Module apache
			if options.module == "apache":
				# Check whether module apache is enabled
				if node['module_apache'] != 1:
					print_error("Module apache is not enabled for this node!")
					sys.exit(1)
 
				# Add Virtual Host	
				if len(sys.argv) > 6 and sys.argv[5] == "addvh" and sys.argv[6] != None:
					try:			
						cursor.execute("INSERT INTO apache_virtualhosts (nodeid, status, hostname) VALUES (%s, %s, %s)", (node['nodeid'], 1, sys.argv[6]))
						print "Virtual Host " + sys.argv[6] + " created"
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
				# Delete Virtual Host
				elif len(sys.argv) > 6 and sys.argv[5] == "deletevh" and sys.argv[6] != None:
					try:			
						cursor.execute("DELETE FROM apache_virtualhosts WHERE hostname = %s", (sys.argv[6]))
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
 
					if cursor.rowcount > 0:
						print "Virtual Host " + sys.argv[6] + " deleted"
					else:
						print "Could not find Virtual Host " + sys.argv[6]
						sys.exit(1)
				# Enable (1) Virtual Host
				elif len(sys.argv) > 6 and sys.argv[5] == "enablevh" and sys.argv[6] != None:
					try:
						cursor.execute("UPDATE apache_virtualhosts SET status = %s WHERE nodeid = %s AND hostname = %s", (1, node['nodeid'], sys.argv[6]))
					except MySQLdb.Error, e:
						print_error("%d, %s" % (e.args[0], e.args[1]))
 
					if cursor.rowcount > 0:
						print "Virtual Host " + sys.argv[6] + " enabled"
					else:
						print_error("Could not find Virtual Host " + sys.argv[6])
						sys.exit(1)
				# Disable (0) Virtual Host
				elif len(sys.argv) > 6 and sys.argv[5] == "disablevh" and sys.argv[6] != None:
					try:
						cursor.execute("UPDATE apache_virtualhosts SET status = %s WHERE nodeid = %s AND hostname = %s", (0, node['nodeid'], sys.argv[6]))
					except MySQLdb.Error, e:
						print_error("%d, %s" % (e.args[0], e.args[1]))
 
					if cursor.rowcount > 0:
						print "Virtual Host " + sys.argv[6] + " disabled"
					else:
						print_error("Could not find Virtual Host " + sys.argv[6])
						sys.exit(1)
				# Else, print help message
				else:
					print_error("Invalid option for module apache!\nOptions are:\n\taddvh <hostname>\n\tdeletevh <hostname>\n\tenablevh <hostname>\n\tdisablevh <hostname>")
					sys.exit(1)
 
				exitAndUpdate()
 
			# Module bind
			elif options.module == "bind":
				# Check whether module bind is enabled
				if node['module_bind'] != 1:
					print_error("Module bind is not enabled for this node!")
					sys.exit(1)
 
				# Add domain
				if len(sys.argv) > 6 and sys.argv[5] == "adddomain" and sys.argv[6] != None:
					try:			
						cursor.execute("INSERT INTO bind_domains (nodeid, status, domain) VALUES (%s, %s, %s)", (node['nodeid'], 1, sys.argv[6]))
						print "Domain " + sys.argv[6] + " created"
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
				# Add subdomain to domain
				elif len(sys.argv) > 8 and sys.argv[5] == "addsubdomain" and sys.argv[6] != None and sys.argv[7] != None and sys.argv[8] != None:
					if (ipFormatChk(sys.argv[8]) == False):
						print_error(sys.argv[8] + " is not a valid IP address!")
						sys.exit(1)
 
					domid = getDomId(sys.argv[6])
					if domid == 0:
						print_error("Could not find domain " + sys.argv[6])
						sys.exit(1)
 
					try:			
						cursor.execute("INSERT INTO bind_subdomains (bind_domid, nodeid, status, hostname, ip) VALUES (%s, %s, %s, %s, %s)", (domid, node['nodeid'], 1, sys.argv[7], sys.argv[8]))
						print "Subdomain " + sys.argv[7] + " for domain " + sys.argv[6] + " created"
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
				# Delete domain
				elif len(sys.argv) > 6 and sys.argv[5] == "deletedomain" and sys.argv[6] != None:
					domid = getDomId(sys.argv[6])
					if domid == 0:
						print_error("Could not find domain " + sys.argv[6])
						sys.exit(1)
 
					try:			
						cursor.execute("DELETE FROM bind_domains WHERE domain = %s", (sys.argv[6]))
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
 
					if cursor.rowcount > 0:
						print "Domain " + sys.argv[6] + " deleted"
					else:
						print_error("Could not find domain " + sys.arvg[4])
						sys.exit(1)
 
					try:			
						cursor.execute("DELETE FROM bind_subdomains WHERE bind_domid = %s", (domid))
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
 
					if cursor.rowcount > 0:
						print "Subdomains of domain " + sys.argv[6] + " deleted"
					else:
						print_error("Could not find domain " + sys.arvg[6])
						sys.exit(1)
				# Delete subdomain from domain
				elif len(sys.argv) > 7 and sys.argv[5] == "deletesubdomain" and sys.argv[6] != None and sys.argv[7] != None:
					domid = getDomId(sys.argv[6])
					if domid == 0:
						print "Could not find domain " + sys.argv[6]
						sys.exit(1)
 
					try:			
						cursor.execute("DELETE FROM bind_subdomains WHERE bind_domid = %s AND hostname = %s", (domid, sys.argv[7]))
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
 
					if cursor.rowcount > 0:
						print "Subdomain " + sys.argv[7] + " of domain " + sys.argv[6] + " deleted"
					else:
						print_error("Could not find subdomain " + sys.argv[7] + " for domain " + sys.argv[6])
						sys.exit(1)
				# Enable (1) domain
				elif len(sys.argv) > 6 and sys.argv[5] == "enabledomain" and sys.argv[6] != None:
					try:
						cursor.execute("UPDATE bind_domains SET status = 1 WHERE nodeid = %s AND domain = %s", (node['nodeid'], sys.argv[6]))
					except MySQLdb.Error, e:
						print_error("%d, %s" % (e.args[0], e.args[1]))
 
					if cursor.rowcount > 0:
						print "Domain " + sys.argv[6] + " enabled"
					else:
						print_error("Could not find domain " + sys.argv[4])
				# Enable (1) subdomain of domain
				elif len(sys.argv) > 7 and sys.argv[5] == "enablesubdomain" and sys.argv[6] != None and sys.argv[7] != None:
					domid = getDomId(sys.argv[6])
					if domid == 0:
						print "Could not find domain " + sys.argv[6]
						sys.exit(1)
 
					try:
						cursor.execute("UPDATE bind_subdomains SET status = 1 WHERE bind_domid = %s AND hostname = %s", (domid, sys.argv[7]))
					except MySQLdb.Error, e:
						print_error("%d, %s" % (e.args[0], e.args[1]))
						sys.exit(1)
 
					if cursor.rowcount > 0:
						print "Subdomain " + sys.argv[7] + " of domain " + sys.argv[6] + " deleted"
					else:
						print_error("Could not find subdomain " + sys.argv[7] + " for domain " + sys.argv[6])
						sys.exit(1)
				# Disable (0) domain
				elif len(sys.argv) > 6 and sys.argv[5] == "disabledomain" and sys.argv[6] != None:
					try:
						cursor.execute("UPDATE bind_domains SET status = 0 WHERE nodeid = %s AND domain = %s", (node['nodeid'], sys.argv[6]))
					except MySQLdb.Error, e:
						print_error("%d, %s" % (e.args[0], e.args[1]))
 
					if cursor.rowcount > 0:
						print "Domain " + sys.argv[6] + " disabled"
					else:
						print_error("Could not find domain " + sys.argv[4])
				# Disable (0) subdomain of domain
				elif len(sys.argv) > 7 and sys.argv[5] == "disablesubdomain" and sys.argv[6] != None and sys.argv[7] != None:
					domid = getDomId(sys.argv[6])
					if domid == 0:
						print "Could not find domain " + sys.argv[6]
						sys.exit(1)
 
					try:
						cursor.execute("UPDATE bind_subdomains SET status = -1 WHERE bind_domid = %s AND hostname = %s", (domid, sys.argv[7]))
					except MySQLdb.Error, e:
						print_error("%d, %s" % (e.args[0], e.args[1]))
						sys.exit(1)
 
					if cursor.rowcount > 0:
						print "Subdomain " + sys.argv[7] + " of domain " + sys.argv[6] + " disabled"
					else:
						print_error("Could not find subdomain " + sys.argv[7] + " for domain " + sys.argv[6])
						sys.exit(1)
				else:
					print_error("Invalid option for module bind!\nOptions are:\n\tadddomain <domain>\n\taddsubdomain <domain> <hostname> <ip>\n\tdeletedomain <domain>\n\tdeletesubdomain <domain> <hostname>\n\tenabledomain <domain>\n\tenablesubdomain <domain> <hostname>\n\tdisabledomain <domain>\n\tdisablesubdomain <domain> <hostname>")
					sys.exit(1)
 
				exitAndUpdate()
			else:
				print_error("Invalid module " + options.module + " or module has no options! Try apache or bind.")
				sys.exit(1)		
		else:
			###############		
			# UPDATE NODE #
			###############
 
			# Boolean to check whether a node update (IP, netmask, gateway, enable a module, disable a module, clear a module) was requested
			update_node = False
 
			# Check IP address format
			if options.ip != None:
				if (ipFormatChk(options.ip) == False):
					print_error(options.ip + " is not a valid IP address!")
					sys.exit(1)
				else:
					update_node = True
					node['ip'] = options.ip
 
			# Check netmask address format
			if options.netmask != None:
				if (ipFormatChk(options.netmask) == False):
					print_error(options.netmask + " is not a valid netmask!")
					sys.exit(1)
				else:
					update_node = True
					node['netmask'] = options.netmask
 
	 		# Check gateway address format
	 		if options.gateway != None:
				if (ipFormatChk(options.gateway) == False):				
					print_error(options.gateway + " is not a valid gateway!")
					sys.exit(1)
				else:
					update_node = True
					node['gateway'] = options.gateway
 
			if options.enable_module != None:
				update_node = True
				set_module(options.enable_module, 1)					
			elif options.disable_module != None:
				update_node = True
				set_module(options.disable_module, -1)
			elif options.clear_module != None:
				update_node = True
				set_module(options.clear_module, 0)
 
			if update_node == True:
				try:
					cursor.execute("UPDATE nodes SET hostname = %s, ip = %s, netmask = %s, gateway = %s, module_apache = %s, module_nagios = %s, module_php = %s, module_mysql = %s, module_bind = %s WHERE nodeid = %s", (node['hostname'], node['ip'], node['netmask'], node['gateway'], node['module_apache'], node['module_nagios'], node['module_php'], node['module_mysql'], node['module_bind'], node['nodeid']))
					print "Node " + node['hostname'] + " updated"
					exitAndUpdate()
				except MySQLdb.Error, e:
					print_error("%d: %s" % (e.args[0], e.args[1]))
					sys.exit(1)
 
		##############
		# NO OPTIONS #
		##############
 
		# If no options were given, print a node summary
		if update_node == False:
			print "#" * (len(node['hostname']) + 4)
			print "# \033[1m" + node['hostname'].upper() + "\033[0m #"
			print "#" * (len(node['hostname']) + 4)
			print ""
			print "IP address: " + node['ip']
			print "Netmask: " + node['netmask']
			print "Gateway: " + node['gateway']
			print ""
			print "Module apache: " + getStatus(node['module_apache'])
			print "Module nagios: " + getStatus(node['module_nagios'])
			print "Module php: " + getStatus(node['module_php'])
			print "Module mysql: " + getStatus(node['module_mysql'])
			print "Module bind: " + getStatus(node['module_bind'])
 
			if node['module_apache'] == 1:
				print ""
				print "APACHE VIRTUAL HOSTS:"
 
				try:
					cursor.execute("SELECT apache_vhid, status, hostname FROM apache_virtualhosts WHERE nodeid = %s ORDER BY hostname", node['nodeid'])
					result_set = cursor.fetchall()
				except MySQLdb.Error, e:
					print_error("%d: %s" % (e.args[0], e.args[1]))
					sys.exit(1)
 
				if cursor.rowcount > 0:
					print "\033[1m%5s %20s %10s\033[0m" % ("#", "Hostname", "Status")
					for row in result_set:
						print "%5s %20s %10s" % (row[0], row[2], row[1])
				else:
					print "0 Virtual Hosts for this node"
 
			if node['module_bind'] == 1:
				print ""
				print "BIND DOMAINS:"
 
				try:
					cursor.execute("SELECT bind_domid, status, domain FROM bind_domains WHERE nodeid = %s ORDER BY domain", node['nodeid'])
					result_set = cursor.fetchall()
				except MySQLdb.Error, e:
					print_error("%d: %s" % (e.args[0], e.args[1]))
					sys.exit(1)
 
				if cursor.rowcount > 0:
					print "\033[1m%5s %20s %10s\033[0m" % ("#", "Domain", "Status")
					for row in result_set:
						print "%5s %20s %10s" % (row[0], row[2], row[1])
 
					print ""
					print "BIND SUBDOMAINS:"
					try:
						cursor.execute("SELECT bind_subdomid, domain, bsd.status, hostname, ip FROM bind_subdomains AS bsd LEFT JOIN bind_domains USING (bind_domid) WHERE bsd.nodeid = %s ORDER BY domain, hostname", node['nodeid'])
						result_set = cursor.fetchall()
					except MySQLdb.Error, e:
						print_error("%d: %s" % (e.args[0], e.args[1]))
						sys.exit(1)
 
					if cursor.rowcount > 0:
						print "\033[1m%5s %20s %20s %20s %10s\033[0m" % ("#", "Domain", "Hostname", "IP", "Status")
						for row in result_set:
							print "%5s %20s %20s %20s %10s" % (row[0], row[1], row[3], row[4], row[2])
					else:
						print "0 subdomains for this node"
				else:
					print "0 domains for this node"
 
# Close MySQL connection
db.close()
