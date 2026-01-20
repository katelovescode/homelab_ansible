# Host Vars

## Andromeda

Files in this directory are meant to hold variables that _only_ apply to the Andromeda host. Secret/sensitive values go in `secrets.yml` which is gitignored and encrypted by Ansible vault. Non-sensitive variables can go in `vars.yml` or a new file.

```
# secrets.yml

ansible_host: [IP address]
```
