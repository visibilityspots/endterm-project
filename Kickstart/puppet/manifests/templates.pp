class baseclass {
	$nameservers = []
	include network

	include baseapps, openssh
	
	include itteam
}

class webserver {
	include apache
	include mysql
	include php
}
