# Homelab Ansible

## Requirements

- Python
- `pyenv`
- `pyenv-virtualenv`
- 1Password Beta
- 1Password CLI

## Preparation

```zsh
 # this shouldn't be necessary on my Mac because pyenv virtualenv is configured
 # in .zshrc to automatically activate but just in case
pyenv activate ansible-env-3.13
op signin
```

<!-- NOTE: First pihole: Andromeda, Second pihole: Centaurus -->

## New Appliances/Disaster Recovery

On any newly installed appliances:

```bash
ansible-playbook bootstrap.yml --limit '[hostname]'
```

For adding VMs or containers:

- Edit the inventory file to add the container name
- Take an unused MAC from the `secrets/mac_and_ip_addresses.json` file and assign it to that container name with a specified IP
- Tell Unifi to give that MAC address that fixed IP
- Run the playbook which clones the container, gives it the MAC address, then turns it on and DHCP assigns it the IP we specified in Unifi

## Make it go

Once all appliances are bootstrapped:

```bash
ansible-playbook playbook.yml
```

VMs and containers won't need to be bootstrapped, that's part of the ansible config already.
