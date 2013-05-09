class php {
	$packagelist = ["php5", "libapache2-mod-php5", "php5-mysql"]

	if $nophp {
		package { $packagelist:
			ensure	=> "purged",
			# Could give an error if module "apache" is not loaded
			notify	=> Service["apache2"]
		}
		
		file { "/etc/apache2/mods-enabled/php5.conf":
			ensure	=> "absent"
		}
		
		file { "/etc/apache2/mods-enabled/php5.load":
			ensure	=> "absent"
		}	
	} else {
		package { $packagelist:
			ensure	=> "installed",
			notify	=> Service["apache2"]
		}
		
		file { "/etc/apache2/mods-enabled/php5.conf":
			ensure	=> "/etc/apache2/mods-available/php5.conf",
			require	=> Package["libapache2-mod-php5"]
		}
		
		file { "/etc/apache2/mods-enabled/php5.load":
			ensure	=> "/etc/apache2/mods-available/php5.load",
			require	=> Package["libapache2-mod-php5"]
		}
	}
}
