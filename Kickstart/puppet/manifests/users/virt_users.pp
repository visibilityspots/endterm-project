class virt_users {
	@user { "root":
		ensure	=> "present",
		password => '',
	}

	@user { "wout":
		ensure	=> "present",
		gid	=> "itteam",
		comment	=> "Wout",
		home	=> "/home/wout",
		shell	=> "/bin/bash",
		password => '',
	}

	@user { "jan":
		ensure	=> "present",
		gid	=> "itteam",
		comment	=> "Jan",
		home	=> "/home/jan",
		shell	=> "/bin/bash",
		password => '',
	}

	@user { "jorn":
		ensure	=> "present",
		gid	=> "itteam",
		comment	=> "Jorn",
		home	=> "/home/jorn",
		shell	=> "/bin/bash",
		password => '',
	}

}
