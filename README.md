Flask Starter Project
=============

This is a really simple project with some basic static files
and a single Flask endpoint that could be used to start hacking.

The `.gitignore` includes a statement to ignore files in `venv` which
is a folder right next to my code where I keep my Python environment.
To get this app running set up your environment with:
`virtualenv venv`

Then install the requirements:
`pip install -r requirements.txt`

Finall, run the app:
`python run.py`

To get the index page to load you need Node.js and Bower then you can run.
`cd app/static && npm install` then you can run `npm test` to run the tests.
Note that you'll have to visit the Karma URL and connect a browser (usually
Karma starts a server on localhost:9876).
See [angular-seed][https://github.com/angular/angular-seed]
for more details on how to test the frontend code, but note that webdriver tests
were not brought into this project.

There's also some simple Flask stuff included.
A login should be available at http://localhost:8080/auth/signin/
An admin page should be available at http://localhost:8080/admin/
