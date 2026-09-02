import json
import requests
import csv

import os
# Just for safety reasons, good practice
import getpass

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        repo_url = 'https://api.github.com/repos/' + repo
        repo_info, ct = github_auth(repo_url, lsttokens, ct)
        default_branch = repo_info.get('default_branch', 'master')
        print(f"Tracking commits on default branch: {default_branch}")

        # Core source file extensions
        valid_extensions = ('.java', '.kt', '.c', '.cpp', '.h')
        
        # Substrings indicating generated or compiled artifacts to exclude
        excluded_substrings = ['/build/', '/generated/', '/bin/', 'BuildConfig.java', 'R.java']
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                if 'files' in shaDetails:
                    filesjson = shaDetails['files']
                    for filenameObj in filesjson:
                        filename = filenameObj['filename']
                        
                        # 1. Check if it has a valid source code extension
                        if filename.endswith(valid_extensions):
                            # 2. Check if it is NOT a generated or compiled file
                            if not any(excluded in filename for excluded in excluded_substrings):
                                dictfiles[filename] = dictfiles.get(filename, 0) + 1
                                print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# Retrieve tokens securely from environment or prompt
token_env = os.environ.get('GITHUB_TOKENS')
if token_env:
    lstTokens = [t.strip() for t in token_env.split(',')]
else:
    token_input = getpass.getpass("Enter GitHub Personal Access Token(s) (comma-separated): ")
    lstTokens = [t.strip() for t in token_input.split(',')]

if not lstTokens or not lstTokens[0]:
    print("No tokens provided. Exiting.")
    exit(1)

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
