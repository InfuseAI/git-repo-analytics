import git

from .common import read_repo


def clone_or_pull_repo(repo_url, local_path):
    '''Clone or pull a git repo to a local path'''

    try:
        repo = git.Repo(local_path)
        print(f"Pulling '{repo_url}' to '{local_path}'")
        repo.git.pull()
    except git.exc.NoSuchPathError:
        print(f"Cloning '{repo_url}' to '{local_path}'")
        repo = git.Repo.clone_from(repo_url, local_path)
    return repo


if __name__ == '__main__':
    for name, repo in read_repo():
        # get the latest component of repo
        # e.g. https://github.com/nomic-ai/gpt4all -> gp4all
        subfolder = repo.split('/')[-1]
        repo_url = f'https://github.com/{repo}.git'

        repo = clone_or_pull_repo(repo_url, f'data/repos/{subfolder}')
