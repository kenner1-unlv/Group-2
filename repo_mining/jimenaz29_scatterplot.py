import json
import matplotlib.pyplot as plt
from datetime import datetime

# generating scatter plot for csv file
# x-axis: weeks since the beginning of the repository
# y-axis: source files
# color: author reponsible for the changes

# saved visualization as a png
# <github_username>_file_activity.png

# adding file name to the program
repo = 'scottyab/rootbeer'
file = repo.split('/')[1]

metadataOutput = 'data/jimenaz29_authors_' + file + '.json'
plotOutput = 'jimenaz29_file_activity.png'

# loading json file obtained in authors_file_touches
with open(metadataOutput, "r") as file:
    metadata = json.load(file)

# obtaining time sets
def set_time(date):
    return datetime.fromisoformat(date.replace("Z", "+00:00"))

dates = [ set_time(change["date"]) for  data in metadata.values() for change in data["changes"] ]

begin_date = min(dates)

# creating unique list of authors
authors = set()

for data in metadata.values():
    for change in data["changes"]:
        authors.add(change["author"])

authors = list(authors)

# assigning unique colors per author variance
colors = plt.cm.tab20(range(len(authors)))

author_colors = {}

# assigning unique colors to authors
for i, author in enumerate(authors):
    author_colors[author] = colors[i % len(colors)]

# y axis as source files
files = list(metadata.keys()) 

file_pos = {}

for i, filename in enumerate(files):
    # assigning unique coordinate per file
    file_pos[filename] = i 

# creating scatterplot figure
fig, ax = plt.subplots(figsize=(10, 6))

for filename, data in metadata.items():
    y = file_pos[filename]

    for change in data["changes"]:
        cur_date = set_time(change["date"])

        weeks = (cur_date - begin_date).days // 7

        author = change["author"]

        ax.scatter( weeks, y, color=author_colors[author])

# labeling axes
ax.set_xlabel("weeks")
ax.set_ylabel("file")
ax.set_title(f"{repo} file touches by author over time")

fig.tight_layout()
fig.savefig(plotOutput, dpi=150)
plt.close(fig)
print(f"Successfully saved {plotOutput}")



