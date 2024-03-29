all: fetch load transform report piperider

clone_repos:
	@python -m git_repo_analytics.clone_repos
	@echo

fetch: clone_repos

load:
	@python -m git_repo_analytics.load
	@echo

transform:
	@dbt deps
	@dbt build
	@echo

report:
	@python -m git_repo_analytics.gen_report	
	@echo

piperider:
	@rm -rf data/piperider
	@piperider run -o data/piperider --open
	@echo

clean:
	@rm -rf data
