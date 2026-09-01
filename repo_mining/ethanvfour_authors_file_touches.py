import csv
import json
import os

import requests


def github_auth(url, token):
    headers = {"Authorization": "Bearer " + token}
    request = requests.get(url, headers=headers)
    return json.loads(request.content)


def getDefaultBranch(token, repo):
    url = "https://api.github.com/repos/" + repo
    repoInfo = github_auth(url, token)
    return repoInfo["default_branch"]


def getSourceFiles(csvFile):
    sourceFiles = []

    fileCSV = open(csvFile, "r")
    reader = csv.DictReader(fileCSV)

    for row in reader:
        sourceFiles.append(row["Filename"])

    fileCSV.close()
    return sourceFiles


def getFileChanges(filename, token, repo, branch):
    changes = []
    page = 1

    while True:
        url = (
            "https://api.github.com/repos/"
            + repo
            + "/commits?sha="
            + branch
            + "&path="
            + filename
            + "&page="
            + str(page)
            + "&per_page=100"
        )
        commits = github_auth(url, token)

        if len(commits) == 0:
            break

        for commit in commits:
            author = commit["commit"]["author"]["name"]
            date = commit["commit"]["author"]["date"]

            changes.append(
                {
                    "author": author,
                    "date": date,
                }
            )

        page += 1

    return changes


gh_token = os.environ.get("GITHUB_TOKEN")
if not gh_token:
    raise SystemExit("GITHUB_TOKEN is not set.")

repo = "scottyab/rootbeer"
branch = getDefaultBranch(gh_token, repo)

dataFolder = os.path.join(os.path.dirname(__file__), "data")
csvFile = os.path.join(dataFolder, "ethanvfour_file_rootbeer.csv")
jsonFile = os.path.join(dataFolder, "ethanvfour_authors_rootbeer.json")

sourceFiles = getSourceFiles(csvFile)
results = []

for filename in sourceFiles:
    print("Collecting changes for " + filename)
    changes = getFileChanges(filename, gh_token, repo, branch)
    authors = []
    dates = []

    for change in changes:
        if change["author"] not in authors:
            authors.append(change["author"])
        dates.append(change["date"])

    results.append(
        {
            "path": filename,
            "authors": authors,
            "dates": dates,
            "touches": len(changes),
            "changes": changes,
        }
    )

outputFile = open(jsonFile, "w")
json.dump(results, outputFile, indent=2)
outputFile.close()

print("Saved author and file-touch data to " + jsonFile)
