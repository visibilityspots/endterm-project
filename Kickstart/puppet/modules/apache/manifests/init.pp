class apache {
	$packagelist = ["apache2", "apache2-mpm-prefork", "apache2-utils", "apache2.2-common"]
	
	if $noapache {
		package { $packagelist:
			ensure	=> "purged"
		}
		
		service { "apache2":
			enable	=> "false",
			ensure	=> "stopped"
		}
		
		# Do not remove user "www-data" and group "www-data" because they are default users!
		
		# Remove Apache configuration, but do not delete /var/www!
		file { "/etc/apache2":
			ensure	=> "absent",
			recurse	=> "true",
			force	=> "true"
		}
	} else {
		package { $packagelist:
			ensure	=> "installed"
		}
	
		group { "www-data":
			ensure		=> "present",
			require		=> Package["apache2"]
		}
	
		user { "www-data":
			ensure		=> "present",
			gid		=> "www-data",
			comment		=> "Apache Server",
			home		=> "/var/www",
			shell		=> "/bin/false",
			require		=> Group["www-data"]
		}
	
		service { "apache2":
			enable		=> "true",
			ensure		=> "running",
			hasrestart	=> "true",
			require		=> User["www-data"]
		}
	
		file { "/var/www/index.html":
			ensure		=> "present",
			owner		=> "www-data",
			group		=> "www-data",
			mode		=> "0644",
			replace		=> true,
			source		=> "puppet:///apache/index.html",
			require		=> User["www-data"]
		}
	}
}
