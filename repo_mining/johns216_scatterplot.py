import pandas as pd
from matplotlib import pyplot as plt
import random
from datetime import datetime

x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = [125, 32, 54, 253, 67, 87, 233, 56, 67]

def generate_random_hex_color():
    """Generates a random hexadecimal color code."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # Convert to hex and format with leading zeros if necessary
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    return hex_color

df = pd.read_csv("data/authors_rootbeer.csv")

# formatting
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)

# get authors and filenames
authors = df["Author"].unique()
files = df["Filename"].unique()

# start the plot formmatted by year
file_type = {file: i for i, file in enumerate(files)}
for author in authors:
    adf = df[df["Author"] == author]
    y = adf["Week"]
    x = adf["Filename"].map(file_type)
    # randomize color
    color = generate_random_hex_color()
    plt.scatter(y, x, s=150, c=[color], label=author)

# plot the chart 
plt.title("Author file touches")
plt.xlabel("Weeks since beginning of the repository")
plt.ylabel("Source Files")

plt.show()
