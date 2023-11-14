.PHONY: buildup
buildup:
	docker compose -f docker-compose.yaml up -d --build

.PHONY: up
up:
	docker compose -f docker-compose.yaml up $(OPTIONS)

.PHONY: build
build:
	docker compose -f docker-compose.yaml build

.PHONY: down
down:
	docker compose -f docker-compose.yaml down

.PHONY: kill
kill:
	docker compose -f docker-compose.yaml down -v

.PHONY: createsuperuser
createsuperuser:
	docker compose -f docker-compose.yaml run api python manage.py createsuperuser

.PHONY: shell
shell:
	docker compose -f docker-compose.yaml run api python manage.py shell

.PHONY: test
test:
	docker compose -f docker-compose.yaml run -e DJANGO_ENV="TESTING" api python manage.py test $(APP)

.PHONY: coverage-run
coverage-run:
	docker compose -f docker-compose.yaml run -e DJANGO_ENV="TESTING" api coverage run manage.py test $(APP)

.PHONY: coverage-report
coverage-report:
	docker compose -f docker-compose.yaml run api coverage report

.PHONY: coverage-html
coverage-html:
	docker compose -f docker-compose.yaml run api coverage html
