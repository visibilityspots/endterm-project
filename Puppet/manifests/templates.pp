node basenode {
	# Always Ubuntu
	include ubuntu

	include baseapps, openssh

	include itteam
}

node default inherits basenode {}

node webserver inherits basenode {
	include apache
	include mysql
	include php
	include bind9
}
