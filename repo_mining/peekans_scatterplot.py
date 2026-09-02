import json
from datetime import datetime
import matplotlib.pyplot as plt

with open('data/peekans_authors_rootbeer.json') as f:
    records = json.load(f)

# Parse dates (GitHub returns ISO 8601, e.g. 2015-03-02T10:15:00Z)
for r in records:
    r['parsed_date'] = datetime.strptime(r['date'], '%Y-%m-%dT%H:%M:%SZ')

startDate = min(r['parsed_date'] for r in records)

files = sorted(set(r['filename'] for r in records))
fileIndex = {f: i for i, f in enumerate(files)}

authors = sorted(set(r['author'] for r in records))
colorMap = plt.cm.get_cmap('tab20', len(authors))
authorColors = {a: colorMap(i) for i, a in enumerate(authors)}

x, y, colors = [], [], []
for r in records:
    weeks = (r['parsed_date'] - startDate).days // 7
    x.append(weeks)
    y.append(fileIndex[r['filename']])
    colors.append(authorColors[r['author']])

plt.figure(figsize=(12, 8))
plt.scatter(x, y, c=colors, alpha=0.7)
plt.xlabel('weeks')
plt.ylabel('file')
plt.title('scottyab/rootbeer file touches by Author overtime')

# Legend showing author-color mapping
handles = [plt.Line2D([0], [0], marker='o', color='w',
                       markerfacecolor=authorColors[a], markersize=8, label=a)
           for a in authors]
plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig('peekans_file_activity.png')
print('Saved peekans_file_activity.png')