init:
	pip install -r requirements.txt
	npm install

run:
	flask run

javascripts:
	npm run copyjs
