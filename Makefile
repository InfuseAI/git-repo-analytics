all: fetch load transform report piperider

fetch_gh:
	@python -m git_repo_analytics.fetch_github_api

clone_repos:
	@python -m git_repo_analytics.clone_repos

fetch: fetch_gh clone_repos

load:
	@python -m git_repo_analytics.load

transform:
	dbt build

report:
	@python -m git_repo_analytics.gen_report	

piperider:
	rm -rf data/piperider
	piperider run -o data/piperider --open



