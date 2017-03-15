PROJECT := sydns
GIT_HUB := https://github.com/adfinis-sygroup/powerdns-rest-api

include pyproject/Makefile

install_dev: .dev-requirements.txt install
	pip install -r .dev-requirements.txt
