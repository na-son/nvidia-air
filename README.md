# Nvidia Air labs

here be dragons

## Setup

### Python

Using python 3.9

```shell
python -m venv venv
. venv/bin/activate
python -m pip install air-sdk
export AIR_USER='' #change to air email
export AIR_TOKEN='' #generate an air token
```

### Direnv (optional)

To use direnv, edit `.envrc` and add your email and token then `direnv allow`

## Usage

Run `python main.py` and run the ssh command provided. The air default user:password is `ubuntu:nvidia`

A host, `nix` is provided for emulating a server. You can ssh to it from the oob server.

### Topology generation

Go to https://air.nvidia.com/build 