import csv
import re
from datetime import datetime, timezone

import git

from git_repo_analytics.common import read_repo
import os.path
import duckdb


def load_repos(conn):
    print("Loading repo commits...")

    # Create commits tabls
    conn.execute(
        '''
        CREATE TABLE raw_commits (
            repo VARCHAR, 
            hash VARCHAR, 
            author VARCHAR, 
            email VARCHAR, 
            message text, 
            date VARCHAR, 
            raw_date VARCHAR
        )
        '''
    )

    def get_commits(repo_name, repo):
        log = repo.git.log(date='iso8601-strict').split("\ncommit ")
        # remove 'commit ' in first line
        log[0] = log[0][7:]
        commits = []
        for line in log:
            match = re.search(r"([^\n]+)\n(Merge:\s+([^\n]+)\n)?Author:\s+([^\n]+)\nDate:\s+([^\n]+)\n\n\s+(.*)\n",
                              line,
                              re.DOTALL)
            if match:
                author = re.match(r"(.+)\s+<([^>]+)>", match.group(4))
                date = datetime.fromisoformat(match.group(5))
                commit = {
                    "repo": repo_name,
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

    for name, repo_name in read_repo():
        # get the latest component of repo
        # e.g. https://github.com/nomic-ai/gpt4all -> gp4all
        subfolder = repo_name.split('/')[-1]

        repo = git.Repo(f'data/repos/{subfolder}')
        commits = get_commits(repo_name, repo)

        def commit(c):
            return (c["repo"], c["hash"], c["author"], c["email"], c["message"], c["date"], c["raw_date"])

        conn.executemany("INSERT INTO raw_commits VALUES(?, ?, ?, ?, ?, ?, ?)", map(commit, commits))


def load_github(conn):
    print("Loading github data...")

    conn.execute(
        '''
        create table raw_repos as
        select * from 'data/gh/*/repo.csv';
        '''
    )
    conn.execute(
        '''
        create table raw_contributers as
        select * from 'data/gh/*/contributers.csv';
        '''
    )


if __name__ == '__main__':
    fname = 'data/git_repo.duckdb'

    if os.path.isfile(fname):
        os.remove(fname)

    with duckdb.connect(database=fname) as conn:
        load_repos(conn)
        load_github(conn)
