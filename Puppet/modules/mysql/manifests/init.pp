class mysql {
	$packagelist = ["mysql-server"]

	package { $packagelist:
		ensure	=> "installed"
	}

	file { "/etc/mysql/my.cnf":
		owner	=> "root",
		group	=> "root",
		mode	=> "0644",
		replace	=> true,
		source	=> "puppet:///mysql/my.cnf",
		require => Package["mysql-server"]
	}

	group { "mysql":
		ensure	=> "present",
		gid	=> "3306",
		require	=> Package["mysql-server"]
	}

	user { "mysql":
		ensure	=> "present",
		uid	=> "3306",
		gid	=> "3306",
		comment	=> "MySQL Server",
		home	=> "/var/lib/mysql",
		shell	=> "/bin/false",
		require	=> Group["mysql"]
	}

	service { "mysql":
		enable	=> "true",
		ensure	=> "running",
		require	=> File["/etc/mysql/my.cnf"]
	}
}
