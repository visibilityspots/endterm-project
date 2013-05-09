CREATE TABLE IF NOT EXISTS `apache_virtualhosts` (
  `apache_vhid` int(11) NOT NULL AUTO_INCREMENT,
  `nodeid` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `hostname` varchar(80) NOT NULL,
  PRIMARY KEY (`apache_vhid`),
  UNIQUE KEY `nodeid` (`nodeid`,`hostname`)
);
 
CREATE TABLE IF NOT EXISTS `bind_domains` (
  `bind_domid` int(11) NOT NULL AUTO_INCREMENT,
  `nodeid` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `domain` varchar(80) NOT NULL,
  PRIMARY KEY (`bind_domid`),
  UNIQUE KEY `nodeid` (`nodeid`,`domain`)
);
 
CREATE TABLE IF NOT EXISTS `bind_subdomains` (
  `bind_subdomid` int(11) NOT NULL AUTO_INCREMENT,
  `bind_domid` int(11) NOT NULL,
  `nodeid` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `hostname` varchar(80) NOT NULL,
  `ip` varchar(15) NOT NULL,
  PRIMARY KEY (`bind_subdomid`)
  UNIQUE KEY `bind_domid` (`bind_domid`,`nodeid`,`hostname`)
);
 
CREATE TABLE IF NOT EXISTS `nodes` (
  `nodeid` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(80) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `netmask` varchar(15) NOT NULL,
  `gateway` varchar(15) NOT NULL,
  `module_apache` tinyint(1) DEFAULT '0',
  `module_nagios` tinyint(1) DEFAULT '0',
  `module_php` tinyint(1) DEFAULT '0',
  `module_mysql` tinyint(1) DEFAULT '0',
  `module_bind` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`nodeid`),
  UNIQUE KEY `hostname` (`hostname`)

