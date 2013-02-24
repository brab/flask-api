node default {
  group { 'puppet':
    ensure => present,
  }

  exec { 'initial_apt_update':
    command => '/usr/bin/apt-get update',
  }
  exec { 'initial_apt_upgrade':
    command => '/usr/bin/apt-get --assume-yes upgrade',
    require => Exec['initial_apt_update'],
  }
  exec { 'apt_autoremove':
    command => '/usr/bin/apt-get autoremove --assume-yes',
    require => Exec['initial_apt_upgrade'],
  }
  exec { 'apt_autoclean':
    command => '/usr/bin/apt-get autoclean --assume-yes',
    require => Exec['initial_apt_upgrade'],
  }

  package { 'software-properties-common':
    ensure  => 'installed',
    require => Exec['initial_apt_update'],
  }

  $packages = ['git-core', 'git', 'make', 'g++', 'python-pip', 'python-dev', 'libncurses5-dev',
  'libjpeg-dev', 'python-imaging', 'libevent-dev', 'nodejs', 'npm', 'ruby-compass', 'curl',
  'libjpeg-turbo-progs', 'optipng', 'mongodb', 'mongodb-dev']

  package { 'install-packages':
    name    => $packages,
    ensure  => 'installed',
    require => Exec['initial_apt_upgrade'],
    before  => Exec['pip-install', 'easy-install', 'gem-install'],
  }

  exec { 'pip-install':
    command => '/usr/bin/pip install -r py-packages.txt',
    cwd     => '/home/vagrant/app',
  }

  exec { 'easy-install':
    command => '/usr/bin/easy_install readline',
  }

  exec { 'gem-install':
    command => '/opt/vagrant_ruby/bin/gem install foreman',
  }
}
