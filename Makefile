.PHONY: install
install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install -r requirements-dev.txt
	python setup.py develop

.PHONY: lint
lint:
	flake8 chaoscf/ tests/
	isort --check-only --profile black chaoscf/ tests/
	black --check --diff chaoscf/ tests/

.PHONY: format
format:
	isort --profile black chaoscf/ tests/
	black chaoscf/ tests/

.PHONY: tests
tests:
	pytest
