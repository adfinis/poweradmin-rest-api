.PHONY: install lint test db_shell


help: 
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip3 install -r requirements.txt

lint: ## Lint source code
	flake8

db_shell: ## Open up a mysql shell
	docker exec -it powerdnsrestapisrc_db_1 mysql -usydns -psydns powerdns

test: ## Runs all tests
	python3 sydns/manage.py test
