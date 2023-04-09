clean:
	rm -rf env

install:
	python -m venv env 
	env/bin/pip install --upgrade pip
	env/bin/pip install -r requirements.txt