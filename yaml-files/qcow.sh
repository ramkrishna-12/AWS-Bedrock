# Step 1: Always verify source format first
qemu-img info ubuntu.iso

# Step 2: Convert
qemu-img convert -f raw -O qcow2 ubuntu.iso ubuntu.qcow2

# Step 3: Upload to Glance
openstack image create \
  --disk-format qcow2 \
  --container-format bare \
  --file ubuntu.qcow2 \
  --public ubuntu-22