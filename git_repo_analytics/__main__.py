import csv

from .git import clone_or_pull_repo, get_commits
import os.path
import duckdb


def load_commits(con, commits):
    print("Loading commits...")

    def commit(c):
        return (c["repo_url"], c["hash"], c["author"], c["email"], c["message"], c["date"], c["raw_date"])

    con.executemany("INSERT INTO logs VALUES(?, ?, ?, ?, ?, ?, ?)", map(commit, commits))


def read_repo(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield tuple(row.values())


def clone_or_pull_repos(conn):
    # read csv file from seeds/repos.csv
    for name, repo in read_repo('seeds/repos.csv'):
        # get the latest component of repo
        # e.g. https://github.com/nomic-ai/gpt4all -> gp4all
        subfolder = repo.split('/')[-1]
        repo_url = f'{repo}.git'

        repo = clone_or_pull_repo(repo_url, f'scrape/repos/{subfolder}')
        commits = get_commits(repo_url, repo)
        load_commits(conn, commits)


if __name__ == '__main__':
    path = os.getcwd()
    if not path.endswith("/"):
        path = path + "/"
    fname = f'{path}git_repo.duckdb'
    if os.path.isfile(fname):
        os.remove(fname)

    with duckdb.connect(database=fname) as conn:
        conn.execute(
            "CREATE TABLE logs (repo_url VARCHAR(256), hash VARCHAR(40), author VARCHAR(256), email VARCHAR(256), " +
            "message text, date VARCHAR(35), raw_date VARCHAR(35))")

        clone_or_pull_repos(conn)
