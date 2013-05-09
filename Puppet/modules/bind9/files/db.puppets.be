;
; BIND data file for puppets.be
;
$TTL	604800
@	IN	SOA	web.puppets.be. root.puppets.be. (
			     56		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
@	IN	NS	web.puppets.be.
@	IN	A	192.168.255.73
web	IN	A	192.168.255.73
puppet	IN	A	192.168.255.84
nagios 	IN	A	192.168.255.87
