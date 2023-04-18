from datetime import datetime, timezone
import re

import git


def clone_or_pull_repo(repo_url, local_path):
    '''Clone or pull a git repo to a local path'''

    try:
        repo = git.Repo(local_path)
        print(f'Pulling {repo_url} to {local_path}')
        repo.git.pull()
    except git.exc.NoSuchPathError:
        print(f'Cloning {repo_url} to {local_path}')
        repo = git.Repo.clone_from(repo_url, local_path)
    return repo


def get_commits(repo_url, repo):
    log = repo.git.log(date='iso8601-strict').split("\ncommit ")
    # remove 'commit ' in first line
    log[0] = log[0][7:]
    commits = []
    for line in log:
        match = re.search(r"([^\n]+)\n(Merge:\s+([^\n]+)\n)?Author:\s+([^\n]+)\nDate:\s+([^\n]+)\n\n\s+(.*)\n", line,
                          re.DOTALL)
        if match:
            author = re.match(r"(.+)\s+<([^>]+)>", match.group(4))
            date = datetime.fromisoformat(match.group(5))
            commit = {
                "repo_url": repo_url,
                "hash": match.group(1),
                "date": date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                "raw_date": match.group(5),
                "message": match.group(6)
            }
            if author:
                commit["author"] = author.group(1)
                commit["email"] = author.group(2)
            else:
                commit["author"] = match.group(4)
                commit["email"] = None
            commits.append(commit)
    return commits
