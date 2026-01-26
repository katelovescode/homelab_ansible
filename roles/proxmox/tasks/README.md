# Proxmox Tasks

Uses community proxmox module and a local copy of the `proxmox_pveum.py` script from [https://github.com/pazuzu-dev/proxmox_pveum](Proxmox PVEUM Module). I only did this this way to avoid having to use git submodules

## 1Password

A service account token for Ansible is configured in the .envrc for this repository. `direnv allow .` is required for loading in ENV vars, and once it's loaded 1Password should not ask for TouchID confirmation except at the beginning of the run for SSH connection

## A Note on Users

The tasks run on these hosts will create and configure several node and cluster attributes, and it may be a little confusing to understand which user is doing what. For clarity, here's the order of operations on a Proxmox node (after `ansible_user` role is run on all hosts in the playbook):

- `remote_user: root`
  - installs `sudo`, which isn't included in debian by default
- `enterprise_repos`
  - interacts w/ the OS to disable enterprise repos and enable no-subscription repos
  - Removing Ceph & Enterprise PVE: default `ansible` user
  - Adding No-Subscription: `remote_user: root`
  - `dist-update`: `become: true`
- `required_packages` as `ansible` with `become: true`
  - installs `pip` and `proxmoxer` so Ansible can use the `community.proxmox` modules
- `admin_user` as default `ansible` user, `become: true` on `ansible.builtin.user` and `ansible.posix.authorized_key` modules, `root` API account for proxmox actions
  - interacts w/ the OS to create an admin user, and then uses the root account's password to create an admin user and assign them administrator privileges via the Proxmox API
- `install_templates` as `ansible` with the admin account's Proxmox API credentials
  - using the admin account's password to interact with the API, installs Debian 12 template for containers

We don't have to document every step but essentially, any time we're interacting with the OS, we want to be using `ansible`, and any time we're interacting with the API we want to be using the admin account's API creds. But privilege escalation may require `become: true` or `remote_user: root` depending on which functions/files you're trying to interact with on the system.

## Possible Enhancements

- Add `ansible` user to the Proxmox API users
- Change authentication for the API to use token or ticket auth
- Add service account token permissions for SSH key to avoid TouchID auth at the beginning
- 1Password Connect server
