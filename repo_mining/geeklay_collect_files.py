import json
import requests
import csv
import os
from pathlib import Path

if not os.path.exists("data"):
 os.makedirs("data")

if 'GIT_TOKEN' in os.environ or 'GITHUB_TOKEN' in os.environ: 
    token = os.getenv('GIT_TOKEN') if os.getenv('GIT_TOKEN') else os.getenv('GITHUB_TOKEN')
else: 
    print("Github token not supplied. Set GIT_TOKEN or GITHUB_TOKEN.\n" +
          "export GIT_TOKEN=... or export GITHUB_TOKEN=...")
    exit(1)

if not token:
    print("Error with token envvar.")
    exit(1)

# GitHub Authentication function
def github_auth(url, token, params=None):
    jsonData = None
    try:
        headers = {'Authorization': 'Bearer {}'.format(token)}
        request = requests.get(url, headers=headers, params=params)
        jsonData = json.loads(request.content)
    except Exception as e:
        pass
        print(e)
    return jsonData

srcfile_exts = ['.java', '.kt', '.cpp', '.hpp', '.c', '.h']

def is_src(filename):
    return any(Path(filename).suffix == ext for ext in srcfile_exts)

# @dictFiles, empty dictionary of files
# @token, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, token, repo, branch):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            #commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100&sha=' + branch
            commitsUrl = f'https://api.github.com/repos/{repo}/commits'
            params = { "page": spage, "per_page": 100, "sha": branch }
            jsonCommits = github_auth(commitsUrl, token, params)
            author_frequency = dict()
            author_name = str()

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails = github_auth(shaUrl, token)
                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if is_src(filename):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print("\u25CB\t" + filename)
                    else:
                        print("\u2718\t" + filename)

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

def langsused(repo):
    url = 'https://api.github.com/repos/' + repo + '/languages'
    return [f"{l}\t\t{li}" for l, li in  github_auth(url, token).items()]

def defaultbranch(repo):
    url = 'https://api.github.com/repos/' + repo 
    return github_auth(url, token)['default_branch']
        

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


dictfiles = dict()
branch = defaultbranch(repo)
countfiles(dictfiles, token, repo, branch)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/geeklay_file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None

# file extensions to add to csv, ignore png,xml etc...
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()

print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')

print("\n" + "Default branch: " + branch + "\n")
print("\nLanguage\tLines")
for i in langsused(repo):
    print(i)



