import json
import requests
import csv
import os
import getpass

if not os.path.exists("data"):
    os.makedirs("data")

def github_auth(url, lsttokens, ct):
    jsonData = None
    try:
        ct = ct % len(lsttokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

def get_default_branch(repo, lsttokens, ct):
    url = 'https://api.github.com/repos/' + repo
    data, ct = github_auth(url, lsttokens, ct)
    return data.get('default_branch', 'master'), ct

def get_touches_for_file(repo, path, branch, lsttokens, ct):
    """Return one record per commit that touched this file:
    filename, author, date. Filtering commits by path via the
    GitHub API avoids re-scanning every commit for every file."""
    touches = []
    ipage = 1
    while True:
        url = ('https://api.github.com/repos/' + repo + '/commits'
               '?path=' + path + '&sha=' + branch +
               '&page=' + str(ipage) + '&per_page=100')
        commits, ct = github_auth(url, lsttokens, ct)
        if not commits:
            break
        for c in commits:
            commitInfo = c.get('commit', {})
            authorInfo = commitInfo.get('author', {})
            author = None
            # Prefer GitHub username when available, fall back to commit name
            if c.get('author'):
                author = c['author'].get('login')
            if not author:
                author = authorInfo.get('name', 'unknown')
            date = authorInfo.get('date')
            touches.append({
                "filename": path,
                "author": author,
                "date": date
            })
        ipage += 1
    return touches, ct

# Load source files identified in Task 1
sourceFilesCsv = 'data/peekans_file_rootbeer.csv'
sourceFiles = []
with open(sourceFilesCsv, newline='') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        sourceFiles.append(row[0])

repo = 'scottyab/rootbeer'

# Retrieve tokens securely from environment or prompt
token_env = os.environ.get('PEEKANS_GH_TOKENS')
if token_env:
    lstTokens = [t.strip() for t in token_env.split(',')]
else:
    token_input = getpass.getpass("Enter GitHub Personal Access Token(s) (comma-separated): ")
    lstTokens = [t.strip() for t in token_input.split(',')]

if not lstTokens or not lstTokens[0]:
    print("No tokens provided. Exiting.")
    exit(1)

ct = 0
branch, ct = get_default_branch(repo, lstTokens, ct)
print('Default branch: ' + branch)

allTouches = []
for path in sourceFiles:
    touches, ct = get_touches_for_file(repo, path, branch, lstTokens, ct)
    allTouches.extend(touches)
    print(path + ': ' + str(len(touches)) + ' touches')

outputFile = 'data/peekans_authors_rootbeer.json'
with open(outputFile, 'w') as f:
    json.dump(allTouches, f, indent=2)

print('Total touch records: ' + str(len(allTouches)))
print('Output written to: ' + outputFile)