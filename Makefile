PROJECT := powerdns

include pyproject/Makefile

FAIL_UNDER := 100
install_dev: .dev-requirements.txt install
	pip install -r .dev-requirements.txt
