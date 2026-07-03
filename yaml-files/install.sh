# Installation sequence per node
# Install nova-compute + neutron-openvswitch-agent
apt install nova-compute neutron-openvswitch-agent

# Configure /etc/nova/nova.conf — point to existing RabbitMQ, Keystone, Placement
# Configure /etc/neutron/neutron.conf + /etc/neutron/plugins/ml2/openvswitch_agent.ini

# Start services
systemctl start nova-compute neutron-openvswitch-agent

# Register with Placement (automatic but verify)
openstack compute service list --host 
# State: up, Status: enabled — both must be true within 60 seconds

openstack resource provider list | grep 
# Must appear with correct CPU/RAM/disk inventory


# Verify before declaring done
# Force schedule a test VM to the new node
openstack server create --flavor m1.small --image test-img \
  --availability-zone nova: test-vm

# Verify it reaches ACTIVE
openstack server show test-vm | grep status

# Attach a volume, assign a FIP, ping external — full end-to-end test
# Then delete the test VM

# installing the compute node is complete 
# multiple compute nodes can be installed in parallel, but each node must be verified before moving on to the next.