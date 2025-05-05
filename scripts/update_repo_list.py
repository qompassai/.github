# ~/.GH/Qompass/.github/scripts/update_repo_list.py
# -------------------------------------------------
# Copyright (C) 2025 Qompass AI, All rights reserved

#!/usr/bin/env python3
import requests
import os

GITHUB_ORG = "qompassai"
README_PATH = "README.md"
START_MARKER = "<!-- REPO-LIST-START -->"
END_MARKER = "<!-- REPO-LIST-END -->"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_repos():
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/repos?per_page=100"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    repos = []

    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        repos += r.json()
        url = r.links.get("next", {}).get("url")

    return sorted(repo["name"] for repo in repos if not repo["private"])

def update_readme(repos):
    with open(README_PATH, "r") as f:
        content = f.read()

    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if start == -1 or end == -1:
        raise ValueError("Markers not found in README.md")

    before = content[:start + len(START_MARKER)]
    after = content[end:]

    repo_lines = "\n".join(f"- [{repo}](https://github.com/{GITHUB_ORG}/{repo})" for repo in repos)
    new_content = f"{before}\n{repo_lines}\n{after}"

    with open(README_PATH, "w") as f:
        f.write(new_content)

if __name__ == "__main__":
    repos = fetch_repos()
    update_readme(repos)

