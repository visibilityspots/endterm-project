class nagios {
	$packagelist = ["nagios2", "nagios-plugins", "nagios-images", "nagios2-common"]
	
	if $nonagios {
		package { $packagelist:
			ensure	=> "purged"
		}
		
		user { "nagios":
			ensure	=> "absent"
		}
		
		group { "nagios":
			ensure	=> "absent",
			require	=> User["nagios"]
		}
		
		file { "/etc/nagios2":
			ensure	=> "absent",
			recurse	=> "true",
			force	=> "true"
		}
		
		file { "/var/cache/nagios2":
			ensure	=> "absent",
			recurse	=> "true",
			force	=> "true"
		}
		
		file { "/etc/apache2/conf.d/nagios2.conf":
			ensure	=> "absent"
		}
	} else {
		package { $packagelist:
			ensure	=> "installed",
		}
	
		group { "nagios":
			ensure	=> "present",
			require	=> Package["nagios2"]
		}
	
		user { "nagios":
			ensure		=> "present",
			gid		=> "nagios",
			comment		=> "Nagios Server",
			home		=> "/var/run/nagios2",
			shell		=> "/bin/false",
			require		=> Group["nagios"]
		}
		
		file { "/etc/nagios2":
			ensure		=> "directory",
			require		=> User["nagios"]
		}
		
		file { "/etc/nagios2/mysite":
			ensure		=> "directory",
			require		=> File["/etc/nagios2"]
		}
		
		file { "/etc/nagios2/mysite/contacts.cfg":
			ensure		=> "present",
			source		=> "puppet:///nagios/contacts.cfg",
			notify		=> Service["nagios2"],
			require		=> File["/etc/nagios2/mysite"]
		}

		file { "/etc/nagios2/mysite/hostgroups.cfg":
			ensure		=> "present",
			source		=> "puppet:///nagios/hostgroups.cfg",
			notify		=> Service["nagios2"],
			require		=> File["/etc/nagios2/mysite"]
		}

		file { "/etc/nagios2/mysite/hosts.cfg":
			ensure		=> "present",
			source		=> "puppet:///nagios/hosts.cfg",
			notify		=> Service["nagios2"],
			require		=> File["/etc/nagios2/mysite"]
		}
		
		file { "/etc/nagios2/mysite/services.cfg":
			ensure		=> "present",
			source		=> "puppet:///nagios/services.cfg",
			notify		=> Service["nagios2"],
			require		=> File["/etc/nagios2/mysite"]
		}
	
		file { "/etc/nagios2/mysite/templates.cfg":
			ensure		=> "present",
			source		=> "puppet:///nagios/templates.cfg",
			notify		=> Service["nagios2"],
			require		=> File["/etc/nagios2/mysite"]
		}
		
		file { "/etc/nagios2/mysite/timeperiods_nagios2.cfg":
			ensure		=> "present",
			source		=> "puppet:///nagios/timeperiods_nagios2.cfg",
			notify		=> Service["nagios2"],
			require		=> File["/etc/nagios2/mysite"]
		}
	
		file { "/etc/nagios2/nagios.cfg":
			ensure		=> "present",
			source		=> "puppet:///nagios/nagios.cfg",
			replace		=> "true",
			notify		=> Service["nagios2"],
			require		=> File["/etc/nagios2/mysite"]
		}
		
		file { "/var/cache/nagios2":
			ensure		=> "directory",
			owner		=> "nagios",
			group		=> "www-data",
			require		=> File["/etc/nagios2/nagios.cfg"]
		}
		
		file { "/var/cache/nagios2/objects.cache":
			ensure		=> "present",
			owner		=> "nagios",
			group		=> "www-data",
			require		=> File["/var/cache/nagios2"]
		}
		
		file { "/var/lib/nagios2":
			ensure		=> "directory",
			owner		=> "nagios",
			group		=> "nagios",
			require		=> File["/etc/nagios2/nagios.cfg"]
		}
		
		file { "/var/lib/nagios2/comments.dat":
			ensure		=> "present",
			owner		=> "nagios",
			group		=> "www-data",
			require		=> File["/var/lib/nagios2"]
		}

		file { "/var/lib/nagios2/downtime.dat":
			ensure		=> "present",
			owner		=> "nagios",
			group		=> "www-data",
			require		=> File["/var/lib/nagios2"]
		}
		
		file { "/var/lib/nagios2/rw":
			ensure		=> "directory",
			owner		=> "nagios",
			group		=> "www-data",
			require		=> File["/var/lib/nagios2"]
		}
		
		service { "nagios2":
			enable		=> "true",
			ensure		=> "running",
			require		=> File["/etc/nagios2/nagios.cfg"]
		}
		
		file { "/etc/apache2/conf.d/nagios2.conf":
			ensure		=> "/etc/nagios2/apache2.conf",
			# Could give an error if module "apache" is not loaded
			notify		=> Service["apache2"],
			require		=> User["nagios"]
		}
	
		file { "/etc/nagios2/htpasswd.users":
			source		=> "puppet:///nagios/htpasswd.users",
			replace		=> "true",
			require		=> User["nagios"]		
		}
	}
}
