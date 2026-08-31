import csv
from datetime import datetime

import matplotlib.pyplot as plt

# Input from Task 2
input_file = "data/authors_file_touches_rootbeer.csv"

output_file = "repo_mining/rosto-designs_file_activity.png"

changes = []

with open(input_file, "r") as fileCSV:
    reader = csv.DictReader(fileCSV)

    for row in reader:
        filename = row["Filename"]
        author = row["Author"]
        date = datetime.fromisoformat(
            row["Date"].replace("Z", "+00:00")
        )

        changes.append({
            "filename": filename,
            "author": author,
            "date": date
        })

if len(changes) == 0:
    print("No file-touch data found.")
    exit(1)

start_date = min(change["date"] for change in changes)
print("Beginning of repository:", start_date)

for change in changes:
    difference = change["date"] - start_date
    change["week"] = difference.days // 7
  
unique_changes = {}
for change in changes:
    key = (
        change["week"],
        change["filename"],
        change["author"]
    )

    unique_changes[key] = change

changes = list(unique_changes.values())

files = sorted(
    set(change["filename"] for change in changes)
)

file_positions = {}

for index, filename in enumerate(files):
    file_positions[filename] = index

authors = sorted(
    set(change["author"] for change in changes)
)

# Create scatter plot
plt.figure(figsize=(14, 10))

# Plot each author's changes separately so that
# the legend identifies authors
for author in authors:
    x_values = []
    y_values = []

    for change in changes:
        if change["author"] == author:
            x_values.append(change["week"])
            y_values.append(
                file_positions[change["filename"]]
            )

    plt.scatter(
        x_values,
        y_values,
        label=author,
        s=25
    )

plt.xlabel("Weeks Since Beginning of Repository")
plt.ylabel("Source Files")

plt.yticks(
    range(len(files)),
    files,
    fontsize=6
)

plt.title("RootBeer Repository Source File Activity")

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.4
)

plt.legend(
    title="Authors",
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    fontsize=7
)

plt.tight_layout()

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)
plt.close()
print("Scatter plot saved as:", output_file)
