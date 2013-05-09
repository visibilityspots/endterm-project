class bind9 {
	$packagelist = ["bind9"]
	$nameserver = ["192.168.255.254"]

	package { $packagelist:
		ensure	=> "installed"
	}

	service { "bind9":
		enable		=> "true",
		ensure		=> "running",
		hasrestart	=> "true",
	}

	file { "/etc/bind/named.conf.options":
		ensure		=> "present",
		replace		=> true,
		content => template("named.conf.options-template.erb")
	}

	file { "/etc/bind/named.conf.local":
		ensure		=> "present",
		replace		=> true,
		source		=> "puppet:///bind9/named.conf.local",
	}

	file { "/etc/bind/db.puppets.be":
		ensure		=> "present",
		replace		=> true,
		source		=> "puppet:///bind9/db.puppets.be",
	}

	file { "/etc/bind/db.192":
		ensure		=> "present",
		replace		=> true,
		source		=> "puppet:///bind9/db.192",
	}

	exec { "restart-bind9":
		command		=> "/etc/init.d/bind9 restart",
		refreshonly	=> "true"
	}
}
