define apache::virtual_host($ensure = 'present') {
	$document_root = "/var/www/$name"
	
	case $ensure {
		'present': {
			file { $document_root:
				ensure	=> "directory",
				require	=> Package["apache2"]
			}
			file { "${document_root}/index.html":
				content	=> template("apache/index.html.erb"),
				replace	=> false,
				require	=> File["$document_root"]
			}
			file { "/etc/apache2/sites-available/$name":
				content	=> template("apache/virtual_host.erb"),	
				require	=> File["$document_root"]
			}
			exec { "/usr/sbin/a2ensite $name":
				unless => "/bin/sh -c '[ -L /etc/apache2/sites-enabled/${name} ] && [ /etc/apache2/sites-enabled/${name} -ef /etc/apache2/sites-available/${name} ]'",
				notify => Exec["reload-apache2"],
				subscribe => File["/etc/apache2/sites-available/$name"],
				refreshonly => "true",
				require => File["/etc/apache2/sites-available/$name"]
			}
		}
		'disabled': {
			exec { "/usr/sbin/a2dissite $name":
				onlyif => "/bin/sh -c '[ -L /etc/apache2/sites-enabled/${name} ] && [ /etc/apache2/sites-enabled/${name} -ef /etc/apache2/sites-available/${name} ]'",
				notify => Exec["reload-apache2"],
				require => Package["apache2"]
			}
		}	
		'absent': {
			file { "/etc/apache2/sites-available/$name":
				ensure	=> "absent"
			}
			file { $document_root:
				ensure	=> "absent",
				force	=> "true"
			}
			exec { "/usr/sbin/a2dissite $name":
				onlyif => "/bin/sh -c '[ -L /etc/apache2/sites-enabled/${name} ] && [ /etc/apache2/sites-enabled/${name} -ef /etc/apache2/sites-available/${name} ]'",
				notify => Exec["reload-apache2"],
				require => Package["apache2"]
			}
		}
	}
}
