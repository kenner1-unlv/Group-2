"""
Create a scatter plot of Rootbeer source-file activity.

Plot encoding
-------------
X-axis: weeks since the repository's first default-branch commit
Y-axis: selected source files
Color: author responsible for the change

Each point represents one author changing one source file during one week.
Multiple commits by the same author to the same file in the same week are
collapsed into one point so the visualization follows the assignment's stated
unit of analysis.
"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib

# Use a noninteractive backend so the script reliably saves an image when run
# from Git Bash without requiring a plotting window.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
INPUT_FILE = (
    SCRIPT_DIRECTORY
    / "data"
    / "kenner1-unlv_authors_rootbeer.json"
)
OUTPUT_FILE = SCRIPT_DIRECTORY / "kenner1-unlv_file_activity.png"


def parse_github_date(date_text):
    """Convert GitHub's ISO 8601 timestamp into a datetime object."""
    return datetime.fromisoformat(
        date_text.replace("Z", "+00:00")
    )


def shorten_file_path(file_path):
    """
    Shorten long historical paths while preserving component and era.

    Prefixes distinguish current library/sample code from legacy rootchecker,
    JNI, native, and test paths without requiring unreadably long y-axis labels.
    """
    replacements = {
        "app/src/main/java/com/scottyab/rootbeer/sample/": "sample/",
        "app/src/main/java/com/scottyab/rootchecker/": "legacy/rootchecker/",
        "app/src/androidTest/java/com/scottyab/rootbeer/": "test/app/",
        "app/src/androidTest/java/com/scottyab/rootchecker/": (
            "test/legacy-app/"
        ),
        "rootbeerlib/src/main/java/com/scottyab/rootbeer/": "library/",
        "rootbeerlib/src/test/java/com/scottyab/rootbeer/": "test/library/",
        "rootbeerlib/src/androidTest/java/com/scottyab/rootbeer/": (
            "test/library-android/"
        ),
        "rootbeerlib/src/main/cpp/": "native/current/",
        "rootbeerlib/src/main/jni/": "native/main-jni/",
        "rootbeerlib/jni/": "native/legacy-library/",
        "app/jni/": "native/legacy-app/",
    }

    for prefix, replacement in replacements.items():
        if file_path.startswith(prefix):
            return file_path.replace(prefix, replacement, 1)

    return file_path


def load_activity_data():
    """Load and minimally validate the Task 2 JSON data."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Run the author/file-touch collector first: {INPUT_FILE}"
        )

    with INPUT_FILE.open(encoding="utf-8") as json_file:
        data = json.load(json_file)

    required_fields = {
        "repository",
        "repository_start_date",
        "files",
    }

    missing_fields = required_fields.difference(data)

    if missing_fields:
        raise ValueError(
            f"Input JSON is missing required fields: "
            f"{sorted(missing_fields)}"
        )

    return data


def build_weekly_points(data):
    """
    Convert commit events into unique author-file-week observations.

    A set performs the required aggregation: if one author changes one file
    several times during the same week, only one plotted point remains.
    """
    repository_start = parse_github_date(
        data["repository_start_date"]
    )

    weekly_points = set()

    for file_data in data["files"]:
        file_path = file_data["path"]

        for change in file_data["changes"]:
            change_date = parse_github_date(change["date"])
            week = (change_date - repository_start).days // 7

            weekly_points.add(
                (
                    week,
                    file_path,
                    change["author"],
                )
            )

    return weekly_points


def create_scatter_plot(data, weekly_points):
    """Create and save the required author-colored scatter plot."""
    # Rank files by total touches. Sorting from low to high places the most
    # frequently changed files near the top of the finished chart.
    touch_counts = {
        file_data["path"]: file_data["touches"]
        for file_data in data["files"]
    }

    ordered_files = sorted(
        touch_counts,
        key=lambda file_path: (
            touch_counts[file_path],
            file_path.lower(),
        ),
    )

    file_positions = {
        file_path: position
        for position, file_path in enumerate(ordered_files)
    }

    # Rank authors by plotted observations to keep the most active authors
    # first in the legend.
    author_point_counts = Counter(
        author
        for _, _, author in weekly_points
    )
    ordered_authors = [
        author
        for author, _ in author_point_counts.most_common()
    ]

    color_map = plt.colormaps["tab20"]
    author_colors = {
        author: color_map(index % color_map.N)
        for index, author in enumerate(ordered_authors)
    }

    figure, axis = plt.subplots(
        figsize=(18, 10.5),
        constrained_layout=True,
    )

    for author in ordered_authors:
        author_points = [
            (week, file_path)
            for week, file_path, point_author in weekly_points
            if point_author == author
        ]

        x_values = [
            week
            for week, _ in author_points
        ]
        y_values = [
            file_positions[file_path]
            for _, file_path in author_points
        ]

        axis.scatter(
            x_values,
            y_values,
            color=author_colors[author],
            label=f"{author} ({len(author_points)})",
            s=34,
            alpha=0.82,
            edgecolors="white",
            linewidths=0.35,
        )

    axis.set_yticks(range(len(ordered_files)))
    axis.set_yticklabels(
        [
            f"{shorten_file_path(file_path)} "
            f"({touch_counts[file_path]} touches)"
            for file_path in ordered_files
        ],
        fontsize=6.8,
    )

    axis.set_xlabel(
        "Weeks since repository beginning",
        fontsize=11,
    )
    axis.set_ylabel(
        "Source files",
        fontsize=11,
    )
    axis.set_title(
        "Rootbeer Source-File Activity by Author and Week",
        fontsize=14,
        weight="bold",
    )

    axis.grid(
        axis="x",
        linestyle="--",
        alpha=0.3,
    )
    axis.set_axisbelow(True)

    axis.legend(
        title="Author (weekly points)",
        bbox_to_anchor=(1.01, 1),
        loc="upper left",
        fontsize=7,
        title_fontsize=8,
        frameon=True,
        ncol=1,
    )

    figure.savefig(
        OUTPUT_FILE,
        dpi=240,
        bbox_inches="tight",
    )
    plt.close(figure)


def main():
    """Load the Task 2 data, aggregate it by week, and create the plot."""
    data = load_activity_data()
    weekly_points = build_weekly_points(data)

    if not weekly_points:
        raise RuntimeError("No activity points were available to plot.")

    create_scatter_plot(
        data,
        weekly_points,
    )

    authors = {
        author
        for _, _, author in weekly_points
    }

    weeks = [
        week
        for week, _, _ in weekly_points
    ]

    print(f"Input change events: {sum(f['touches'] for f in data['files'])}")
    print(f"Unique weekly points: {len(weekly_points)}")
    print(f"Authors represented: {len(authors)}")
    print(f"Repository week range: {min(weeks)} to {max(weeks)}")
    print(f"Visualization written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()