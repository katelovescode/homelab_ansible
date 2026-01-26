# Host Vars

## Enterprise

Files in this directory are meant to hold variables that _only_ apply to the Enterprise host. Secret/sensitive values go in `secrets.yml` which is gitignored and encrypted by Ansible vault. Non-sensitive variables can go in `vars.yml` or a new file.

```
# secrets.yml

proxmox_root_password: "{{ '[Password String]' }}"
```
