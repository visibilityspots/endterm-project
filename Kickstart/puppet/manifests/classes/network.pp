class network {	
	file { "/etc/resolv.conf":
		owner	=> "root",
		group	=> "root",
		mode	=> "0644",
		content	=> template("resolv.conf.erb")
	}

	file { "/etc/network/interfaces":
		owner	=> "root",
		group	=> "root",
		mode	=> "0644",
		content	=> template("interfaces.erb")
	}
}
