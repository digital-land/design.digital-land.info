init:
	pip install -r requirements.txt
	npm install

run:
	flask run

frontend-assets: javascripts stylesheets

javascripts:
	npm run copyjs
	npm run nps copy.javascripts
	npm run nps build.javascripts

stylesheets:
	npm run nps build.stylesheets

black:
	black .

black-check:
	black --check .

flake8:
	flake8 --exclude .venv,node_modules

watch:
	npm run watch
