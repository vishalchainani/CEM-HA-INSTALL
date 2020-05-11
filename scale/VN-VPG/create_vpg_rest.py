import requests
import json
import csv

auth_url='http://10.1.1.3:5000/v3/auth/tokens'
api_url='http://10.1.1.3:8082/'
fabric_name='Fabric-Test'


def get_token():
	params={
	    "auth": {
	        "scope": {
	            "project": {
	                "domain": {"id": "default"},
	                "name": "admin"
	            }
	        },
	        "identity": {
	            "methods": ["password"],
	            "password": {
	                "user": {
	                    "name": "admin",
	                    "domain": {"id": "default"},
	                    "password": "contrail123"
	                }
	            }
	        }
	    }
	}
	resp=requests.post(auth_url, json=params)
	return resp.headers['X-Subject-Token']

def gen_link_info(row):
	link_information=[]
	intf_list=row['interfaces'].split(' ')
	switch_list=row['switch_name'].split(' ')
	
	for switch in switch_list:
		index=switch_list.index(switch)
		intf=intf_list[index]
		data='{\\\"port_id\\\":\\\"%s\\\",\\\"switch_id\\\":\\\"%s\\\",\\\"switch_info\\\":\\\"%s\\\",\\\"fabric\\\":\\\"%s\\\"}'%(intf, intf, switch, fabric_name)
		link_information.append(data)
	
	return link_information

def get_vpg_list():
	vpg_list=[]
	token = get_token()
	headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
	url_vpg_list=api_url+'virtual-port-groups'
	resp=requests.get(url_vpg_list, headers=headers)
	for vpg in resp.json()['virtual-port-groups']:
		vpg_list.append(vpg['fq_name'][2])
	return vpg_list


def create_vmi(row):
	list_info=gen_link_info(row)
	vmi_name=row['vpg_name']+'_'+row['switch_name'].split(' ')[0]+'_'+row['interfaces'].split(' ')[0]+'_'+row['vlan']
	if row['vlan_type'].lower() == 'untagged':
		params='{"virtual-machine-interface":{"virtual_machine_interface_bindings":{"key_value_pair":[{"key":"vnic_type","value":"baremetal"},{"key":"vif_type","value":"vrouter"},{"key":"profile","value":"{\\"local_link_information\\":[%s]}"},{"key":"vpg","value":"%s"},{"key":"tor_port_vlan_id", "value":"%s"}]},"virtual_machine_interface_properties":{"sub_interface_vlan_tag":"0"},"virtual_network_refs":[{"to":["default-domain","admin","%s"]}],"instance_ip_back_refs":[],"name":"%s","parent_type":"project","port_profile_refs":[],"fq_name":["default-domain","admin","%s"],"security_group_refs":[]}}'%(','.join(list_info), row['vpg_name'], row['vlan'], row['vn_name'], vmi_name, vmi_name)
	elif row['vlan_type'].lower() == 'tagged':
		params='{"virtual-machine-interface":{"virtual_machine_interface_bindings":{"key_value_pair":[{"key":"vnic_type","value":"baremetal"},{"key":"vif_type","value":"vrouter"},{"key":"profile","value":"{\\"local_link_information\\":[%s]}"},{"key":"vpg","value":"%s"}]},"virtual_machine_interface_properties":{"sub_interface_vlan_tag":"%s"},"virtual_network_refs":[{"to":["default-domain","admin","%s"]}],"instance_ip_back_refs":[],"name":"%s","parent_type":"project","port_profile_refs":[],"fq_name":["default-domain","admin","%s"],"security_group_refs":[]}}'%(','.join(list_info), row['vpg_name'], row['vlan'], row['vn_name'], vmi_name, vmi_name)
	data=json.loads(params)
	token=get_token()
	headers={'Content-Type': 'application/json','X-Auth-Token': token}
	url_vmi=api_url+'virtual-machine-interfaces'
	resp=requests.post(url_vmi, headers=headers, json=data)
	output = resp.json()
	print "Created Virtual Machine Interface "+output['virtual-machine-interface']['name']


def create_vpg(row):
	params_vpg='{"virtual-port-group":{"fq_name":["default-global-system-config","%s","%s"],"parent_type":"fabric","virtual_port_group_type":"access"}}'%(fabric_name, row['vpg_name'])
	data=json.loads(params_vpg)
	token=get_token()
	headers={'Content-Type': 'application/json','X-Auth-Token': token}
	url_vpg=api_url+'virtual-port-groups'
	resp=requests.post(url_vpg, headers=headers, json=data)
	output = resp.json()
	print "Create VPG "+output['virtual-port-group']['name']
	create_vmi(row)

with open('vpg.csv', 'r') as csvfile:
	reader=csv.DictReader(csvfile)
	for row in reader:
		if row['vpg_name'] in get_vpg_list():
			create_vmi(row)
		else:
			create_vpg(row)


		

