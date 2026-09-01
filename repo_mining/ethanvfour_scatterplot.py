import json
import os
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.style.use("classic")


def getDate(date):
    return datetime.fromisoformat(date.replace("Z", "+00:00"))


dataFolder = os.path.join(os.path.dirname(__file__), "data")
jsonFile = os.path.join(dataFolder, "ethanvfour_authors_rootbeer.json")
imageFile = os.path.join(os.path.dirname(__file__), "ethanvfour_file_activity.png")

inputFile = open(jsonFile, "r")
filesData = json.load(inputFile)
inputFile.close()

if len(filesData) == 0:
    raise SystemExit("No file activity data was found.")

allDates = []
for fileInfo in filesData:
    for change in fileInfo["changes"]:
        allDates.append(getDate(change["date"]))

startDate = min(allDates)
fileNames = []
authorPoints = {}
seenPoints = set()

for fileNumber, fileInfo in enumerate(filesData):
    fileNames.append(fileInfo["path"])

    for change in fileInfo["changes"]:
        author = change["author"]
        week = (getDate(change["date"]) - startDate).days // 7
        point = (week, fileNumber, author)

        if point in seenPoints:
            continue

        seenPoints.add(point)

        if author not in authorPoints:
            authorPoints[author] = {"weeks": [], "files": []}

        authorPoints[author]["weeks"].append(week)
        authorPoints[author]["files"].append(fileNumber)

plt.figure(figsize=(12, 8))

for author, points in authorPoints.items():
    plt.scatter(points["weeks"], points["files"], label=author, s=25)

plt.xlabel("Weeks since beginning of repository")
plt.ylabel("Source files")
plt.title("Rootbeer Source File Activity")
plt.yticks(range(len(fileNames)), fileNames, fontsize=6)
plt.legend(title="Authors", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(imageFile, dpi=150)
plt.close()

print("Saved scatter plot to " + imageFile)
