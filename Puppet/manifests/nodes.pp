node 'web.puppets.be' inherits webserver {
	include nagios

	apache::virtual_host { "web.puppets.be":
		ensure	=> "present"
	}
	apache::virtual_host { "foo.puppets.be":
		ensure	=> "present"
	}
}
