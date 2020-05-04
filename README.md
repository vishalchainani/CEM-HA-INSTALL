# CEM-HA-INSTALL

This REPO is contains files needed for CEM HA installation. Below is the topology diagram, which depicts the interfaces on the respective VMs and their network connectivity to fabric and management network.

This topology also shows a contrail repo VM, incase the contrail repository has to be built locally.

![CEM HA VM TOPOLOGY](CEM_HA_VM_TOPO.png)

All the VMs must be updated with the below packages

`yum install -y yum-utils device-mapper-persistent-data lvm2 net-tools numactl nano`
