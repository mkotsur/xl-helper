exec { "update_repo" :
  command => "/usr/bin/apt-get update"
}

exec {"disable_firewall":
  path => ["/usr/bin/","/usr/sbin/","/bin"],
  command => "sudo ufw disable",
  user => root
}

package { "python-pip":
  ensure => "installed",
  require => Exec ['update_repo'],
}

package { "default-jre":
  ensure => "installed",
  require => Exec ['update_repo'],
}

package { "vim":
  ensure => "installed",
  require => Exec ['update_repo'],
}