.PHONY: up
up:
	docker-compose up -d --build

.PHONY: down
down:
	docker-compose down

.PHONY: shell
shell:
	docker-compose exec --user `id -u`:`id -g` develop /bin/sh

.PHONY: lint
lint:
	python -m flake8 kamoshika tests
	python -m mypy --ignore-missing-imports kamoshika tests
	python -m pylint kamoshika tests

.PHONY: test
test:
	python -m pytest tests
