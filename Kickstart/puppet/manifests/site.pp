# Only Ubuntu is supported with these manifests and modules!

import "templates.pp"
import "nodes.pp"
import "mysql_nodes.pp"
import "classes/*"
import "groups/*"
import "users/*"

filebucket { main: server => puppet }
File { backup => main }
