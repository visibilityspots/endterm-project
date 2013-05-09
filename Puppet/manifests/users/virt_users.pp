class virt_users {
	@user { "wout":
		ensure	=> "present",
		uid	=> "1001",
		gid	=> "1001",
		comment	=> "Wout",
		home	=> "/home/wout",
		shell	=> "/bin/bash",
		password => '',
	}

	@user { "jorn":
		ensure	=> "present",
		uid	=> "1002",
		gid	=> "1001",
		comment	=> "Jorn",
		home	=> "/home/jorn",
		shell	=> "/bin/bash",
		password => '',
	}

	@user { "jan":
		ensure	=> "present",
		uid	=> "1003",
		gid	=> "1001",
		comment	=> "Jan",
		home	=> "/home/jan",
		shell	=> "/bin/bash",
		password => '',
	}
}
