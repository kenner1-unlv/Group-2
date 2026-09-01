import csv
import json
import os

import requests


def github_auth(url, token):
    try:
        headers = {"Authorization": "Bearer " + token}
        request = requests.get(url, headers=headers)
        return json.loads(request.content)
    except Exception as error:
        print(error)
        return None


def isSource(filename):
    sourceTypes = (".cpp", ".c", ".h", ".java", ".kt")
    return filename.lower().endswith(sourceTypes)


def getDefaultBranch(token, repo):
    url = "https://api.github.com/repos/" + repo
    repoInfo = github_auth(url, token)
    return repoInfo["default_branch"]


def countfiles(dictfiles, token, repo, branch):
    page = 1

    while True:
        commitsUrl = (
            "https://api.github.com/repos/"
            + repo
            + "/commits?sha="
            + branch
            + "&page="
            + str(page)
            + "&per_page=100"
        )
        commits = github_auth(commitsUrl, token)

        if len(commits) == 0:
            break

        print("Processing page " + str(page))

        for commit in commits:
            sha = commit["sha"]
            commitUrl = "https://api.github.com/repos/" + repo + "/commits/" + sha
            commitInfo = github_auth(commitUrl, token)

            for changedFile in commitInfo["files"]:
                filename = changedFile["filename"]

                if isSource(filename):
                    dictfiles[filename] = dictfiles.get(filename, 0) + 1

        page += 1


# Read the GitHub token from the environment.
gh_token = os.environ.get("GITHUB_TOKEN")
if not gh_token:
    raise SystemExit("GITHUB_TOKEN is not set.")

repo = "scottyab/rootbeer"
branch = getDefaultBranch(gh_token, repo)

print("Default branch: " + branch)

dictfiles = {}
countfiles(dictfiles, gh_token, repo, branch)

print("Total source files: " + str(len(dictfiles)))

dataFolder = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(dataFolder, exist_ok=True)
fileOutput = os.path.join(dataFolder, "ethanvfour_file_rootbeer.csv")

fileCSV = open(fileOutput, "w", newline="")
writer = csv.writer(fileCSV)
writer.writerow(["Filename", "Touches"])

for filename, touches in sorted(dictfiles.items()):
    writer.writerow([filename, touches])
    print(filename)

fileCSV.close()
print("Saved file list to " + fileOutput)
