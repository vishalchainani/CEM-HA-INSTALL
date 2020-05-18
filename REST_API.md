1. To generate token for authentication

`
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

curl -s -D - -H "Content-Type: application/json" -d @auth http://10.1.1.3:5000/v3/auth/tokens | awk "/X-Subject-Token/"'{print $2}'`
