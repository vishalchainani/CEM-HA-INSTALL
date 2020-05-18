import requests
import json
import csv
import re


auth_url='http://10.1.1.3:5000/v3/auth/tokens'
api_url='http://10.1.1.3:8082/'

spine1_name='vqfx10k_spine1'
spine2_name='vqfx10k_spine2'

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

def get_uuid_href(name, element):
	token=get_token()
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    url=api_url+element
    resp=requests.get(url, headers=headers)
    output=resp.json()
    for data in output[element]:
    	if len(data['fq_name']) == 2:
    		if data['fq_name'][1] == name:
    			href=data['href']
    			uuid=data['uuid']
    	else:
    		if data['fq_name'][2] == name:
    			href=data['href']
    			uuid=data['uuid']
    return href, uuid

def create_ce_interface(static_route_prefix):
	temp_dict={}
	ce_intf_name=re.sub(r'\.','_', static_route_prefix.split('/')[0])
	params={
  		"interface-route-table": {
  		  "display_name": "ce_intf_name",
  		  "fq_name": [
  		    "default-domain",
  		    "admin",
  		    "ce_intf_name"
  		  ],
  		  "parent_type": "project",
  		  "interface_route_table_routes": {
  		    "route": [
  		      {
  		        "prefix": "prefix",
  		        "community_attributes": {
  		          "community_attribute": [
  		            "no-reoriginate"
  		          ]
  		        }
  		      }
  		    ]
  		  },
  		  "perms2": {
  		    "owner_access": 7,
  		    "global_access": 0,
  		    "share": []
  		  },
  		  "tag_refs": []
  		}
	}
	params['interface-route-table']['display_name']=ce_intf_name
	params['interface-route-table']['fq_name'][2]=ce_intf_name
	params['interface-route-table']['interface_route_table_routes']['route'][0]['prefix']=static_route_prefix
	token=get_token()
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    url_intf_route_table=api_url+'interface-route-tables'
    resp=requests.post(url_intf_route_table, headers=headers, json=params)
    output=resp.json()
    temp_dict['name']=output['interface-route-table']['name']
    temp_dict['uuid']=output['interface-route-table']['uuid']
    temp_dict['href']=output['interface-route-table']['href']
    return temp_dict

def create_vmi(static_route_name, static_route_href, static_route_uuid, vn_name, vn_href, vn_uuid):
        params={
                "virtual-machine-interface": {
                  "parent_type": "project",
                  "interface_route_table_refs": [
                    {
                      "to": [
                        "default-domain",
                        "admin",
                        "ce_loopback"
                      ],
                      "href": "http://10.1.1.3:8082/interface-route-table/27a58932-0046-4dd8-a417-c2f5bc13206a",
                      "uuid": "27a58932-0046-4dd8-a417-c2f5bc13206a"
                    }
                  ],
                  "virtual_machine_interface_device_owner": "network:router_interface",
                  "fq_name": [
                    "default-domain",
                    "admin",
                    "test_vmi"
                  ],
                  "virtual_network_refs": [
                    {
                      "to": [
                        "default-domain",
                        "admin",
                        "my_routed_vn"
                      ],
                      "href": "http://10.1.1.3:8082/virtual-network/c30a8154-c41e-409d-b49e-048113313dc9",
                      "uuid": "c30a8154-c41e-409d-b49e-048113313dc9"
                    }
                  ]
                }
        }
        params['virtual-machine-interface']['interface_route_table_refs'][0]['to'][2]=static_route_name
        params['virtual-machine-interface']['interface_route_table_refs'][0]["href"]=static_route_href
        params['virtual-machine-interface']['interface_route_table_refs'][0]["uuid"]=static_route_uuid
        params['virtual-machine-interface']['fq_name'][2]=vn_name+'_'+static_route_name
        params['virtual-machine-interface']['virtual_network_refs'][0]["to"][2]=vn_name
        params['virtual-machine-interface']['virtual_network_refs'][0]["href"]=vn_href
        params['virtual-machine-interface']['virtual_network_refs'][0]["uuid"]=vn_uuid
        token=get_token()
        headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
        url_vmi=api_url+'virtual-machine-interfaces'
        resp=requests.post(url_vmi, headers=headers, json=params)
        temp_dict={}
        output=resp.json()
        temp_dict['name']=output['virtual-machine-interface']['name']
        temp_dict['uuid']=output['virtual-machine-interface']['uuid']
        temp_dict['href']=output['virtual-machine-interface']['href']
        return temp_dict


def create_lr(lr_name, spine1_name, spine1_uuid, spine1_href, spine2_name, spine2_uuid, spine2_href, route_target):
	params={
  		"logical-router": {
  		  "virtual_network_refs": [],
  		  "tag_refs": [],
  		  "logical_router_gateway_external": False,
  		  "display_name": "MY_LR",
  		  "name": "MY_LR",
  		  "physical_router_refs": [
  		    {
  		      "to": [
  		        "default-global-system-config",
  		        "vqfx10k_spine1"
  		      ],
  		      "uuid": "ed9aa673-20ad-4816-b647-1ebd263cea52",
  		      "href": "http://10.1.1.3:8082/physical-router/ed9aa673-20ad-4816-b647-1ebd263cea52"
  		    },
            {
  		      "to": [
  		        "default-global-system-config",
  		        "vqfx10k_spine2"
  		      ],
  		      "uuid": "ed9aa673-20ad-4816-b647-1ebd263cea52",
  		      "href": "http://10.1.1.3:8082/physical-router/ed9aa673-20ad-4816-b647-1ebd263cea52"
  		    }
  		  ],
  		  "perms2": {
  		    "owner_access": 7,
  		    "global_access": 0,
  		    "share": []
  		  },
  		  "parent_type": "project",
  		  
  		  "configured_route_target_list": {
  		    "route_target": [
  		      "target:65202:123"
  		    ]
  		  },
  		  "logical_router_type": "vxlan-routing",
  		  "fq_name": [
  		    "default-domain",
  		    "admin",
  		    "MY_LR"
  		  ]
  		}
	}
	route_target_final="target:"+route_target
	params['logical-router']['display_name']=lr_name
	params['logical-router']['name']=lr_name
	params['logical-router']['physical_router_refs'][0]['to'][1]=spine1_name
	params['logical-router']['physical_router_refs'][0]['uuid']=spine1_uuid
	params['logical-router']['physical_router_refs'][0]['href']=spine1_href
    params['logical-router']['physical_router_refs'][1]['to'][1]=spine2_name
	params['logical-router']['physical_router_refs'][1]['uuid']=spine2_uuid
	params['logical-router']['physical_router_refs'][1]['href']=spine2_href
	params['logical-router']['configured_route_target_list']['route_target'][0]=route_target_final
	params['logical-router']['fq_name'][2]=lr_name
	token=get_token()
	headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
	url_lr=api_url+'logical-routers'
	resp=requests.post(url_lr, headers=headers, json=params)
	temp_dict={}
	output=resp.json()
	temp_dict['name']=output['logical-router']['name']
	temp_dict['uuid']=output['logical-router']['uuid']
	temp_dict['href']=output['logical-router']['href']
	return temp_dict

def update_lr(lr_uuid, list_of_vmi, list_of_vn):
	params={
  		"logical-router": {
  		  "virtual_machine_interface_refs": [
  		    {
  		      "fq_name": [
  		        "default-domain",
  		        "admin",
  		        "test_vmi"
  		      ],
  		      "uuid": "fd675c50-f778-4a67-b879-b34eb4f64412",
  		      "href": "http://10.1.1.3:8082/virtual-machine-interface/fd675c50-f778-4a67-b879-b34eb4f64412",
  		      "parent_type": "project",
  		      "virtual_network_refs": [
  		        {
  		          "to": [
  		            "default-domain",
  		            "admin",
  		            "my_routed_vn"
  		          ],
  		          "uuid": "c30a8154-c41e-409d-b49e-048113313dc9",
  		          "href": "http://10.1.1.3:8082/virtual-networks/c30a8154-c41e-409d-b49e-048113313dc9"
  		        }
  		      ]
  		    }
  		  ]
  		}
	}
	params['logical-router']['virtual_machine_interface_refs'].pop()
	for vmi in list_of_vmi:
		temp_dict={}
		index=list_of_vmi.index(vmi)
		temp_dict['fq_name']=['default-domain', 'admin', vmi["name"]]
		temp_dict['uuid']=vmi["uuid"]
		temp_dict['href']=vmi["href"]
		temp_dict['parent_type']='project'
		temp_dict['virtual_network_refs']=[]
		temp_vn={}
		temp_vn["to"]=[]
		temp_vn["to"].append("default-domain")
		temp_vn["to"].append("admin")
		temp_vn["to"].append(list_of_vn[index]["name"])
		temp_vn["uuid"]=list_of_vn[index]["uuid"]
		temp_vn["href"]=list_of_vn[index]["href"]
		temp_dict['virtual_network_refs'].append(temp_vn)
		params['logical-router']['virtual_machine_interface_refs'].append(temp_dict)
	print params
	token=get_token()
	headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
	url_lr=api_url+'logical-router/'+lr_uuid
	resp=requests.put(url_lr, headers=headers, json=params)
	print resp.json()
	

def update_vn(spine1_irb_ip_address, spine1_uuid, spine1_nh_ip_address, spine2_irb_ip_address, spine2_uuid, spine2_nh_ip_address, intf_route_table_uuid, vn_uuid):
	params={
  		"virtual-network": {
  		  "virtual_network_routed_properties": {
  		    "routed_properties": [
  		      {
  		        "routed_interface_ip_address": "172.16.31.1",
  		        "routing_protocol": "static-routes",
  		        "physical_router_uuid": "ed9aa673-20ad-4816-b647-1ebd263cea52",
  		        "static_route_params": {
  		          "interface_route_table_uuid": [
  		            "27a58932-0046-4dd8-a417-c2f5bc13206a"
  		          ],
  		          "next_hop_ip_address": [
  		            "172.16.31.5"
  		          ]
  		        }
  		      },
              {
  		        "routed_interface_ip_address": "172.16.31.1",
  		        "routing_protocol": "static-routes",
  		        "physical_router_uuid": "ed9aa673-20ad-4816-b647-1ebd263cea52",
  		        "static_route_params": {
  		          "interface_route_table_uuid": [
  		            "27a58932-0046-4dd8-a417-c2f5bc13206a"
  		          ],
  		          "next_hop_ip_address": [
  		            "172.16.31.5"
  		          ]
  		        }
  		      }
  		    ]
  		  }
  		}
	}
	params['virtual-network']['virtual_network_routed_properties']['routed_properties'][0]['routed_interface_ip_address']=spine1_irb_ip_address
	params['virtual-network']['virtual_network_routed_properties']['routed_properties'][0]['physical_router_uuid']=spine1_uuid
	params['virtual-network']['virtual_network_routed_properties']['routed_properties'][0]['static_route_params']['interface_route_table_uuid'][0]=intf_route_table_uuid
	params['virtual-network']['virtual_network_routed_properties']['routed_properties'][0]['static_route_params']['next_hop_ip_address'][0]=spine1_nh_ip_address
    params['virtual-network']['virtual_network_routed_properties']['routed_properties'][1]['routed_interface_ip_address']=spine2_irb_ip_address
	params['virtual-network']['virtual_network_routed_properties']['routed_properties'][1]['physical_router_uuid']=spine2_uuid
	params['virtual-network']['virtual_network_routed_properties']['routed_properties'][1]['static_route_params']['interface_route_table_uuid'][0]=intf_route_table_uuid
	params['virtual-network']['virtual_network_routed_properties']['routed_properties'][1]['static_route_params']['next_hop_ip_address'][0]=spine2_nh_ip_address
	token=get_token()
	headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
	url_vn=api_url+'virtual-network/'+vn_uuid
	resp=requests.put(url_vn, headers=headers, json=params)
	print resp.json()



spine1_href, spine1_uuid = get_uuid_href(spine1_name, 'physical-routers')
spine2_href, spine2_uuid = get_uuid_href(spine2_name, 'physical-routers')

with open('static_two_spine.csv', 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		list_ce_intf=[]
		vmi_list=[]
		lr_list=[]
		vn_list=[]
		list_ce_intf.append(create_ce_interface(row["STATIC_PREFIX"]))
		print list_ce_intf
		vn_name=row["VN_LIST"].split(",") 
		spine1_irb_list=row["SPINE_1_IRB_IP_ADDR_LIST"].split(",")
        spine2_irb_list=row["SPINE_2_IRB_IP_ADDR_LIST"].split(",")
		spine1_nh_list=row["SPINE_1_NH_LIST"].split(",")
        spine2_nh_list=row["SPINE_2_NH_LIST"].split(",")
        
		for vn in vn_name:
			temp_dict={}
			vn_index_no=vn_name.index(vn)
			temp_dict['name']=vn
			temp_dict['spine1_irb_address']=spine1_irb_list[vn_index_no]
            temp_dict['spine2_irb_address']=spine2_irb_list[vn_index_no]
			temp_dict['spine1_nh_address']=spine1_nh_list[vn_index_no]
            temp_dict['spine2_nh_address']=spine2_nh_list[vn_index_no]
			vn_href, vn_uuid = get_uuid_href(vn, 'virtual-networks')
			temp_dict['uuid']=vn_uuid
			temp_dict['href']=vn_href
			vn_list.append(temp_dict)
		print vn_list
		for vn in vn_list:
			vmi_list.append(create_vmi(list_ce_intf[0]['name'], list_ce_intf[0]['href'], list_ce_intf[0]['uuid'], vn["name"], vn["href"], vn["uuid"]))
		print vmi_list
		lr_list.append(create_lr(row["LR_NAME"], spine1_name, spine1_uuid, spine1_href, spine2_name, spine2_uuid, spine2_href, row["ROUTE_TARGET"] ))
		print lr_list
		update_lr(lr_list[0]['uuid'], vmi_list, vn_list)
		for vn in vn_list:
			update_vn(vn['spine1_irb_address'], spine1_uuid, vn['spine1_nh_address'], vn['spine2_irb_address'], spine2_uuid, vn['spine2_nh_address'], list_ce_intf[0]['uuid'], vn['uuid'])
