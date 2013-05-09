#!/usr/bin/python
import sys
import MySQLdb
import time
 
# Puppet configuration
puppet_nodes = '/etc/puppet/manifests/mysql_nodes.pp'
bind_db = '/etc/puppet/modules/bind/files/db/'
 
# MySQL configuration
mysql_hostname = 'localhost'
mysql_database = 'puppet'
mysql_username = 'puppet'
mysql_password = 'puppet'
 
# Open MySQL connection
try:
	dbconn = MySQLdb.connect(mysql_hostname, mysql_username, mysql_password, mysql_database)
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)
 
# Open nodes.pp
f = open(puppet_nodes, 'w')
now = time.localtime()
f.write("# Generated on " + str(now.tm_mday) + "/" + str(now.tm_mon) + "/" + str(now.tm_year) + " " + str(now.tm_hour) + ":" + str(now.tm_min) + "\n\n")
 
cursor = dbconn.cursor()
cursor.execute("SELECT nodeid, hostname, ip, netmask, gateway, module_apache, module_nagios, module_php, module_mysql, module_bind FROM nodes")
nodes = cursor.fetchall()
for node in nodes:
	f.write("node '" + node[1] + "' {\n")
	f.write("\t$ip = \"" + node[2] + "\"\n")
	f.write("\t$netmask = \"" + node[3] + "\"\n")
	f.write("\t$gateway = \"" + node[4] + "\"\n")
	f.write("\tinclude baseclass\n\n")
 
	# Check for module "apache"
	if (node[5] == 1):
		f.write("\tinclude apache\n")
 
		# Check for module "nagios"
		if (node[6] == 1):
			f.write("\tinclude nagios\n")
		elif (node[6] == -1):
			f.write("\t$nonagios = true\n")
			f.write("\tinclude nagios\n")
 
		# Check for module "php"
		if (node[7] == 1):
			f.write("\tinclude php\n")
		elif (node[7] == -1):
			f.write("\t$nophp = true\n")
			f.write("\tinclude php\n")
 
		# Search for all Virtual Hosts
		cursor.execute("SELECT apache_vhid, status, hostname FROM apache_virtualhosts WHERE nodeid = " + str(node[0]))
		virtualhosts = cursor.fetchall()
		for vh in virtualhosts:
			f.write("\tapache::virtual_host { \"" + vh[2] + "\":\n")
			if (vh[1] == 1):
				f.write("\t\tensure => \"present\",\n")
			elif (vh[1] == -1):
				f.write("\t\tensure => \"absent\",\n")
			else:
				f.write("\t\tensure => \"disabled\",\n")
			f.write("\t}\n")
	elif (node[5] == -1):
		f.write("\t$noapache = true\n")
		f.write("\tinclude apache\n")
 
		# If module "nagios" is enabled/disabled, disable it
		if (node[6] == 1 or node[6] == -1):
			f.write("\t$nonagios = true\n")
			f.write("\tinclude nagios\n")
 
		# If module "php" is enabled/disabled, disable it
		if (node[7] == 1 or node[7] == -1):
			f.write("\t$nophp = true\n")
			f.write("\tinclude php\n")
 
	# Check for module "mysql"
	if (node[8] == 1):
		f.write("\tinclude mysql\n")
	elif (node[8] == -1):
		f.write("\t$nomysql = true\n")
		f.write("\tinclude mysql\n")
 
	# Check for module "bind"
	if (node[9] == 1):		
		# Search for all domains
		cursor.execute("SELECT bind_domid, status, domain FROM bind_domains WHERE nodeid = " + str(node[0]))
		domains = cursor.fetchall()
		if (len(domains) > 0):
			f.write("\n\t$domains = [")
			i = 1;
			for domain in domains:
				if (i == len(domains)):
					f.write("\"" + domain[2] + "\"")
				else:
					f.write("\"" + domain[2] + "\", ")
 
				i = i + 1
 
				# Create db files for this domain
				dbf = open(bind_db + "db." + domain[2], 'w')
				dbf.write("$TTL		604800\n")
				dbf.write("@		IN	SOA	ns." + domain[2] + ". root." + domain[2] + ". (\n")
				dbf.write("				1\n")
				dbf.write("				604800\n")
				dbf.write("				86400\n")
				dbf.write("				2419200\n")
				dbf.write("				604800 )\n\n")
				dbf.write("@		IN	NS	ns." + domain[2] + ".\n")
				cursor.execute("SELECT bind_subdomid, status, hostname, ip FROM bind_subdomains WHERE status = 1 AND bind_domid = " + str(domain[0]))
				subdomains = cursor.fetchall()
				for subdomain in subdomains:
					dbf.write(subdomain[2] + "		IN	A	" + subdomain[3] + "\n")
				dbf.close()
 
			f.write("]\n")	
 
			f.write("\tinclude bind\n")
		for domain in domains:
			f.write("\tbind::domain { \"" + domain[2] + "\":\n")
			if (domain[1] == 1):
				f.write("\t\tensure => \"present\",\n")
			else:
				f.write("\t\tensure => \"absent\",\n")
			f.write("\t}\n")
	elif (node[9] == -1):
		f.write("\n\t$nobind = true\n")
		f.write("\tinclude bind\n")
 
	f.write("}\n\n")
 
cursor.close()
 
# Close nodes.pp
f.close()
 
# Close MySQL connection
dbconn.close()
