.PHONY: buildup
buildup:
	docker compose -f docker-compose.yaml up -d --build

.PHONY: up
up:
	docker compose -f docker-compose.yaml up $(OPTIONS)

.PHONY: down
down:
	docker compose -f docker-compose.yaml down

.PHONY: kill
kill:
	docker compose -f docker-compose.yaml down -v

.PHONY: createsuperuser
createsuperuser:
	docker compose -f docker-compose.yaml run api python manage.py createsuperuser

.PHONY: test
test:
	docker compose -f docker-compose.yaml run api python manage.py test $(APP)
