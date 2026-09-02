import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

def github_auth(url, lstTokens, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lstTokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

def is_source(filename):
    return filename.endswith((".java", ".kt", ".xml"))

# @repo, the repo we want to extract info from
# @dictFiles, empty dictionary of files
# @tokens, Github authentication tokens
def get_authors(repo, dictfiles, tokens, ct):
    ipage = 1       # url page counter
    authors = []    # get authors

    try:
        # loop throug all repos
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?path=' + dictfiles + '&page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, tokens, ct)

            # break if not
            if not jsonCommits:
                break

            # iterate through list
            for c in jsonCommits:
                # get commit info
                c_info = c["commit"]["author"]
                authors.append((c_info["name"], c_info["date"]))
            ipage += 1   # next page
    
    except:
        print("Error getting data from repos")
        exit(0)

    return authors, ct 

# repo for rootbeer
repo = 'scottyab/rootbeer'

# Token 
lstTokens = ["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"]

# create and read file names into file
fs = []
with open("data/file_rootbeer.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if is_source(row["Filename"]):
            fs.append(row["Filename"])

# write to output
out = "data/authors_rootbeer.csv"
ct = 0
with open(out, "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["Filename", "Author", "Date"])
    for f in fs:
        history, ct = get_authors(repo, f, lstTokens, ct)
        for author, date in history:
            writer.writerow([f, author, date])
            
            