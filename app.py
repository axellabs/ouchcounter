"""The REST API backend for the ouchcounter, a chronic pain logger
"""
import os
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

# Load secrets and env variables
load_dotenv()
USERNAME = os.getenv("DATABASE_USERNAME")
PASSWORD = os.getenv("DATABASE_PASSWORD")
URI = os.getenv("DATABASE_URI")
NAME = os.getenv("DATABASE_NAME")

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USERNAME}:{PASSWORD}@{URI}/{NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Create a Pain Object
class PainEntry(db.Model):
    """The database model for a single pain entry

    Args:
        db (Model): takes in a database model
    """
    id = db.Column(db.Integer, primary_key=True)
    pain_level = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def __init__(self, pain_level, date):
        self.pain_level = pain_level
        self.date = date

# Create a schema with marshmallow
class PainEntrySchema(ma.Schema):
    """[summary]

    Args:
        ma (Marshmellow): a schema wrapper (???)
        learn more about marshmellow and how that works
    """
    class Meta:
        """holds the fields for the schema
        """
        fields = ('pain_level', 'date')

# Init schema
pain_entry_schema = PainEntrySchema()
pain_entries_schema = PainEntrySchema(many=True)

#--------
## Routes
#---------

# Home route
@app.route('/', methods=['GET'])
def homepage():
    """route for the home url, confirms site is working

    Returns:
        [str]: a greeting message
    """
    return "Hello world"

# Add a pain entry
@app.route('/new-ouchie', methods=['PUT'])
def add_pain_entry():
    """adds a pain entry via JSON to the log

    Returns:
        pain_entry (json) : returns a json object formatted by the pain entry data schema
    """
    pain_level = request.json['pain_level']
    date = datetime.datetime.now()

    new_pain_entry = PainEntry(pain_level, date)

    db.session.add(new_pain_entry)
    db.session.commit()

    return pain_entry_schema.jsonify(new_pain_entry)

# Add a pain entry: but more automated
@app.route('/new-ouchie/<painLevel>', methods=['PUT'])
def add_pain_entry_url(pain_level):
    """adds a pain entry to the log via URL arguments

    Args:
        pain_level (int): level of pain as an int between 1 and 10

    Returns:
        pain_entry (json) : returns a json object formatted by the pain entry data schema
    """
    date = datetime.datetime.now()

    new_pain_entry = PainEntry(pain_level, date)

    db.session.add(new_pain_entry)
    db.session.commit()

    return pain_entry_schema.jsonify(new_pain_entry)

# Return all pain logs
@app.route('/all-ouchies', methods=['GET'])
def show_pain_entries():
    """returns all of the pain entries from the database

    Returns:
        (json) : an array of all pain entry objects
    """
    all_pain_entries = PainEntry.query.all()
    result = pain_entries_schema.dump(all_pain_entries)
    return jsonify(result)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
    