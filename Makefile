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
	pylint ./src/backend
.PHONY: check_linting

