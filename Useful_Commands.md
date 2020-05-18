1. To install Contrail Command and provision the contrai cluster using CLI

`docker run -td --net host -e action=provision_cluster -v /root/command_servers.yml:/command_servers.yml -v /root/instances.yml:/instances.yml --privileged --name contrail_command_deployer hub.juniper.net/contrail/contrail-command-deployer:1912.32`

2. Check installation logs for Contrail Command

`docker logs -f contrail_command_deployer`

3. Check installation logs for Contrail Cluster

`docker exec contrail_command tail -f /var/log/contrail/deploy.log`

4. Decrypt the Appformix license and check for maximum number of hosts

`decrypt appformix license`

`gpg --decrypt appformix-license-RTU00024994638.v3.sig | grep Max`

5. To assign fixed IP addresses to em0 interface of switches during ZTP process

Edit jinja2 template of `dnsmasq.conf1` file at below location within `config_device_manager_1` docker on all the control nodes.

`vi /opt/contrail/fabric_ansible_playbooks/roles/ztp_dhcp_config/templates/dsnmasq.conf.j2`

Copy the below lines after
