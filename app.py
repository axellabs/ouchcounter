from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from dotenv import load_dotenv
import datetime
import os

# Load secrets and env variables
load_dotenv()
USERNAME =  os.getenv("DATABASE_USERNAME")
PASSWORD =  os.getenv("DATABASE_PASSWORD")
URI =  os.getenv("DATABASE_URI")
NAME =  os.getenv("DATABASE_NAME")

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
  id = db.Column(db.Integer, primary_key=True)
  painLevel = db.Column(db.Integer)
  date = db.Column(db.DateTime)

  def __init__(self, painLevel, date):
    self.painLevel = painLevel
    self.date = date

# Create a schema with marshmallow
class PainEntrySchema(ma.Schema):
  class Meta:
    fields = ('painLevel', 'date')

# Init schema
pain_entry_schema = PainEntrySchema()
pain_entries_schema = PainEntrySchema(many=True)

##--------
## Routes
##---------

# Home route
@app.route('/', methods=['GET'])
def homepage():
  return "Hello world"

# Add a pain entry
@app.route('/new-ouchie', methods=['PUT'])
def add_pain_entry():
  painLevel = request.json['painLevel']
  date = datetime.datetime.now()

  new_pain_entry = PainEntry(painLevel, date)

  db.session.add(new_pain_entry)
  db.session.commit()

  return pain_entry_schema.jsonify(new_pain_entry)

# Add a pain entry: but more automated
@app.route('/new-ouchie/<painLevel>', methods=['PUT'])
def add_pain_entry_url(painLevel):
  painLevel = painLevel
  date = datetime.datetime.now()

  new_pain_entry = PainEntry(painLevel, date)

  db.session.add(new_pain_entry)
  db.session.commit()

  return pain_entry_schema.jsonify(new_pain_entry)

# Run server 
if __name__ == '__main__':
  app.run(debug=True)