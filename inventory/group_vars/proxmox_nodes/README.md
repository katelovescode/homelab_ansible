# Group Vars

## Proxmox Nodes

Files in this directory are meant to hold variables that _only_ apply to the Proxmox nodes. Secret/sensitive values go in `secrets.yml` which is gitignored and encrypted by Ansible vault. Non-sensitive variables can go in `vars.yml` or a new file.

```
# secrets.yml

proxmox_admin_username: [Username]
proxmox_admin_authentication_realm: [pam/pve]
proxmox_admin_email: [email]
proxmox_admin_password: "{{ '[Password String]' }}"
proxmox_admin_hashed_password: "{{ '[Password String]' | password_hash('sha512') }}"
```
