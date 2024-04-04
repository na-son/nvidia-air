import os
import air_sdk

EMAIL = os.environ["AIR_EMAIL"]
TOKEN = os.environ["AIR_TOKEN"]

air = air_sdk.AirApi(username=EMAIL, password=TOKEN)

topology = "./topology.dot"

# create sim with topology
sim = air.simulations.create(topology_data=topology)

# simulation node startup stuff 


#nodes = air.simulation_nodes.list(simulation=sim)
#for node in nodes:
#   if 'oob' == node.name:
#       oob = node


#data = 'curl https://github.com/na-son.keys >> ~/.ssh/authorized_keys'
#oob.create_instructions(data=data, executor='shell')

oob_mgmt_server = air.simulation_nodes.list(simulation=sim, name='oob-mgmt-server')[0]
#ztp_contents = '<ztp_script_content_here>'
key = 'curl https://github.com/na-son.keys >> /home/ubuntu/.ssh/authorized_keys; chage -d 1 ubuntu'
clone = 'git clone https://github.com/na-son/nvidia-air.git /home/ubuntu/nvidia-air'
#data = {'/var/www/html/cumulus-ztp': ztp_contents}
#oob_mgmt_server.create_instructions(data=json.dumps(data), executor='file')
oob_mgmt_server.create_instructions(data=key, executor='shell')
oob_mgmt_server.create_instructions(data=clone, executor='shell')

# start simulation
#sim.start()

# get NAT for external SSH
service_name = 'oob-mgmt-server SSH'
interface = 'oob-mgmt-server:eth0'
dest_port = 22
service = air.services.create(name=service_name, interface=interface, simulation=sim, dest_port=dest_port)
print(f'ssh -p {service.src_port} {service.os_default_username}@{service.host}')

