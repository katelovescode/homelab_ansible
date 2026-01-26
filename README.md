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

## Make it go

Once all appliances are bootstrapped:

```bash
ansible-playbook playbook.yml
```
