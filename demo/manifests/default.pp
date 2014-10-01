 exec { "update_repo" :
    command => "/usr/bin/apt-get update"
  }

  package { "python-pip":
    ensure => "installed",
   require => Exec ['update_repo'],
  }

  package { "vim":
    ensure => "installed",
   require => Exec ['update_repo'],
  }