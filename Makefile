.PHONY: install install_dev test
PROJECT := powerdns

install: .requirements.txt  ## Standard pip install including .requirements.txt (for testing)
	pip install --upgrade pip
	pip install --upgrade -r .requirements.txt

install_dev: .dev-requirements.txt install  # Standard pip install inlcuding .dev-requirements (for development)
	pip install --upgrade pip
	pip install -r .dev-requirements.txt -r .requirements.txt

test:
	@flake8
	@pytest --cov --create-db
