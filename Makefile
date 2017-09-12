.PHONY: install install_dev test help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Standard pip install including requirements.txt (for deployment)
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

install_dev:  ## Standard pip install inlcuding dev-requirements (for development)
	pip install --upgrade pip
	pip install -r dev-requirements.txt -r requirements.txt

test:
	@flake8
	@pytest --cov --create-db
