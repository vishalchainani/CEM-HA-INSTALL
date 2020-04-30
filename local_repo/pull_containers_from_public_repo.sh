#!/bin/bash
cd /var/tmp/; git clone https://github.com/Juniper/contrail-ansible-deployer.git -b R2003
contrail_image_list="contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-analytics-api contrail-analytics-collector contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-analytics-alarm-gen contrail-external-kafka contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-analytics-query-engine contrail-external-cassandra contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-analytics-snmp-collector contrail-analytics-snmp-topology contrail-openstack-compute-init contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-controller-config-api contrail-controller-config-svcmonitor contrail-controller-config-schema contrail-controller-config-devicemgr contrail-controller-config-dnsmasq contrail-controller-config-stats contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-external-cassandra contrail-external-zookeeper contrail-external-rabbitmq contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-controller-control-control contrail-controller-control-named contrail-controller-control-dns contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-controller-control-control contrail-kubernetes-cni-init contrail-node-init contrail-status contrail-kubernetes-kube-manager contrail-mesosphere-cni-init contrail-node-init contrail-status contrail-mesosphere-mesos-manager contrail-external-redis contrail-external-stunnel contrail-external-rsyslogd contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-tor-agent contrail-node-init contrail-status contrail-vcenter-fabric-manager contrail-vcenter-manager contrail-vcenter-plugin contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-vrouter-kernel-init-dpdk contrail-vrouter-agent-dpdk contrail-vrouter-agent contrail-node-init contrail-status contrail-nodemgr contrail-provisioner contrail-vrouter-agent contrail-node-init contrail-status contrail-controller-webui-web contrail-controller-webui-job contrail-node-init contrail-status contrail-external-haproxy contrail-openstack-neutron-init contrail-vrouter-kernel-build-init contrail-vrouter-kernel-init contrail-openstack-heat-init contrail-command contrail-command-deployer contrail-kolla-ansible-deployer" 
CONTRAIL_PUBLIC_REGSITRY=${CONTRAIL_PUBLIC_REGSITRY:-"hub.juniper.net/contrail"}
CONTRAIL_VERSION=${CONTRAIL_VERSION:="2003.33"}
echo "$CONTRAIL_PUBLIC_REGSITRY" 
echo "$CONTRAIL_VERSION" 
rm -rf container_images
mkdir container_images
echo "Pulling images from $CONTRAIL_PUBLIC_REGSITRY" 
for container_image in $contrail_image_list; do
  container_image_name="$CONTRAIL_PUBLIC_REGSITRY/$container_image:$CONTRAIL_VERSION" 
  container_image_exists="sudo docker images $container_image_name | grep $container_image" 
  if ! `eval $container_image_exists >/dev/null`; then
    sudo docker pull $container_image_name
    sudo docker save $container_image_name > container_images/$container_image.$CONTRAIL_VERSION.tgz
  fi 
done
echo "All container packages are stored under /var/tmp/container_images"
rm -rf /var/tmp/contrail-ansible-deployer