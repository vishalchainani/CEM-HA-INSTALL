import requests
import json
import csv

auth_url='http://10.1.1.3:5000/v3/auth/tokens'
api_url='http://10.1.1.3:8082/'


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

def get_physical_routers():
        router_list=[]
        token=get_token()
        headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
        url_router_list=api_url+'physical-routers'
        resp=requests.get(url_router_list, headers=headers)
        output_list = resp.json()["physical-routers"]
        return output_list

def get_uuid(switches):
        final_list=[]
        router_list=get_physical_routers()
        for switch in switches.split(' '):
                temp_dict={}
                for router in router_list:
                        if switch == router['fq_name'][1]:
                                data='{\"uuid\":\"%s\"}'%(router['uuid'])
                                final_list.append(data)
        return final_list
def update_physical_router(router_list, vn_name, vn_uuid):
        for router_uuid in router_list:
                clean_uuid=str(router_uuid).split(':')[1].strip('\"').strip('}').strip('\"')
                token=get_token()
                headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
                url=api_url+'physical-router'+'/'+clean_uuid
                print url
                update_info='{"physical-router":{"virtual_network_refs":[{"to":["default-domain","admin","%s"],"href":"http://%svirtual-network/%s","attr":null,"uuid":"%s"}]}}'%(vn_name,api_url, vn_uuid, vn_uuid)
                print update_info
                data=json.loads(update_info)
                resp=requests.put(url, headers=headers, json=data)

def create_vn(vn_name, gateway, dns, prefix, prefix_len, routed, switches):
        router_list=get_uuid(switches)
        if routed.lower() == 'yes':
                params='{"virtual-network":{"parent_type":"project","fq_name":["default-domain","admin","%s"],"network_ipam_refs":[{"attr":{"ipam_subnets":[{"enable_dhcp":false,"subnet":{"ip_prefix":"%s","ip_prefix_len":"%s"}}]},"to":["default-domain","default-project","default-network-ipam"]}], "phyiscal_router_back_refs":[%s], "virtual_network_category":"routed"}}'%(vn_name, prefix, prefix_len, ','.join(router_list))
        else:
               params='{"virtual-network":{"parent_type":"project","fq_name":["default-domain","admin","%s"],"network_ipam_refs":[{"attr":{"ipam_subnets":[{"default_gateway":"%s","dns_server_address":"%s","enable_dhcp":false,"subnet":{"ip_prefix":"%s","ip_prefix_len":"%s"}}]},"to":["default-domain","default-project","default-network-ipam"]}], "phyiscal_router_back_refs":[%s]}}'%(vn_name, gateway, dns, prefix, prefix_len, ','.join(router_list))
        data=json.loads(params)
        token=get_token()
        headers= {'Content-Type': 'application/json','X-Auth-Token': token}
        url=api_url+'virtual-networks'
        resp=requests.post(url, headers=headers, json=data)
        output=resp.json()
        update_physical_router(router_list, output['virtual-network']['name'], output['virtual-network']['uuid'] )
        print "Created VN "+output['virtual-network']['name']+" with uuid "+output['virtual-network']['uuid']

with open('vn.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                create_vn(row['vn_name'], row['gateway'], row['dns'], row['prefix'].split('/')[0], row['prefix'].split('/')[1], row['routed'], row['switches'])
