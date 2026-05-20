.PHONY: test lint type cov complexity all

test:
	pytest -v

cov:
	pytest --cov=. --cov-report=term-missing --cov-report=html

lint:
	ruff check legacy.py tests/

type:
	mypy --strict legacy.py

complexity:
	radon cc legacy.py -s -a

all: lint type test cov complexity