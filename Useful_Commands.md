1. To install Contrail Command and provision the contrai cluster using CLI

`docker run -td --net host -e action=provision_cluster -v /root/command_servers.yml:/command_servers.yml -v /root/instances.yml:/instances.yml --privileged --name contrail_command_deployer hub.juniper.net/contrail/contrail-command-deployer:1912.32`
