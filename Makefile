init:
	pip install -r requirements.txt
	npm install

run:
	npm start

frontend-assets: javascripts stylesheets govassets

javascripts:
	npm run copyjs
	npm run nps copy.javascripts
	npm run nps build.javascripts

stylesheets:
	npm run nps build.stylesheets

govassets:
	npm run copygovuk
	
black:
	black .

black-check:
	black --check .

flake8:
	flake8 --exclude .venv,node_modules
