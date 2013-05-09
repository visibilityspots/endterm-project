define bind::domain($ensure = 'present') {
	case $ensure {
		'present': {
			file { "/etc/bind/db.${name}":
				ensure	=> "present",
				replace	=> "true",
				source	=> "puppet:///bind/db/db.${name}",
				notify	=> Exec["restart-bind9"],				
			}
		}	
		'absent': {
			file { "/etc/bind/db.${name}":
				ensure	=> "absent",
				notify	=> Exec["restart-bind9"]
			}
		}
	}
}
