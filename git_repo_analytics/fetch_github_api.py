import csv
import os

import github
from github import Github

from .common import read_repo


def fetch_github(gh_repo_name, output):
    '''

    Parameters
    ----------
    gh_repo_name, e.g.InfuseAI/Piperider

    Returns
    -------

    '''
    print(f"Fetching '{gh_repo_name}' to '{output}'")
    g = Github(os.environ.get('GITHUB_TOKEN'))
    repo = g.get_repo(gh_repo_name)

    with open(os.path.join(output, 'repo.csv'), 'w', newline='') as csvfile:
        try:
            latest_release = repo.get_latest_release()
        except github.GithubException:
            latest_release = None

        repo_data = {
            'repo': repo.full_name,
            'description': repo.description,
            'homepage': repo.homepage,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'subscribers': repo.subscribers_count,
            'license': repo.get_license().license.name,
            'latest_release': latest_release.tag_name if latest_release else None,
            'latest_release_published_at': latest_release.published_at if latest_release else None,
        }
        writer = csv.DictWriter(csvfile, fieldnames=repo_data.keys())
        writer.writeheader()
        writer.writerow(repo_data)

    with open(os.path.join(output, 'contributers.csv'), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['repo', 'login', 'type', 'name', 'contributions'])
        writer.writeheader()
        for contributor in repo.get_contributors():
            data = {
                'repo': repo.full_name,
                'login': contributor.login,
                'name': contributor.name,
                'type': contributor.type,
                'contributions': contributor.contributions,
            }
            writer.writerow(data)


def fetch_github_repos():
    print("Fetching github stats...")
    from .fetch_github_api import fetch_github

    for name, repo in read_repo():
        subfolder = repo.split('/')[-1]
        os.makedirs(f'data/gh/{subfolder}', exist_ok=True)
        fetch_github(repo, f'data/gh/{subfolder}')


if __name__ == '__main__':
    fetch_github_repos()
