up:
	docker compose up --build

down:
	docker compose down

test:
	docker compose run app pytest
test:
	docker exec -it app pytest -v
