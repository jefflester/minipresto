# System-Level Ranger Access Control Module
This module provisions a Ranger server and Postgres database for Ranger storage. It is an unsecured deployment without SSL or an authentication mechanism.

## Requirements
- Starburst Data license 
- Access to Starburst Data Harbor repository for Docker images

## Sample Usage
To provision this module, run:

```shell
minipresto provision --security system-ranger
```

## Policies
- Bob: admin access to TPCH `sf100` schema
- Alice: admin access to TPCH `sf10` schema
- System: all users have select/ownership access to `system` catalog

## Accessing Ranger
- Go to `localhost:6080`
- Sign in with user: admin and pass: prestoRocks15
