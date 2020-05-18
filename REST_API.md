1. To generate token for authentication

```
cat << EOF > /auth
{
    "auth": {
        "scope": {
            "project": {
                "domain": {"id": "default"},
                "name": "$tenant"
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
EOF

curl -s -D - -H "Content-Type: application/json" -d @auth http://10.1.1.3:5000/v3/auth/tokens | awk "/X-Subject-Token/"'{print $2}'
```
2. Create a Virtual Network

```
cat << EOF > /vr

{
  "virtual-network": {
    "parent_type": "project",
    "fq_name": [
      "default-domain",
      "admin",
      "vn_test_400"
    ],
    "network_ipam_refs": [
      {
        "attr": {
          "ipam_subnets": [
            {
              "default_gateway": "192.168.100.1",
              "dns_server_address": "192.168.100.254",
              "enable_dhcp": false,
              "subnet": {
                "ip_prefix": "192.168.100.0",
                "ip_prefix_len": 24
              }
            }
          ]
        },
        "to": [
          "default-domain",
          "default-project",
          "default-network-ipam"
        ]
      }
    ],
    "phyiscal_router_back_refs": [
      {
        "uuid": "ed9aa673-20ad-4816-b647-1ebd263cea52"
      }
    ],
    "router_external": false
  }
}
EOF

curl -X POST -H "X-Auth-Token: ec646c9e3faa4842a51b6d187c999ee2" -H "Content-Type: application/json; charset=UTF-8" -d @vr http://10.1.1.3:8082/virtual-networks
```

3. Create a Routed Virtual Network

```
cat << EOF > /routed_vr

{
  "virtual-network": {
    "parent_type": "project",
    "fq_name": [
      "default-domain",
      "admin",
      "vn_test_300"
    ],
    "network_ipam_refs": [
      {
        "attr": {
          "ipam_subnets": [
            {
              "enable_dhcp": false,
              "subnet": {
                "ip_prefix": "192.168.100.0",
                "ip_prefix_len": "24"
              }
            }
          ]
        },
        "to": [
          "default-domain",
          "default-project",
          "default-network-ipam"
        ]
      }
    ],
    "phyiscal_router_back_refs":[
      {
      	"uuid":ed9aa673-20ad-4816-b647-1ebd263cea52
      }
    ],
    "virtual_network_category":"routed"
  }
}
EOF

curl -X POST -H "X-Auth-Token: ec646c9e3faa4842a51b6d187c999ee2" -H "Content-Type: application/json; charset=UTF-8" -d @routed_vr http://10.1.1.3:8082/virtual-networks
```



