OPENSTACK_HOST = "keystone.primary.example.com"
OPENSTACK_KEYSTONE_URL = "http://keystone.primary.example.com:5000/v3"

AVAILABLE_REGIONS = [
  ('http://keystone.primary.example.com:5000/v3', 'Region1'),
  ('http://keystone.secondary.example.com:5000/v3', 'Region2'),
]

MULTI_REGION_SUPPORT = True



# What breaks most often:
# 1. SSL cert mismatch: Region2 uses a self-signed cert but OPENSTACK_SSL_NO_VERIFY is False. Horizon silently fails to load Region2 data.
# 2. Endpoint catalog per-region: services in Region2 must have their endpoints registered under the correct region name in Keystone. If nova in Region2 has --region RegionTwo but Horizon expects Region2, it fails with empty project lists.
# 3. Session region not sticky: user switches region, session doesn't encode it properly — they see Region1 data on Region2 UI. Fix: use server-side sessions (not cookie) so region choice is server-persisted.
# 4. Time zone issues: if regions span geographic locations, timestamp display can confuse operators

# local settings.py is for local overrides. It is not tracked in git, so you can safely put sensitive information here (like passwords) without worrying about it being committed to the repository.
# deploy openstack-dashboard with a local_settings.py that contains the above settings, and it will work with multiple regions as long as the above caveats are addressed.
# local controls openstack deployment 
