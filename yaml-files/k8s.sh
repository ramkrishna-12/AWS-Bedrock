kubectl create secret generic openstack-credentials \
  --from-literal=OS_AUTH_URL=https://openstack.example.com:5000/v3 \
  --from-literal=OS_PROJECT_NAME=myproject \
  --from-literal=OS_USERNAME=myuser \
  --from-literal=OS_PASSWORD=mypassword \
  --from-literal=OS_USER_DOMAIN_NAME=Default \
  --from-literal=OS_PROJECT_DOMAIN_NAME=Default
