ntp
=========

Installs and configures the NTP service on server and client machines.

Requirements
------------
FreeBSD/Ubuntu OS

Role Variables
--------------

ntp_package: the package name to use for installing ntp
ntp_mode: the ntp mode to configure, client/server

Example Playbook
----------------
```
---
- hosts: all
  connection: local
  sudo: yes
  roles:
    - ntp
  vars:
      ntp_mode: server
```

License
-------

Apache

Author Information
------------------

Stephen Garlick @ gocurb
