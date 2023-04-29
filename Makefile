clean:
	rm -rf env

install:
	python -m venv env 
	env/bin/pip install --upgrade pip
	env/bin/pip install -r requirements.txt

reset_docker:
	docker compose down --remove-orphans
	docker compose build --no-cache
	docker compose up -d