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
			
			file { "/etc/apache2/sites-enabled/$name":
				ensure	=> "/etc/apache2/sites-available/$name",
				require	=> File["/etc/apache2/sites-available/$name"],
				notify	=> Service["apache2"]
			}
		}
		'disabled': {
			file { "/etc/apache2/sites-enabled/$name":
				ensure	=> "absent",
				notify	=> Service["apache2"]
			}
		}	
		'absent': {
			file { $document_root:
				ensure	=> "absent",
				recurse	=> "true",
				force	=> "true"
			}
			
			file { "/etc/apache2/sites-available/$name":
				ensure	=> "absent"
			}
			
			file { "/etc/apache2/sites-enabled/$name":
				ensure	=> "absent",
				notify	=> Service["apache2"]
			}
		}
	}
}
