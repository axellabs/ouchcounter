# Ouchcounter

This is a small webapp for logging and tracking pain levels in people with chronic pain (or who just want to track their pain). I'm making this as a learning exercise in API design in python.

It's served by a database running on a docker container on my machine. To run this app:

1. Clone the repo
2. Activate the virtual python environment by running `source ouchcounterpy/bin/activate` and run `pip install` to get all of the dependencies
3. `docker pull postgres` to get the PostgreSQL image on your computer
4. `docker run --rm --name postgres -e POSTGRES_PASSWORD=makepasswordhere -d -p 5432:5432 -v $HOME/path/to/persistent/volume:/var/lib/postgresql/data postgres`
5. Edit the SQLALCHEMY_DATABASE_URI to include your database password and docker IP address.
6. Run the app and initialize the database by running the following commands in the `ouchcounterpy` virtual environment:
   1. `from app import db`
   2. `db.create_all()`