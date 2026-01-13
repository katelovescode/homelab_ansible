# Host Vars

## Enterprise

Files in this directory are meant to hold variables that _only_ apply to the Enterprise Proxmox installation. Secret/sensitive values go in `secrets.yml` which is gitignored and encrypted by Ansible vault. Non-sensitive variables can go in `vars.yml` or a new file.

```
# secrets.yml

ansible_host: [IP address]
trusted_gateway: [IP address]
root_api_password: "{{ '[Password String]' }}"
admin_api_password: "{{ '[Password String]' }}"
admin_username: [Username string]
admin_authentication_realm: [pam/pve]
admin_email: [email for admin user]
admin_password: "{{ '[Password String]' | password_hash('sha512') }}"
admin_public_key: [ssh-ed25519 AAAAC...]
pihole_1_root_password: "{{ '[Password String]' }}"
pihole_1_ip_address: [IP address]
```
