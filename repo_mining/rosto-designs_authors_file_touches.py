import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# Collect author and date information for one source file
def get_file_history(repo, filename, lsttokens):
    ipage = 1
    ct = 0
    changes = []
    try:
        # Loop through every page of commits for this file
        while True:
            spage = str(ipage)
            commitsUrl = (
                'https://api.github.com/repos/' + repo +
                '/commits?path=' + filename +
                '&page=' + spage +
                '&per_page=100'
            )

            jsonCommits, ct = github_auth(
                commitsUrl,
                lsttokens,
                ct
            )

            # No more commits
            if len(jsonCommits) == 0:
                break
            for commitObject in jsonCommits:
                commitData = commitObject['commit']
                author = commitData['author']['name']
                date = commitData['author']['date']
                changes.append([author, date])
            ipage += 1
    except Exception as e:
        print("Error receiving data for " + filename)
        print(e)
    return changes

# GitHub repo
repo = 'scottyab/rootbeer'

# Get GitHub token from environment variable
githubToken = os.getenv("GITHUB_TOKEN")
if githubToken is None:
    print("Error: GITHUB_TOKEN environment variable is not set.")
    exit(1)

lstTokens = [githubToken]

# Read source files identified by Task 1
sourceFiles = []
with open('data/file_rootbeer.csv', 'r') as fileCSV:
    reader = csv.DictReader(fileCSV)
    for row in reader:
        sourceFiles.append(row['Filename'])
        
print('Total number of source files: ' + str(len(sourceFiles)))

# Task 2 output
fileOutput = 'data/authors_file_touches_rootbeer.csv'
fileCSV = open(fileOutput, 'w', newline='')
writer = csv.writer(fileCSV)
writer.writerow([
    "Filename",
    "Author",
    "Date",
    "Touches"
])

# Process every source file
for filename in sourceFiles:
    print('Processing: ' + filename)
    changes = get_file_history(
        repo,
        filename,
        lstTokens
    )

    # Number of commits that changed this file
    touch_count = len(changes)

    # Write one row for every change
    for change in changes:
        author = change[0]
        date = change[1]
        writer.writerow([
            filename,
            author,
            date,
            touch_count
        ])
        
fileCSV.close()
print(
    'Author and file-touch data written to: '
    + fileOutput
)
