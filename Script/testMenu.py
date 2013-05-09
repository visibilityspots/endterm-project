#!/usr/bin/python
import MySQLdb, getopt, sys, optparse
#mysql connect info
db = MySQLdb.connect(host="localhost", user="root", passwd="pek", db="puppet")
cursor = db.cursor()

from optparse import OptionParser
def main():
        parser=OptionParser()
         # Options
        parser.add_option("-H", "--hostname",dest="hostname",help="Enter hostname")
        parser.add_option("-I", "--ip",dest="ip",help="Enter hostname")
        parser.add_option("-A", "--apache",dest="apache",default="0",help="enter 1 to enable apache or enter 0 to disable appache")
        parser.add_option("-M", "--mysql",dest="mysql",default="0",help="enter 1 to enable mysql or enter 0 to disable mysql")
        parser.add_option("-D", "--dns",dest="dns",default="0",help="enter 1 to enable dns or enter 0 to disable dns")
        parser.add_option("-P", "--postfix",dest="postfix",default="0",help="enter 1 to enable postfix or enter 0 to disable postfix")
        parser.add_option("-N", "--nagios",dest="nagios",default ="0",help="enter 1 to enable nagios or enter 0 to disable nagios")
 
 
        (options,args)=parser.parse_args()
        if options.nagios=="1":
                options.apache ="1"
                print "apache is required and will be installed"
        print options.hostname
        print options.ip
        print options.apache
        print options.mysql
        print options.dns
        print options.postfix
        print options.nagios
        #cursor.execute("INSERT INTO `puppet`.`nodes` (`node`,`ip`,`mod_apache`,`mod_mysql`,`mod_dns`,`mod_postfix`,`mod_nagios`)VALUES (%s, %s, %s, %s, %s, %s, %s)",(options.hostname,options.ip,options.apache,options.mysql,options.dns,options.postfix,options.nagios))
 
if __name__ == "__main__":
     main()
