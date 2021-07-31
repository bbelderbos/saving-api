.PHONY: venv
venv:
	python3.9 -m venv venv

.PHONY: install
install:
	pip install -r requirements-dev.txt

.PHONY: lint
lint:
	flake8 db api tests

.PHONY: typing
typing:
	mypy db api tests

.PHONY: test
test:
	pytest

.PHONY: cov
cov:
	pytest --cov=db --cov=api --cov-report term-missing

.PHONY: ci
ci: lint typing test

