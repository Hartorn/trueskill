default: help;

help: ## Display commands help
	@grep -E '^[a-zA-Z][a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

format: ## Format all files inside backend with black & isort
	poetry run black .
	poetry run isort .
.PHONY: format

check_format: ## Format all files inside backend with black & isort
	poetry run black . --check
	poetry run isort . -c
.PHONY: check_format

check_linting: ## Format all files inside backend with black & isort
	poetry run pylint ./src ./tests
.PHONY: check_linting

setup: ## Install the deps
	poetry install --sync
.PHONY: setup

clean: ## Remove all caches
	rm -rf __pycache__ **/__pycache__ .pytest_cache
.PHONY: clean

test: clean ## Run the tests
	poetry run pytest -p no:cacheprovider -v
.PHONY: test