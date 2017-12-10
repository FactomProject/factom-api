SHELL=/bin/bash

# Docker-compose
build: ## Build all docker images.
	docker-compose build
flake8: ## Run flake8.
	docker-compose run factom-api flake8 .
shell: ## Open a bash shell inside docker conatiner.
	docker-compose run factom-api bash
sandbox: ## Run the factom sandbox server.
	docker-compose up factom-sandbox
test: ## Run test suite.
	docker-compose run factom-api pytest
tox: ## Run tox.
	docker-compose run factom-api tox
clean: ## Clean the application.
	find . -name '*.py[co]' -delete
	find . -type d -name "__pycache__" -delete
help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
