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

4. Create a VPG with VN

```
cat << EOF > /vpg

{
  "virtual-machine-interface": {
    "virtual_machine_interface_bindings": {
      "key_value_pair": [
        {
          "key": "vnic_type",
          "value": "baremetal"
        },
        {
          "key": "vif_type",
          "value": "vrouter"
        },
        {
          "key": "profile",
          "value": "{\"local_link_information\":[{\"port_id\":\"xe-0/0/7\",\"switch_id\":\"xe-0/0/7\",\"switch_info\":\"vqfx10k_leaf1\",\"fabric\":\"Fabric-Test\"},{\"port_id\":\"xe-0/0/7\",\"switch_id\":\"xe-0/0/7\",\"switch_info\":\"vqfx10k_leaf2\",\"fabric\":\"Fabric-Test\"}]}"
        },
        {
          "key": "vpg",
          "value": "vpg_test"
        }
      ]
    },
    "virtual_machine_interface_properties": {
      "sub_interface_vlan_tag": "200"
    },
    "virtual_network_refs": [
      {
        "to": [
          "default-domain",
          "admin",
          "vn_test_100"
        ]
      }
    ],
    "instance_ip_back_refs": [],
    "name": "vmi_test",
    "parent_type": "project",
    "port_profile_refs": [],
    "fq_name": [
      "default-domain",
      "admin",
      "vmi_test"
    ],
    "security_group_refs": []
  }
}
EOF

curl -X POST -H "X-Auth-Token: ec646c9e3faa4842a51b6d187c999ee2" -H "Content-Type: application/json; charset=UTF-8" -d @vpg http://10.1.1.3:8082/virtual-machine-interfaces
```

5. Create VPG with native VN

```
cat << EOF > /vpg_native_vn

{
  "virtual-machine-interface": {
    "virtual_machine_interface_bindings": {
      "key_value_pair": [
        {
          "key": "vnic_type",
          "value": "baremetal"
        },
        {
          "key": "vif_type",
          "value": "vrouter"
        },
        {
          "key": "profile",
          "value": "{\"local_link_information\":[{\"port_id\":\"xe-0/0/6\",\"switch_id\":\"xe-0/0/7\",\"switch_info\":\"vqfx10k_leaf1\",\"fabric\":\"Fabric-Test\"}]}"
        },
        {
          "key": "vpg",
          "value": "test_vpg"
        },
        {
          "key": "tor_port_vlan_id",
          "value": "300"
        }
      ]
    },
    "virtual_machine_interface_properties": {
      "sub_interface_vlan_tag": "0"
    },
    "virtual_network_refs": [
      {
        "to": [
          "default-domain",
          "admin",
          "vn-blue"
        ]
      }
    ],
    "display_name": "test_vmi",
    "instance_ip_back_refs": [],
    "name": "test_vmi",
    "parent_type": "project",
    "port_profile_refs": [],
    "fq_name": [
      "default-domain",
      "admin",
      "test_vmi"
    ],
    "security_group_refs": []
  }
}
EOF

curl -X POST -H "X-Auth-Token: ec646c9e3faa4842a51b6d187c999ee2" -H "Content-Type: application/json; charset=UTF-8" -d @vpg_native_vn http://10.1.1.3:8082/virtual-machine-interfaces
```
6. Create a static route

```
cat << EOF > /static_route
{
  "interface-route-table": {
    "display_name": "ce_loopback",
    "fq_name": [
      "default-domain",
      "admin",
      "ce_loopback"
    ],
    "parent_type": "project",
    "interface_route_table_routes": {
      "route": [
        {
          "prefix": "1.2.3.4/32",
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
EOF

curl -X POST -H  "X-Auth-Token: 22cb7190991b425884437a387adff433" -H "Content-Type: application/json; charset=UTF-8" -d @static_route http://10.1.1.3:8082/interface-route-tables
```


