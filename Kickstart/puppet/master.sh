#!/bin/bash
##############################
# Puppet master installation #
##############################
 
backtitle="Puppet master configuration"
 
# Temporarily file to read answers from dialog 
answer=`mktemp`
 
dialog --sleep 1 --backtitle "$backtitle" --infobox "Starting Puppet configuration" 3 33
 
# Puppet master network settings
dialog --backtitle "$backtitle" --nocancel --inputbox "IP address of this Puppet master:" 8 37 2> $answer
ipmaster=`cat ${answer}`
dialog --backtitle "$backtitle" --nocancel --inputbox "Netmask of this Puppet master:" 8 34 "255.255.255.0" 2> $answer
nmmaster=`cat ${answer}`
dialog --backtitle "$backtitle" --nocancel --inputbox "Gateway of this Puppet master:" 8 34 2> $answer
gwmaster=`cat ${answer}`
echo -e "auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\n\taddress ${ipmaster}\n\tnetmask ${nmmaster}\n\tgateway ${gwmaster}" > /etc/network/interfaces
dialog --backtitle "$backtitle" --nocancel --inputbox "Nameserver(s) of this Puppet master (seperated by ,):" 8 60 2> $answer
nameservers=`cat $answer | tr --delete ' ' | tr ',' "\n"`
echo -n "" > /etc/resolv.conf
for ns in $nameservers; do
	echo "nameserver $ns" >> /etc/resolv.conf
done
dialog --backtitle "$backtitle" --nocancel --inputbox "FQDN of this Puppet master:" 8 40 2> $answer
fqdnmaster=`cat ${answer}`
hostname $fqdnmaster
echo $fqdnmaster > /etc/hostname
hostmaster=`echo ${fqdnmaster} | cut -d '.' -f 1`
echo -e "\n127.0.0.1\t${fqdnmaster} ${hostmaster} puppet" >> /etc/hosts
 
# Copy Puppet configuration
dialog --sleep 1 --backtitle "$backtitle" --infobox "Copying Puppet configuration" 3 32
cp -R /media/cdrom/puppet/manifests /etc/puppet/
cp -R /media/cdrom/puppet/modules /etc/puppet/
cp -R /media/cdrom/puppet/templates /etc/puppet/
chmod 700 /etc/puppet
chown puppet:puppet /etc/puppet
 
# Set up Puppet configuration
dialog --sleep 1 --backtitle "$backtitle" --infobox "Setting up Puppet configuration" 3 35
sed -i "s/^templatedir=.*$/templatedir=\/etc\/puppet\/templates/" /etc/puppet/puppet.conf
sed -i "s/^pluginsync=.*$/pluginsync=false/" /etc/puppet/puppet.conf
nsline=""
for ns in $nameservers; do
	nsline="${nsline}\"${ns}\", "
done
nsline=`echo $nsline | sed 's/,$//'`
sed -i "s/^.*\$nameservers = \[\]$/\t\$nameservers = [${nsline}]/" /etc/puppet/manifests/templates.pp
sed -i "s/^.*\$forwarders = \[\]$/\t\$forwarders = [${nsline}]/" /etc/puppet/modules/bind/manifests/init.pp
 
# Set up MySQL
dialog --sleep 1 --backtitle "$backtitle" --infobox "Setting up MySQL" 3 20
/etc/init.d/mysql start
dialog --backtitle "$backtitle" --nocancel --inputbox "Database name:" 8 37 "puppet" 2> $answer
dbname=`cat ${answer}`
/usr/bin/mysqladmin create $dbname
/usr/bin/mysql $dbname < /media/cdrom/puppet/puppet.sql
dialog --backtitle "$backtitle" --nocancel --inputbox "Database username:" 8 37 "puppet" 2> $answer
dbuser=`cat ${answer}`
dialog --backtitle "$backtitle" --nocancel --insecure --passwordbox "Database password:" 8 37 "puppet" 2> $answer
dbpass=`cat ${answer}`
echo "CREATE USER '${dbuser}'@'localhost' IDENTIFIED BY '${dbpass}';" | /usr/bin/mysql
echo "GRANT SELECT, INSERT, UPDATE, DELETE ON ${dbname}.* TO '${dbuser}'@'localhost';" | /usr/bin/mysql
/usr/bin/mysqladmin flush-privileges
dialog --backtitle "$backtitle" --nocancel --insecure --passwordbox "MySQL root password:" 8 30 "\$\$32Puppet" 2> $answer
mysqlpass=`cat ${answer}`
/usr/bin/mysqladmin -u root password "$mysqlpass"
 
# Copy scripts
dialog --sleep 1 --backtitle "$backtitle" --infobox "Copying scripts" 3 19
cp /media/cdrom/puppet/mysql-to-puppet.py /media/cdrom/puppet/mysql-to-nagios.py /media/cdrom/puppet/puppetman.py /usr/local/bin/
chmod 700 /usr/local/bin/mysql-to-puppet.py /usr/local/bin/mysql-to-nagios.py /usr/local/bin/puppetman.py
sed -i "s/^mysql_database =.*$/mysql_database = '${dbname}'/" /usr/local/bin/mysql-to-puppet.py
sed -i "s/^mysql_username =.*$/mysql_username = '${dbuser}'/" /usr/local/bin/mysql-to-puppet.py
sed -i "s/^mysql_password =.*$/mysql_password = '${dbpass}'/" /usr/local/bin/mysql-to-puppet.py
sed -i "s/^mysql_database =.*$/mysql_database = '${dbname}'/" /usr/local/bin/mysql-to-nagios.py
sed -i "s/^mysql_username =.*$/mysql_username = '${dbuser}'/" /usr/local/bin/mysql-to-nagios.py
sed -i "s/^mysql_password =.*$/mysql_password = '${dbpass}'/" /usr/local/bin/mysql-to-nagios.py
sed -i "s/^mysql_database =.*$/mysql_database = '${dbname}'/" /usr/local/bin/puppetman.py
sed -i "s/^mysql_username =.*$/mysql_username = '${dbuser}'/" /usr/local/bin/puppetman.py
sed -i "s/^mysql_password =.*$/mysql_password = '${dbpass}'/" /usr/local/bin/puppetman.py
 
dialog --backtitle "$backtitle" --nocancel --pause "Puppet master configuration completed" 8 41 5
