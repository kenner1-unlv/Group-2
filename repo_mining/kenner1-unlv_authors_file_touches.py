"""
Collect author and file-touch history for Rootbeer source paths.

This script uses the same historical event definition as Task 1:

- Scan every commit on the dynamically discovered default branch.
- Include changed paths ending in .java, .kt, .cpp, .c, or .h.
- Count one touch when one commit changes one source path.
- Preserve files later renamed, moved, or deleted.
- Record the responsible author and change date for every touch.

Using the same commit events for paths, totals, authors, and dates prevents the
inconsistent counts that can occur when file histories are queried separately.
"""

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests


REPOSITORY = "scottyab/rootbeer"
SOURCE_EXTENSIONS = {".java", ".kt", ".cpp", ".c", ".h"}

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = SCRIPT_DIRECTORY / "data"
OUTPUT_FILE = DATA_DIRECTORY / "kenner1-unlv_authors_rootbeer.json"

API_BASE_URL = "https://api.github.com"


def create_headers():
    """Build API headers using a credential supplied only at runtime."""
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
    """Request JSON from GitHub and stop clearly on API failures."""
    response = requests.get(
        url,
        headers=create_headers(),
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_default_branch(repository):
    """Discover the repository default branch instead of assuming its name."""
    repository_data = github_get(
        f"{API_BASE_URL}/repos/{repository}"
    )
    return repository_data["default_branch"]


def is_source_file(file_path):
    """Apply the same source extension definition used by Task 1."""
    return Path(file_path).suffix.lower() in SOURCE_EXTENSIONS


def identify_author(commit_details):
    """
    Prefer a linked GitHub username as the stable contributor identity.

    If GitHub cannot associate a commit with an account, fall back to the
    author name stored in the Git commit.
    """
    github_author = commit_details.get("author")

    if github_author and github_author.get("login"):
        return github_author["login"]

    commit_author = commit_details.get("commit", {}).get("author", {})
    return commit_author.get("name") or "Unknown author"


def collect_historical_file_history(repository, branch):
    """
    Collect every historical source-path touch from default-branch commits.

    The same event supplies the path, author, date, and touch count. This keeps
    Task 2 totals directly reconcilable with Task 1.
    """
    file_changes = {}
    repository_commit_dates = []
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

        for commit_summary in commits:
            commit_details = github_get(
                f"{API_BASE_URL}/repos/{repository}/commits/"
                f"{commit_summary['sha']}"
            )

            author = identify_author(commit_details)
            change_date = commit_details["commit"]["author"]["date"]
            repository_commit_dates.append(change_date)

            for changed_file in commit_details.get("files", []):
                file_path = changed_file["filename"]

                if is_source_file(file_path):
                    file_changes.setdefault(file_path, []).append(
                        {
                            "sha": commit_summary["sha"],
                            "author": author,
                            "date": change_date,
                        }
                    )

        page += 1

    if not file_changes:
        raise RuntimeError(
            "No historical source-file changes were collected."
        )

    if not repository_commit_dates:
        raise RuntimeError(
            "No repository commits were returned."
        )

    return file_changes, min(repository_commit_dates)


def build_output(
    repository,
    branch,
    file_changes,
    repository_start_date,
):
    """
    Build JSON containing detailed change events and author summaries.

    Detailed events support the weekly plot. Per-file and per-author totals
    support management findings and reconciliation with the Task 1 CSV.
    """
    files = []

    for file_path in sorted(file_changes):
        changes = sorted(
            file_changes[file_path],
            key=lambda change: change["date"],
        )

        author_counts = Counter(
            change["author"] for change in changes
        )

        authors = [
            {
                "author": author,
                "touches": touches,
            }
            for author, touches in sorted(
                author_counts.items(),
                key=lambda item: (-item[1], item[0].lower()),
            )
        ]

        files.append(
            {
                "path": file_path,
                "touches": len(changes),
                "authors": authors,
                "changes": changes,
            }
        )

    return {
        "repository": repository,
        "default_branch": branch,
        "repository_start_date": repository_start_date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_extensions": sorted(SOURCE_EXTENSIONS),
        "file_scope": "historical default-branch source paths",
        "touch_definition": (
            "one commit changing one historical source path"
        ),
        "files": files,
    }


def write_json(output_data):
    """Write readable JSON for validation, plotting, and reporting."""
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(
            output_data,
            json_file,
            indent=2,
            ensure_ascii=False,
        )
        json_file.write("\n")


def main():
    """Run the complete historical author/file-touch collection."""
    default_branch = get_default_branch(REPOSITORY)
    print(f"Default branch: {default_branch}")

    file_changes, repository_start_date = (
        collect_historical_file_history(
            REPOSITORY,
            default_branch,
        )
    )

    output_data = build_output(
        REPOSITORY,
        default_branch,
        file_changes,
        repository_start_date,
    )
    write_json(output_data)

    total_touches = sum(
        file_data["touches"]
        for file_data in output_data["files"]
    )

    unique_authors = {
        change["author"]
        for file_data in output_data["files"]
        for change in file_data["changes"]
    }

    print(f"Output written to: {OUTPUT_FILE}")
    print(f"Historical source paths: {len(output_data['files'])}")
    print(f"Total source-path touches: {total_touches}")
    print(f"Unique authors: {len(unique_authors)}")


if __name__ == "__main__":
    main()