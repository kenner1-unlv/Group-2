import os 
import csv
import requests 
import json
from datetime import datetime
from collections import Counter

dotenvpath = os.getcwd() + "/.env"
if os.path.exists(dotenvpath):
    from dotenv import load_dotenv
    load_dotenv(dotenvpath)

if 'GIT_TOKEN' in os.environ or 'GITHUB_TOKEN' in os.environ: 
    token = os.getenv('GIT_TOKEN') if os.getenv('GIT_TOKEN') else os.getenv('GITHUB_TOKEN')
else: 
    print("Github token not supplied. Set GIT_TOKEN or GITHUB_TOKEN.\n" +
          "export GIT_TOKEN=... or export GITHUB_TOKEN=...")
    exit(1)

if not token:
    print("Error with token envvar.")
    exit(1)

# Github API request
def github_auth(url, token, params=None):
    headers = {"Authorization": f"Bearer {token}"}
    request = requests.get(url, headers=headers, params=params, timeout=10)
    request.raise_for_status();
    return request.json()

repo = "scottyab/rootbeer"
branch = "master"

# Paths array
paths = ["data/geeklay_file_rootbeer.csv", 
         "data/geeklay_authors_rootbeer.json"]

def get_commits(path, token):
    commits = list()
    pageno = 1

    while True:    
        #commiturl = f"https://api.github.com/repos/{repo}/commits?page={pageno}&per_page=100&sha={branch}&path={path}"
        commiturl = f"https://api.github.com/repos/{repo}/commits"
        params = {"page": pageno, "per_page": 100, "sha": branch, "path": path}
        commit = github_auth(commiturl, token, params)
        if not commit:
            break
        for i in commit:
            commitinfo = i.get("commit").get("author")
            commits.append({"author": commitinfo.get("name"), "date": commitinfo.get("date")})
        pageno += 1
    return commits

def get_paths(path):
    paths = list()
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            fn = row.get("Filename")
            if fn:
                paths.append(fn)
    return paths

def print_info(data):
    authors = Counter(i.get('author') for i in [p for q in data for p in q.get('commits')])
    tcommits = sum(authors.values())
    # Yes, this is horrendous.
    pctcontri = {k: v for k,v in
                       sorted({k: v/tcommits*100 for k,v in authors.items()}.items(),
                       key=lambda v: v[1],
                       reverse=True)}
    print("Contributors + Commits:\n", authors)
    print("Total Commits:\t", tcommits)
    print("Percentage Contribution:\n", pctcontri)
  # with open("usefuldata", "w") as file:
  #     dt = {"Total Commits": tcommits,
  #           "Authors/Contributors": authors,
  #           "Percent Contribution": pctcontri
  #           }
  #     json.dump(dt, file, indent=4)

res = list()

for path in get_paths(paths[0]):
    print("fetching commits for {}".format(path))
    commits = get_commits(path, token)
    res.append({"path": path,
                "touches": len(commits),
                "commits": commits,
                })

print_info(res)

with open(paths[1], "w") as file:
    json.dump(res, file, indent=4)

