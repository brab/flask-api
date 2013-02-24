Vagrant::Config.run do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network :hostonly, "192.168.33.10"
  config.vm.share_folder "code", "/home/vagrant/app", ".", :nfs => true
  config.vm.customize ["setextradata", :id, "VBoxInternal2/SharedFolderEnableSymlinksCreate/app", "1"]
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/"
    puppet.manifest_file  = "manifests/vagrant.pp"
    puppet.module_path = "puppet/modules/"
  end
end
