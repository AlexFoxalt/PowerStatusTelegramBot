docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_start:
	docker-compose start

docker_down:
	docker-compose down

docker_destroy:
	docker-compose down -v

docker_stop:
	docker-compose stop

docker_restart:
	docker-compose stop
	docker-compose up -d

docker_logs:
	docker-compose logs --tail=100 -f

docker_logs_app:
	docker-compose logs --tail=100 -f tg_app

docker_prune:
	docker image prune

ve:
	test ! -d .ve && python3 -m venv .ve; \
	. .ve/bin/activate; \
	pip install -r requirements.txt;

clean:
	test -d .ve && rm -rf .ve

run:
	python3 main.py
