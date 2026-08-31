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

def is_source_file(filename):
    # Human-written programming-language source files
    source_extensions = (
        '.java',
        '.kt',
        '.kts',
        '.c',
        '.cpp',
        '.h',
        '.hpp'
    )

    # Exclude obvious generated/build/IDE content
    excluded_directories = (
        'build/',
        'generated/',
        '.gradle/',
        '.idea/'
    )

    for directory in excluded_directories:
        if directory in filename:
            return False
    return filename.lower().endswith(source_extensions)

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # Get repository information so we can determine
        # the default branch instead of assuming "main"
        repoUrl = 'https://api.github.com/repos/' + repo
        repoData, ct = github_auth(repoUrl, lsttokens, ct)

        defaultBranch = repoData['default_branch']
        print('Default branch: ' + defaultBranch)

        # Identify programming languages used in repository
        languagesUrl = 'https://api.github.com/repos/' + repo + '/languages'
        languages, ct = github_auth(languagesUrl, lsttokens, ct)

        print('Programming languages:')
        for language in languages:
            print(' - ' + language)

        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            # use the default branch returned by GitHub
            commitsUrl = (
                'https://api.github.com/repos/' + repo +
                '/commits?sha=' + defaultBranch +
                '&page=' + spage +
                '&per_page=100'
            )

            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break

            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']

                # For each commit, use the GitHub commit API to extract
                # the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    # Only include files that satisfy our source-file definition
                    if is_source_file(filename):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
            ipage += 1

    except Exception as e:  #so you can see the error
        print("Error receiving data")
        print(e)
        exit(0)
     
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# Get the GitHub token from an environment variable instead
# of storing credentials inside the Python file.
githubToken = os.getenv("GITHUB_TOKEN")

if githubToken is None:
    print("Error: GITHUB_TOKEN environment variable is not set.")
    exit(1)
 
lstTokens = [githubToken]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of source files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w', newline='')  # small Windows CSV improvement
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
# print the final source files selected for analysis
print('\nSource files selected for analysis:')

for filename in dictfiles:
    print(filename)
if bigfilename is not None:
    print(
        'The file ' + bigfilename +
        ' has been touched ' +
        str(bigcount) +
        ' times.'
    )
