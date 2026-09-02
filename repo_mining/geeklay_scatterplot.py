import matplotlib.pyplot as plot
import json
from datetime import datetime
from sys import version as sysv, version_info as sysvinfo
from collections import Counter

__mmpyversion = sysvinfo[:2]

filepaths = ["data/geeklay_authors_rootbeer.json",
         "geeklay_file_activity.png"
         ]

def convert_date(date):
    return datetime.fromisoformat(date) if __mmpyversion >= (3,11) else datetime.fromisoformat(date.replace("Z", "+00:00"))

with open(filepaths[0], "r") as file: 
    data = json.load(file)

first_commit = convert_date(min([j["date"] for e in data for j in e["commits"]]))

colormap = plot.get_cmap("Paired")

# authors: total commits
authors = Counter(i for i in [p.get('author') for q in data for p in q.get('commits')])
# sort..
authors = {k: v for k,v in (sorted(authors.items(), key=lambda item: item[1], reverse=True))}

paths = [i.get('path') for i in data]
files = {name: ind for ind, name in enumerate(paths)}
author_colors = {author: colormap(i % colormap.N) for i, author in enumerate(authors)}

x = []
y = []
colors = []
temp = set()

figure, axis = plot.subplots(figsize=(15,10))

for i, entry in enumerate(data):
    for commit in entry["commits"]:
        # could have this be the filenames themselves instead of indices
        x = ((convert_date(commit["date"]) - first_commit).days //7)
        y = (files.get(entry['path']))
        colors.append(author_colors.get(commit['author']))
        axis.scatter(x,y, c = author_colors.get(commit['author']), s=25,
                      label = f"{commit['author']}" if commit['author'] not in temp else "")
        temp.add(commit['author']) 

axis.set_xlabel("weeks")
axis.set_ylabel("files")
axis.set_title("Rootbeer Files Touched by Contributors Over Time")
figure.legend(title="authors",
              loc="center right",
              fontsize=8,
              title_fontsize=10)
figure.savefig(filepaths[1], dpi=96)
plot.close(figure)
print(f"Scatterplot saved to {filepaths[1]}")

