kubectl create secret generic openstack-credentials \
  --from-literal=OS_AUTH_URL=https://openstack.example.com:5000/v3 \
  --from-literal=OS_PROJECT_NAME=myproject \
  --from-literal=OS_USERNAME=myuser \
  --from-literal=OS_PASSWORD=mypassword \
  --from-literal=OS_USER_DOMAIN_NAME=Default \
  --from-literal=OS_PROJECT_DOMAIN_NAME=Default

# This command creates a Kubernetes secret named "openstack-credentials" that contains the OpenStack authentication credentials. The secret can be used by pods in the cluster to authenticate with OpenStack services.
# Make sure to replace the placeholder values (https://openstack.example.com:5000/v3, myproject, myuser, mypassword) with your actual OpenStack credentials before running the command.
# kubectl get secret openstack-credentials -o yaml
