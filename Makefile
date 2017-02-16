PROJECT := powerdns-rest-api
GIT_HUB := https://github.com/adfinis-sygroup/powerdns-rest-api

include pyproject/Makefile

test_ext:
	python3 manage.py test sydns.api
