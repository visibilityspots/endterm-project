class php {
	$packagelist = ["php5", "libapache2-mod-php5", "php5-mysql"]

	package { $packagelist:
		ensure	=> "installed",
		notify	=> Service["apache2"]
	}

	apache::module { "php5":
		ensure => "present"
	}
}
