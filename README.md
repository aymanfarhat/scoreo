Run the server

`export FLASK_DEBUG=1`
then
`flask run`

Before running the flask app needs to be referenced in an environment variable: `export FLASK_APP=scoreo/__init__.py`

Update the database:

After updating the models file for the database scheme run: `flask db migrate` to generate a new migration.
After generating the new migration, run `flask db upgrade` to apply the migration.

If a migrations folder does not exist this means the database is not yet initialised. run `flask db init` then migrate it upgrade.
