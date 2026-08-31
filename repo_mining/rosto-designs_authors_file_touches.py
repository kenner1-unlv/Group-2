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

# Collect author and change-date information for one source file
def get_file_history(repo, filename, lsttokens):
    ipage = 1
    ct = 0

    authors = set()
    dates = []
    touch_count = 0

    try:
        # Loop through all commit pages for this specific file
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

            # Stop when there are no more commits
            if len(jsonCommits) == 0:
                break

            # Collect author and date for each change
            for commitObject in jsonCommits:
                commitData = commitObject['commit']
                author = commitData['author']['name']
                date = commitData['author']['date']
                authors.add(author)
                dates.append(date)
                touch_count += 1
            ipage += 1
    except Exception as e:
        print("Error receiving data for " + filename)
        print(e)
    return authors, dates, touch_count

# GitHub repo
repo = 'scottyab/rootbeer'

# Get GitHub token from environment variable
githubToken = os.getenv("GITHUB_TOKEN")
if githubToken is None:
    print("Error: GITHUB_TOKEN environment variable is not set.")
    exit(1)
  
lstTokens = [githubToken]

# Read the source files identified in Task 1
sourceFiles = []
with open('data/file_rootbeer.csv', 'r') as fileCSV:
    reader = csv.DictReader(fileCSV)
    for row in reader:
        sourceFiles.append(row['Filename'])
print('Total number of source files: ' + str(len(sourceFiles)))

# Output file for Task 2
fileOutput = 'data/authors_file_touches_rootbeer.csv'
fileCSV = open(fileOutput, 'w', newline='')
writer = csv.writer(fileCSV)
rows = ["Filename", "Authors", "Dates", "Touches"]
writer.writerow(rows)

# Collect history for every source file
for filename in sourceFiles:
    print('Processing: ' + filename)
    authors, dates, touch_count = get_file_history(
        repo,
        filename,
        lstTokens
    )
  
    # Convert lists/sets into strings for the CSV
    authorsString = '; '.join(sorted(authors))
    datesString = '; '.join(dates)
    rows = [
        filename,
        authorsString,
        datesString,
        touch_count
    ]
    writer.writerow(rows)
fileCSV.close()
print('Author and file-touch data written to: ' + fileOutput)
