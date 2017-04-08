Run the server

`export FLASK_DEBUG=1`
then
`flask run`

Before running the flask app needs to be referenced in an environment variable: `export FLASK_APP=scoreo/__init__.py`

Update the database:

After updating the models file for the database scheme run: `flask db migrate` to generate a new migration.
After generating the new migration, run `flask db upgrade` to apply the migration.

If a migrations folder does not exist this means the database is not yet initialised. run `flask db init` then migrate it upgrade.

To run on gunicorn: Run via `gunicorn --bind 0.0.0.0:5000 wsgi:app`

Also make sure to create an upstart script for gunicorn on ubuntu, reference: 
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04
