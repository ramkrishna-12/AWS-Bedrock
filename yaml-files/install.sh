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