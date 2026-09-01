import csv
import json
import os

import requests


if not os.path.exists("data"):
    os.makedirs("data")


# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {"Authorization": "Bearer {}".format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct


def isSource(filename):
    """Return True when filename has one of the selected source extensions."""
    source_extensions = (".cpp", ".c", ".h", ".java", ".kt")
    return filename.lower().endswith(source_extensions)


# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = (
                "https://api.github.com/repos/"
                + repo
                + "/commits?page="
                + spage
                + "&per_page=100"
            )
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject["sha"]
                # For each commit, use the GitHub commit API to extract the files
                # touched by the commit.
                shaUrl = "https://api.github.com/repos/" + repo + "/commits/" + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails["files"]
                for filenameObj in filesjson:
                    filename = filenameObj["filename"]
                    dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    print(filename)
            ipage += 1
    except Exception:
        print("Error receiving data")
        raise


# Read a token securely instead of storing credentials in source code.
gh_token = os.environ.get("GITHUB_TOKEN")
if not gh_token:
    raise SystemExit("GITHUB_TOKEN is not set.")
lstTokens = [gh_token]

# GitHub repo
repo = "scottyab/rootbeer"

dictfiles = {}
countfiles(dictfiles, lstTokens, repo)
print("Total number of files: " + str(len(dictfiles)))

file = repo.split("/")[1]
# change this to the path of your file
fileOutput = "data/file_" + file + ".csv"
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, "w")
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
print("The file " + bigfilename + " has been touched " + str(bigcount) + " times.")
