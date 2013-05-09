class nagios {
	$packagelist = ["nagios2", "nagios-plugins", "nagios-images", "nagios-nrpe-plugin"]

	package { $packagelist:
		ensure	=> "installed",
		require	=> Class["apache"]
	}

	group { "nagios":
		ensure	=> "present",
		gid	=> "5000",
		require	=> Package["nagios2"]
	}

	user { "nagios":
		ensure		=> "present",
		uid		=> "5000",
		gid		=> "5000",
		comment		=> "Nagios Server",
		home		=> "/var/run/nagios2",
		shell		=> "/bin/false",
		require		=> Group["nagios"]
	}

	file { "/etc/apache2/conf.d/nagios2.conf":
		ensure		=> "/etc/nagios2/apache2.conf",
		require		=> User["nagios"]
	}

	file { "/etc/nagios2/htpasswd.users":
		source		=> "puppet:///nagios/htpasswd.users",
		replace		=> true,
		require		=> User["nagios"]		
	}

	file { "/etc/nagios2/configuration":
		ensure		=> "directory",
		owner		=> "nagios",
		group		=> "nagios",
		require		=> User["nagios"]
	}
}
