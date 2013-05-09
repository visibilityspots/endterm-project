class apache {
	$packagelist = ["apache2"]

	package { $packagelist:
		ensure	=> "installed"
	}

	group { "www-data":
		ensure		=> "present",
		gid		=> "80",
		require		=> Package["apache2"]
	}

	user { "www-data":
		ensure		=> "present",
		uid		=> "80",
		gid		=> "80",
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

	exec { "reload-apache2":
		command		=> "/etc/init.d/apache2 reload",
		refreshonly	=> "true"
	}

	exec { "force-reload-apache2":
		command		=> "/etc/init.d/apache2 force-reload",
		refreshonly	=> "true"
	}

	define module($ensure = 'present') {
		case $ensure {
			'present': {
				exec { "/usr/sbin/a2enmod $name":
					unless => "/bin/sh -c '[ -L /etc/apache2/mods-enabled/${name}.load ] && [ /etc/apache2/mods-enabled/${name}.load -ef /etc/apache2/mods-available/${name}.load ]'",
					notify => Service["apache2"],	
					require => Package["apache2"]
				}
			}
			'absent': {
				exec { "/usr/sbin/a2dismod $name":
					onlyif => "/bin/sh -c '[ -L /etc/apache2/mods-enabled/${name}.load ] && [ /etc/apache2/mods-enabled/${name}.load -ef /etc/apache2/mods-available/${name}.load ]'",
					notify => Service["apache2"],
					require => Package["apache2"]
				}
			}
		}
	}
}
