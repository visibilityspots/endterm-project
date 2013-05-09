class baseapps {
	$packagelist = ["nano"]

	package { $packagelist:
		ensure => "installed",
	}
}
