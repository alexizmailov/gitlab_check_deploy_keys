#!/usr/bin/env python3

import argparse, json
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser(description="GitLab Deploy Key checker")
parser.add_argument('-H', help='GitLab url/ip')
parser.add_argument('--token', help='Secret token for accessing GitLab API')
parser.add_argument('--puppetfile', help='GitLab group ID or name to check (incompatible with --group)')
parser.add_argument('--keyid', help='Key ID to check(single key, or comma separated list)')
args = parser.parse_args()

if args.H:
  GITLAB_URL = 'https://{}'.format(args.H)
else:
  print ("No Gitlab url provided, use -H")
  exit(1)

if args.token:
  TOKEN = args.token
else:
  print ("No private token provided, use --token")
  exit(1)

if args.puppetfile:
  PUPPETFILE_URL = args.puppetfile
else:
  print ("No Puppetfile url provided, use --puppetfile")
  exit(1)

if args.keyid:
  deploy_key_list = args.keyid.split(',')
else:
  print ("No deploy key IDs provided, use --keyid")
  exit(1)



def get_data(REQUEST, return_json = True):
  API_REQUEST = "%s%s" % (GITLAB_URL, REQUEST)
  response = Request(API_REQUEST)
  response.add_header('PRIVATE-TOKEN', TOKEN)
  try:
    data = urlopen(response).read().decode('utf-8')
  except:
    print ("URL not found: {}".format(API_REQUEST))
    exit(2)
  if return_json:
     return json.loads(data)
  else:
    return data



PUPPETFILE = get_data(PUPPETFILE_URL, False)
modules = PUPPETFILE.split('\n')
projects = {'systems':[], 'mirrors':[]}

for line in modules:
  if 'git@' in line and not '#' in line:
    path_name = line.replace("'",'').replace(',','').replace('.git', '').split(':')[2]
    group, name = path_name.split("/")
    if not projects[group]:
      projects[group] = []
    projects[group].append(name)


repo_list = {}
for group in projects.keys():
  result = get_data('/api/v4/groups/{}'.format(group))
  repos = result['projects']
  for repo in repos:
    if repo['name'] in projects[group]:
      #print (repo['name'], repo['id'])
      repo_list[repo['id']] = repo['name']

missing_keys = []
for item in repo_list.keys():
  request = "/api/v4/projects/{}/deploy_keys".format(item)
  result = get_data(request)
  key_list = ''
  for key in result:
    key_list += str((key['id']))
  if not any(key in key_list for key in deploy_key_list):
    missing_keys.append(repo_list[item])


if len(missing_keys) > 0:
  print ("Deploy key is missing on {} repos: {}".format(len(missing_keys), ','.join(missing_keys)))
  exit(2)
else:
  print ("OK: {} repos checked, all repos have their deploy keys".format(len(repo_list.keys())))
  exit(0)

