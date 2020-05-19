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

Copy the below lines after `dhcp-option=tag:jn,encap:43,3,"tftp"`

```
dhcp-host=d8:18:d3:61:4a:61,10.98.46.2 
dhcp-host=88:d9:8f:7d:8b:61,10.98.46.3 
dhcp-host=78:50:7c:99:68:0a,10.98.46.5 
dhcp-host=78:50:7c:99:d8:0a,10.98.46.6 
dhcp-host=78:50:7c:e3:c8:85,10.98.46.7 
dhcp-host=78:50:7c:e4:db:85,10.98.46.8 
dhcp-host=78:50:7c:e4:c7:85,10.98.46.9 
dhcp-host=78:50:7c:e3:f5:85,10.98.46.10 
dhcp-host=78:50:7c:e3:ff:85,10.98.46.11 
dhcp-host=78:50:7c:e4:b3:85,10.98.46.12 
dhcp-host=78:50:7c:e3:96:85,10.98.46.13 
dhcp-host=78:50:7c:e4:18:85,10.98.46.14
```

6. To check the fabric provisioning logs, look at below file on all the controller node(s)

` tail -f /var/log/contrail/contrail-fabric-ansible-playbooks.log`
