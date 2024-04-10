#!/bin/bash
curl https://github.com/na-son.keys | tee /root/.ssh/authorized_keys

# clone my repo
#git clone https://github.com/na-son/nvidia-air /home/ubuntu/nvidia-air
#chown -R ubuntu:ubuntu /home/ubuntu/nvidia-air

# add some ansible ssh convenience settings so ad hoc ansible works easily
#cat <<EOT >> /etc/ansible/ansible.cfg
#[ssh_connection]
#ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
#EOT

#chmod -R 755 /etc/ansible/*

curl https://raw.githubusercontent.com/elitak/nixos-infect/master/nixos-infect | NIX_CHANNEL=nixos-23.11 NIXOS_CONFIG="https://raw.githubusercontent.com/na-son/nvidia-air/main/configuration.nix" sudo bash -x
