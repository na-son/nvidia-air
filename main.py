import os
import air_sdk

EMAIL = os.environ["AIR_EMAIL"]
TOKEN = os.environ["AIR_TOKEN"]

air = air_sdk.AirApi(username=EMAIL, password=TOKEN)

topology = "./topology.dot"

# create sim with topology
sim = air.simulations.create(topology_data=topology)

# simulation node startup stuff 


nodes = air.simulation_nodes.list(simulation=sim)
for node in nodes:
   if 'nix' == node.name:
       nix = node


key = 'curl https://github.com/na-son.keys | tee /root/.ssh/authorized_keys; chage -d 1 ubuntu'

infect = 'curl https://raw.githubusercontent.com/elitak/nixos-infect/master/nixos-infect | NIX_CHANNEL=nixos-23.11 NIXOS_CONFIG="https://raw.githubusercontent.com/na-son/nvidia-air/main/configuration.nix" sudo bash -x'
nix.create_instructions(data=key, executor='shell')
nix.create_instructions(data=infect, executor='shell')

oob_mgmt_server = air.simulation_nodes.list(simulation=sim, name='oob-mgmt-server')[0]
clone = 'git clone https://github.com/na-son/nvidia-air.git /home/ubuntu/nvidia-air'
oob_mgmt_server.create_instructions(data=key, executor='shell')
oob_mgmt_server.create_instructions(data=clone, executor='shell')

# get NAT for external SSH
service_name = 'oob-mgmt-server SSH'
interface = 'oob-mgmt-server:eth0'
dest_port = 22
service = air.services.create(name=service_name, interface=interface, simulation=sim, dest_port=dest_port)
#print(f'ssh -p {service.src_port} {service.os_default_username}@{service.host}')
print(f'ssh -p {service.src_port} root@{service.host}')
print(f'ssh -J root@{service.host}:{service.src_port} root@nix')

