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
	flake8 kamoshika tests
	mypy --ignore-missing-imports kamoshika tests
	pylint --errors-only kamoshika tests

.PHONY: test
test:
	pytest tests
