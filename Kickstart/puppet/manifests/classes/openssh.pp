class openssh {
	$ssh_packages = ["openssh-server", "openssh-client"]

	package { $ssh_packages:
		ensure => "installed"
	}

	group { "ssh":
		gid		=> "5022",
		notify		=> Service["ssh"],
		require		=> Package["openssh-server"]
	}

	user { "sshd":
		ensure		=> "present",
		uid		=> "5022",
		gid		=> "5022",
		comment		=> "OpenSSH Server",
		home		=> "/var/run/sshd",
		shell		=> "/bin/false",
		notify		=> Service["ssh"],
		require		=> Group["ssh"]
	}

	service { ssh:
		enable		=> "true",
		ensure		=> "running",
		hasrestart	=> "true",
		require		=> User["sshd"]
	}
}
