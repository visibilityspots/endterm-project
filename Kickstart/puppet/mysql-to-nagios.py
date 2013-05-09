#!/usr/bin/python
import sys
import MySQLdb
 
# Nagios configuration
nagios_hosts = '/etc/puppet/modules/nagios/files/hosts.cfg'
nagios_hostgroups = '/etc/puppet/modules/nagios/files/hostgroups.cfg'
nagios_services = '/etc/puppet/modules/nagios/files/services.cfg'
 
# MySQL configuration
mysql_hostname = 'localhost'
mysql_database = 'puppet'
mysql_username = 'puppet'
mysql_password = 'puppet'
 
# Create lists
servers = []
webservers = []
mysqlservers = []
dnsservers = []
 
# Open MySQL connection
try:
	dbconn = MySQLdb.connect(mysql_hostname, mysql_username, mysql_password, mysql_database)
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit(1)
 
# Open hosts.cfg
f = open(nagios_hosts, 'w')
 
# Write host "google" for checking the internet connection
f.write("define host{\n\thost_name\tgoogle\n\talias\t\tInternet Connection\n\taddress\t\twww.google.com\n\tuse\t\tgeneric-host\n\t}\n\n")
 
cursor = dbconn.cursor()
cursor.execute("SELECT nodeid, hostname, ip, module_apache, module_mysql, module_bind FROM nodes")
nodes = cursor.fetchall()
for node in nodes:
	f.write("define host{\n\thost_name\t" + node[1] + "\n\talias\t\t" + node[1] + "\n\taddress\t\t" + node[2] + "\n\tuse\t\tgeneric-host\n\t}\n\n")
 
	# Add to servers list
	servers.append(node[1])
 
	# Check for module "apache"
	if (node[3] == 1):
		webservers.append(node[1])
 
	# Check for module "mysql"
	if (node[4] == 1):
		mysqlservers.append(node[1])
 
	# Check for module "bind"
	if (node[5] == 1):
		dnsservers.append(node[1])	
 
cursor.close()
 
# Close hosts.cfg
f.close()
 
# Close MySQL connection
dbconn.close()
 
# Open hostgroups.cfg
f = open(nagios_hostgroups, 'w')
 
# Write hostgroup "all"
f.write("define hostgroup{\n\thostgroup_name\tall\n\talias\t\tAll Servers\n\tmembers\t\t*\n\t}\n\n")
 
# Write all servers
if (len(servers) > 0):	
	f.write("define hostgroup{\n\thostgroup_name\tservers\n\talias\t\tServers\n\tmembers\t\t")
	f.write(",".join(servers))
	f.write("\n\t}\n\n")
 
# Write all webservers
if (len(webservers) > 0):	
	f.write("define hostgroup{\n\thostgroup_name\twebservers\n\talias\t\tWebservers\n\tmembers\t\t")
	f.write(",".join(webservers))
	f.write("\n\t}\n\n")
 
# Write all mysqlservers
if (len(mysqlservers) > 0):	
	f.write("define hostgroup{\n\thostgroup_name\tmysqlservers\n\talias\t\tMySQL Servers\n\tmembers\t\t")
	f.write(",".join(mysqlservers))
	f.write("\n\t}\n\n")
 
# Write all dnsservers
if (len(dnsservers) > 0):	
	f.write("define hostgroup{\n\thostgroup_name\tdnsservers\n\talias\t\tDNS Servers\n\tmembers\t\t")
	f.write(",".join(dnsservers))
	f.write("\n\t}\n\n")
 
# Close hostgroups.cfg
f.close()
 
# Open services.cfg
f = open(nagios_services, 'w')
 
# Write service "ping" for all servers
f.write("define service{\n\thostgroup_name\t\t\tall\n\tservice_description\t\tPING\n\tcheck_command\t\t\tcheck_ping!100.0,20%!500.0,60%\n\tuse\t\t\t\tgeneric-service\n\tnotification_interval\t\t0\n\t}\n\n")
 
# Write service "ssh" if necessary
if (len(servers) > 0):
	f.write("define service{\n\thostgroup_name\t\t\tservers\n\tservice_description\t\tSSH\n\tcheck_command\t\t\tcheck_ssh\n\tuse\t\t\t\tgeneric-service\n\tnotification_interval\t\t0\n\t}\n\n")
 
# Write service "http" if necessary
if (len(webservers) > 0):
	f.write("define service{\n\thostgroup_name\t\t\twebservers\n\tservice_description\t\tHTTP\n\tcheck_command\t\t\tcheck_http\n\tuse\t\t\t\tgeneric-service\n\tnotification_interval\t\t0\n\t}\n\n")
 
# Write service "mysql" if necessay
if (len(mysqlservers) > 0):
	f.write("define service{\n\thostgroup_name\t\t\tmysqlservers\n\tservice_description\t\tMySQL\n\tcheck_command\t\t\tcheck_mysql\n\tuse\t\t\t\tgeneric-service\n\tnotification_interval\t\t0\n\t}\n\n")
 
# Write service "dns" if necessay
if (len(dnsservers) > 0):
	f.write("define service{\n\thostgroup_name\t\t\tdnsservers\n\tservice_description\t\tDNS\n\tcheck_command\t\t\tcheck_dns\n\tuse\t\t\t\tgeneric-service\n\tnotification_interval\t\t0\n\t}\n\n")
 
# Close services.cfg
f.close()
