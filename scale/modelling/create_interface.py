import requests
import json

auth_url='http://10.209.22.233:5000/v3/auth/tokens'
api_url='http://10.209.22.233:8082/'


def get_token(fn):
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
        token = resp.headers['X-Subject-Token']
        def wrapper(device, intf):
        	fn=create_interface(device, intf)
        	headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
        	url=api_url+'physical-interfaces'
        	resp=requests.post(url, headers=headers, json=params)
        	output=resp.json()
        	return output
        return wrapper


@get_token
def create_interface(device, intf):
	params={
  		"physical-interface": {
    	"fq_name": [
    	    "default-global-system-config",
    	    "device",
    	    "intf",
    	],
    	"parent_type": "physical-router",
    	"display_name": "intf",
    	"name": "intf"
  	}
}
	params["physical-interface"]["fq_name"][1]=device
	params["physical-interface"]["fq_name"][2]=intf
	params["physical-interface"]["display_name"]=intf
	params["physical-interface"]["name"]=intf
	return params



device_list=["ssl-qfx5110-a", "ssl-qfx5110-b", "ssl-mx80-a"]

for device in device_list:
	for i in range(1,21):
		intf='ge-0/0/'+str(i)
		create_interface(device,intf)
