all: fetch load transform piperider

fetch_gh:
	@python -m git_repo_analytics.fetch_github_api

clone_repos:
	@python -m git_repo_analytics.clone_repos

fetch: fetch_gh clone_repos

load:
	@python -m git_repo_analytics.load

transform:
	dbt build

piperider:
	piperider run


