import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

# adding file name to the program
repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
fileOutput = 'data/jimenaz29_file_' + file + '.csv'

metadataOutput = 'data/jimenaz29_authors_' + file + '.json'

# reading the created csv file
target_files = set()

with open(fileOutput, mode='r') as file:
    reader = csv.DictReader(file)

    # isolating filenames as a target for processing
    for row in reader:
        target_files.add(row["Filename"]) 


# GitHub Authentication function
# copied over from collect_files.py
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
# copied over from collect_files.py 
# modified to save metadata: 
# (file path, authors, dates, and number of changes)
def saveMetadatafiles(dictfiles, lsttokens, repo, target_files):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
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
                
                # Obtain information per file
                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']
                
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    # collect files that were identified as src files
                    # in collect_files.py 
                    if filename not in target_files:
                        continue

                    # creating default frame for a new entry
                    if filename not in dictfiles:
                        dictfiles[filename] = {
                            "changes": [],
                            "times_changed": 0
                        }

                    # storing metadata
                    dictfiles[filename]["changes"].append({
                        "author": author,
                        "date": date
                    })
                    dictfiles[filename]["times_changed"] += 1

                    print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# token request
lstTokens = [input("Enter Jimenaz29 Token: ")]

dictfiles = dict()
saveMetadatafiles(dictfiles, lstTokens, repo, target_files)

rows = ["File Path", "Authors", "Dates of Changes", "Times Changed"]

# saving as JSON file

with open(metadataOutput, 'w') as file:
    json.dump(dictfiles, file, indent=3)


