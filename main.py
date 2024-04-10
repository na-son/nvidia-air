import os
import json
import typing
import air_sdk

def copy_run(node: type[air_sdk.simulation_node.SimulationNode], src_filename: str, target_filename: str, post_cmd: list[str]):
    """
    Copies a file to the specified node, and runs each command in post_cmd as root using file_instruction()
    """
    data = {}

    fd = open(src_filename, "r")
    if fd.mode == 'r':
        file_str = fd.read()

    data[target_filename] = file_str
    data["post_cmd"] = post_cmd

    if AIR_DEBUG == True:
        print(f'{src_filename} instruction data is:')
        print(data)

    file_instruction(node, data)

def file_instruction(node: type[air_sdk.simulation_node.SimulationNode], data: str):
    """
    Creates instructions for a node given a file
    """
    try:
        node.create_instructions(data=json.dumps(data), executor='file')
        print(f'created instruction for: {node.name}')
    except:
        print(f'Error while creating instruction for: {node}')
        raise

def create_service(host: str, port: int, interface: str):
    """
    Creates a NAT to expose a given port on the oob-mgmt-server node, prints SSH instructions (works for root or ubuntu)
    """
    service = air.services.create(name=f'{host}-{port}', interface=f'{host}:{interface}', simulation=sim, dest_port=port)
    print(f'ssh -p {service.src_port} root@{service.host}')

def find_node(name: str) -> type[air_sdk.simulation_node.SimulationNode]:
    """
    Finds a node in the topology, and returns the first matching node. Don't have duplicate names in the topology!
    """

    node = air.simulation_nodes.list(simulation=sim, name=name)[0]
    return node

if __name__ == '__main__':
    EMAIL: str = os.environ["AIR_EMAIL"]
    TOKEN: str = os.environ["AIR_TOKEN"]
    AIR_DEBUG: bool = False
    
    air = air_sdk.AirApi(username=EMAIL, password=TOKEN)
    
    topology = "./topology.dot"
    
    # create simulation with topology from dotfile
    sim = air.simulations.create(topology_data=topology)
    
    # nix init
    nix = find_node('nix') 
    copy_run(nix, "hardware/nix-init.sh", "/home/ubuntu/nix-init.sh", ["bash /home/ubuntu/nix-init.sh"])
    
    # linux init script and ZTP
    oob = find_node('oob-mgmt-server')
    copy_run(oob, "hardware/linux-init.sh", "/home/ubuntu/linux-init.sh", ["bash /home/ubuntu/linux-init.sh"])
    copy_run(oob, "hardware/cumulus-ztp", "/var/www/html/cumulus-ztp", ["chmod 755 /var/www/html/cumulus-ztp"])

    create_service(oob.name, 22, 'eth0')
    