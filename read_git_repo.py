from datetime import datetime, timezone
import git
import re
import os.path
import duckdb


def log(repo):
    repo = git.Repo(repo)
    log = repo.git.log(date='iso8601-strict').split("\ncommit ")
    # remove 'commit ' in first line
    log[0] = log[0][7:]
    commits = []
    for line in log:
        match = re.search(r"([^\n]+)\n(Merge:\s+([^\n]+)\n)?Author:\s+([^\n]+)\nDate:\s+([^\n]+)\n\n\s+(.*)\n", line, re.DOTALL)
        if match:
            author = re.match(r"(.+)\s+<([^>]+)>", match.group(4))
            date = datetime.fromisoformat(match.group(5))
            commit = {
                "hash": match.group(1),
                "date": date.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
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


if __name__ == '__main__':
    path = os.getcwd()
    commits = log(f'{path}/git_repo')
    if not path.endswith("/"):
        path = path + "/"
    fname = f'{path}git_repo.duckdb'
    if os.path.isfile(fname):
        os.remove(fname)

    con = duckdb.connect(database=fname)
    con.execute("CREATE TABLE commits (hash VARCHAR(40), author VARCHAR(256), email VARCHAR(256), " +
                "message text, date VARCHAR(35))")

    def commit(c):
        return (c["hash"], c["author"], c["email"], c["message"], c["date"])
    con.executemany("INSERT INTO commits VALUES(?, ?, ?, ?, ?)", map(commit, commits))
    con.close()
