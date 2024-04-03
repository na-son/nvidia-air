import os
import air_sdk

EMAIL = os.environ["AIR_EMAIL"]
TOKEN = os.environ["AIR_TOKEN"]

air = air_sdk.AirApi(username=EMAIL, password=TOKEN)

topology = "./topology.dot"

print("Simulations:")
print(air.simulations.list)

print("Creating Simulation...")
sim = air.simulations.create(topology_data=dot_file)


# SSH Access to OOB server
service_name = 'oob-mgmt-server SSH'
interface = 'oob-mgmt-server:eth0'
dest_port = 22
service = air.services.create(name=service_name, interface=interface, simulation=sim, dest_port=dest_port)
print(f'ssh -p {service.src_port} {service.os_default_username}@{service.host}')

#print("Capacity:")
#air.capacity.get(sim)

nodes = air.simulation_nodes.list(simulation=sim)
for node in nodes:
   if 'sample-node' == node.name:
       sample_node = node
