init:
	pip install -r requirements.txt
	npm install

run:
	flask run

javascripts:
	npm run copyjs
	npm run nps copy.javascripts
	npm run nps build.javascripts
