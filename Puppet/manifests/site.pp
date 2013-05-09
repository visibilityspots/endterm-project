# Only Ubuntu is supported with these manifests and modules!

import "templates.pp"
import "nodes.pp"
import "classes/*"
import "groups/*"
import "users/*"
import "os/*"

import "/usr/local/www/puppetadmin/puppet/puppetadmin.pp"

filebucket { main: server => puppet }
File { backup => main }
