class bind {
	$forwarders = []
	$packagelist = ["bind9"]

	if $nobind {
		package { $packagelist:
			ensure	=> "purged"
		}
	
		user { "bind":
			ensure	=> "absent"
		}
		
		group { "bind":
			ensure	=> "absent",
			require	=> User["bind"]
		}
				
		file { "/etc/bind":
			ensure	=> "absent",
			recurse	=> "true",
			force	=> "true"
		}
	} else {
		package { $packagelist:
			ensure	=> "installed"
		}
		
		group { "bind":
			ensure		=> "present",
			require		=> Package["bind9"]
		}
		
		user { "bind":
			ensure		=> "present",
			gid		=> "bind",
			comment		=> "Bind Server",
			home		=> "/var/cache/bind",
			shell		=> "/bin/false",			
			require		=> Group["bind"]
		}
	
		service { "bind9":
			enable		=> "true",
			# Does not work well
			#ensure		=> "running",
			hasrestart	=> "false",
			provider	=> "debian",
			require		=> User["bind"]
		}
		
		exec { "restart-bind9":
			command		=> "/etc/init.d/bind9 restart",
			refreshonly	=> "true"
		}
		
		file { "/etc/bind":
			ensure		=> "directory",
			owner		=> "root",
			group		=> "bind",
			recurse		=> "true",
			require		=> User["bind"]
		}
		
		file { "/etc/bind/rndc.key":
			ensure		=> "present",
			owner		=> "bind",
			group		=> "bind",
			mode		=> "0640",
			require		=> File["/etc/bind"]
		}
	
		file { "/etc/bind/named.conf.options":
			ensure		=> "present",
			owner		=> "bind",
			group		=> "bind",
			replace		=> "true",
			content		=> template("bind/named.conf.options.erb"),
			notify		=> Exec["restart-bind9"],
			require		=> User["bind"]
		}
		
		file { "/etc/bind/named.conf.local":
			ensure		=> "present",
			owner		=> "bind",
			group		=> "bind",
			replace		=> "true",
			content		=> template("bind/named.conf.local.erb"),
			notify		=> Exec["restart-bind9"],
			require		=> User["bind"]
		}
		
			
	}
}
