# Homelab Ansible

## Requirements

- Python
- Virtualenv

## Get started

Right now this just has a small lil inventory of the proxmox server to configure. To test it:

```
source venv/bin/activate
ansible hosts -m ping -i inventory.yml
```
