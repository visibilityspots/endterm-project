#!/bin/bash
##############################
# Puppet slave installation  #
##############################
 
backtitle="Puppet slave configuration"
 
# Temporarily file to read answers from dialog 
answer=`mktemp`
 
dialog --sleep 1 --backtitle "$backtitle" --infobox "Starting Puppet configuration" 3 33
 
# Puppet slave network settings
dialog --backtitle "$backtitle" --nocancel --inputbox "IP address of this Puppet slave:" 8 36 2> $answer
ipslave=`cat ${answer}`
dialog --backtitle "$backtitle" --nocancel --inputbox "Netmask of this Puppet slave:" 8 33 "255.255.255.0" 2> $answer
nmslave=`cat ${answer}`
dialog --backtitle "$backtitle" --nocancel --inputbox "Gateway of this Puppet slave:" 8 33 2> $answer
gwslave=`cat ${answer}`
echo -e "auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\n\taddress ${ipslave}\n\tnetmask ${nmslave}\n\tgateway ${gwslave}" > /etc/network/interfaces
dialog --backtitle "$backtitle" --nocancel --inputbox "Nameserver(s) of this Puppet master (seperated by ,):" 8 60 2> $answer
nameservers=`cat $answer | tr --delete ' ' | tr ',' "\n"`
echo -n "" > /etc/resolv.conf
for ns in $nameservers; do
	echo "nameserver $ns" >> /etc/resolv.conf
done
dialog --backtitle "$backtitle" --nocancel --inputbox "FQDN of this Puppet slave:\nThis may NOT BE 'puppet.something'" 9 40 2> $answer
fqdnslave=`cat ${answer}`
hostname $fqdnslave
echo $fqdnslave > /etc/hostname
hostslave=`echo ${fqdnslave} | cut -d '.' -f 1`
echo -e "\n127.0.0.1\t${fqdnslave} ${hostslave}" >> /etc/hosts
 
# Puppet slave master information
dialog --backtitle "$backtitle" --nocancel --inputbox "IP address of Puppet master:" 8 32 2> $answer
ipmaster=`cat ${answer}`
dialog --backtitle "$backtitle" --nocancel --inputbox "FQDN of Puppet master:" 8 30 2> $answer
fqdnmaster=`cat ${answer}`
hostmaster=`echo ${fqdnmaster} | cut -d '.' -f 1`
echo -e "${ipmaster}\t${fqdnmaster} ${hostmaster} puppet" >> /etc/hosts
echo -e "\n[puppetd]" >> /etc/puppet/puppet.conf
echo "server=${fqdnmaster}" >> /etc/puppet/puppet.conf
chmod 700 /etc/puppet
 
# Set up Puppet configuration
sed -i "s/^pluginsync=.*$/pluginsync = false/" /etc/puppet/puppet.conf
 
# Wait for signed certificate
dialog --sleep 1 --backtitle "$backtitle" --infobox "Starting Puppet daemon" 3 26
puppetd &
dialog --backtitle "$backtitle" --msgbox "       Press < OK > when the Puppet administrator signed the certificate." 6 41
 
dialog --backtitle "$backtitle" --nocancel --pause "Puppet slave configuration complete" 8 40 5
