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

A login should be available at http://localhost:8080/auth/signin/

An admin page should be available at http://localhost:8080/admin/
