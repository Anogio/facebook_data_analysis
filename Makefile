#!make

.PHONY: install
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

.PHONY: test
test:
	python -m pytest tests
