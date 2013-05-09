class openssh {
	$ssh_packages = ["openssh-server", "openssh-client"]

	package { $ssh_packages:
		ensure => "installed"
	}

	user { "sshd":
		ensure		=> "present",
		uid		=> "22",
		gid		=> "22",
		comment		=> "OpenSSH Server",
		home		=> "/var/run/sshd",
		shell		=> "/bin/false",
		require		=> Package["openssh-server"]
	}

	service { ssh:
		enable		=> true,
		ensure		=> running,
		hasrestart	=> "true",
		require		=> User["sshd"]
	}
}
