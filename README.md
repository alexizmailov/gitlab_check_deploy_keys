# gitlab_check_deploy_keys
Nagios check for puppet modules - makes sure all projects have deploy keys enabled

This script parses your Puppetfile and makes sure all modules in it can be deployed using r10k

Uses GitLab API

License: Apache 2.0

gitlab_check_deploy_keys.py -H gitlab_host --token SOME_SECRET --puppetfile /your_repo/raw/production/Puppetfile --keyid 109
* -H - your GitLab hostname
* --token - Secret token for accessing GitLab API
* --puppetfile - relative url of your Puppetfile in GitLab repo, e.g. ```/your_repo/raw/production/Puppetfile```
* --keyid - Key ID to check(single key, or comma separated list)
