PROJECT := powerdns

include pyproject/Makefile

FAIL_UNDER := 95
install_dev: .dev-requirements.txt install
	pip install -r .dev-requirements.txt
