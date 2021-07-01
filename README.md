# govuk-flask-prototyping

## Getting started

Optional but recommended. Run in a virtualenv. To create one (with Python 3) run:

```
mkvirtualenv --python=`which python3` <name>
```
where <name> is what you wish to call it.

When returning run `workon <name>` to activate the virtualenv you just created.

To install flask and all the other dependencies run:

```
pip install -r requirements.txt
```

Install npm requirements

```
npm install
```

Finally to start the it run:

```
flask run
```

## Security

If you publish your prototypes online, they **must** be protected by a username and password. This is to prevent members of the public finding prototypes and thinking they are real services.

How to protect your prototype is different depending on where you decide to host it:

* [Add a username and password on Heroku](https://govuk-prototype-kit.herokuapp.com/docs/publishing-on-heroku).
* [Add authentication with a Route Service - PaaS](https://docs.cloud.service.gov.uk/#example-route-service-to-add-authentication)

You must protect user privacy at all times, even when using prototypes. Prototypes made with the kit look like GOV.UK, but do not have the same security provisions. Always make sure you are handling user data appropriately.