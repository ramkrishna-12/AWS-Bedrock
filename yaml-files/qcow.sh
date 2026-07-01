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

  # qcow2 is a popular disk image format used by QEMU, which is a generic and open-source machine emulator and virtualizer. The steps outlined in the script are for converting an ISO file (in this case, ubuntu.iso) to the qcow2 format and then uploading it to OpenStack's Glance service for use as a virtual machine image.
  # iso files are typically used for installation media, while qcow2 files are used for virtual machine disk images. The conversion process allows users to create a virtual machine image from an installation ISO, which can then be deployed in a cloud environment like OpenStack.
  # file formats like qcow2 support features such as snapshots and compression, making them more efficient for use in virtualized environments compared to raw disk images.
  # resources like Glance in OpenStack allow users to manage and store virtual machine images, making it easier to deploy and manage virtual machines in a cloud infrastructure.
  