# Homelab Ansible

## Requirements

- Python
- `pyenv`
- `pyenv-virtualenv`
- 1Password Beta
- 1Password CLI

## Get started

```zsh
 # this shouldn't be necessary on my Mac because pyenv virtualenv is configured
 # in .zshrc to automatically activate but just in case
pyenv activate ansible-env-3.13
op signin
ansible-playbook playbook.yml
```

<!-- NOTE: First pihole: Andromeda, Second pihole: Centaurus -->
