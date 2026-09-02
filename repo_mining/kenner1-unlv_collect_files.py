"""
Collect historical source-file activity from scottyab/rootbeer.

Assignment scope
----------------
This script adapts the provided CollectFiles.py starter script to:

1. Read GitHub credentials from an environment variable.
2. Discover the repository's default branch dynamically.
3. Scan the complete default-branch commit history.
4. Select source paths using a documented extension-based definition.
5. Preserve paths for files later renamed, moved, or deleted.
6. Count one touch when one commit changes one source path.
7. Produce a username-specific CSV for later analysis.

Source-file definition
----------------------
A source file is any implementation, header, or test path encountered in the
default-branch history ending in:

    .java, .kt, .cpp, .c, .h

Tests are included because they are maintained executable source. Documentation,
images, configuration, compiled artifacts, and generated output are excluded.

Limitation
----------
Extension-based filtering can miss source written in an unlisted language or
include generated code using a recognized extension. Renamed or moved files are
treated as separate historical paths.
"""

import csv
import os
from pathlib import Path

import requests


REPOSITORY = "scottyab/rootbeer"
SOURCE_EXTENSIONS = {".java", ".kt", ".cpp", ".c", ".h"}

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = SCRIPT_DIRECTORY / "data"
OUTPUT_FILE = DATA_DIRECTORY / "kenner1-unlv_file_rootbeer.csv"

API_BASE_URL = "https://api.github.com"


def create_headers():
    """
    Build authenticated GitHub API headers.

    The token is read at runtime so no credential is stored in source code,
    generated data, screenshots, or commit history.
    """
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        raise RuntimeError(
            "GITHUB_TOKEN is not set. Export it before running this script."
        )

    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def github_get(url, params=None):
    """
    Request JSON from GitHub and report failures clearly.

    The starter script suppressed exceptions. This version stops on HTTP,
    authentication, and rate-limit failures so incomplete results are not
    silently accepted.
    """
    response = requests.get(
        url,
        headers=create_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_default_branch(repository):
    """
    Discover the default branch instead of assuming main or master.

    Rootbeer currently uses master, but the assignment requires the script to
    determine that value dynamically.
    """
    repository_data = github_get(
        f"{API_BASE_URL}/repos/{repository}"
    )
    return repository_data["default_branch"]


def is_source_file(file_path):
    """Apply the documented, case-insensitive source extension filter."""
    return Path(file_path).suffix.lower() in SOURCE_EXTENSIONS


def collect_historical_file_touches(repository, branch):
    """
    Discover and count source paths across the complete branch history.

    The provided starter script discovers files by scanning commits. This
    preserves historical paths even when files were later renamed, moved, or
    deleted. One touch represents one commit changing one source path.
    """
    touches = {}
    page = 1

    while True:
        commits = github_get(
            f"{API_BASE_URL}/repos/{repository}/commits",
            params={
                "sha": branch,
                "page": page,
                "per_page": 100,
            },
        )

        if not commits:
            break

        print(f"Processing commit page {page}...")

        for commit in commits:
            # Commit-list responses omit the complete changed-file list, so
            # each commit must be requested individually.
            commit_details = github_get(
                f"{API_BASE_URL}/repos/{repository}/commits/"
                f"{commit['sha']}"
            )

            for changed_file in commit_details.get("files", []):
                file_path = changed_file["filename"]

                if is_source_file(file_path):
                    touches[file_path] = touches.get(file_path, 0) + 1

        page += 1

    if not touches:
        raise RuntimeError(
            "No historical files matched the source-file definition."
        )

    return dict(sorted(touches.items()))


def write_source_file_csv(file_touches):
    """
    Write historical paths and touch totals to a structured CSV.

    The CSV provides Task 1's selected source-file list and gives later scripts
    a result against which their independently generated totals can be checked.
    """
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Filename", "Touches"])

        for file_path, touch_count in file_touches.items():
            writer.writerow([file_path, touch_count])


def main():
    """Collect historical source paths and their touch totals."""
    default_branch = get_default_branch(REPOSITORY)
    print(f"Default branch: {default_branch}")

    file_touches = collect_historical_file_touches(
        REPOSITORY,
        default_branch,
    )

    print(f"Selected {len(file_touches)} historical source paths:")
    for file_path, touch_count in file_touches.items():
        print(f"  {file_path}: {touch_count}")

    write_source_file_csv(file_touches)

    most_touched_file = max(
        file_touches,
        key=file_touches.get,
    )
    total_touches = sum(file_touches.values())

    print(f"Output written to: {OUTPUT_FILE}")
    print(
        f"Most frequently touched source path: {most_touched_file} "
        f"({file_touches[most_touched_file]} touches)"
    )
    print(f"Total source-path touches: {total_touches}")


# Prevent API collection from running merely because a tool inspects the file.
if __name__ == "__main__":
    main()