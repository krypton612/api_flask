from flask import Blueprint, Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

crud = Flask(__name__)

crud.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://krypton612:12345@localhost:3306/api_notes"
crud.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(crud)
ma = Marshmallow(crud)


class note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    country = db.Column(db.String(150))
    note = db.Column(db.String(255))
    number_mobile = db.Column(db.String(20))

    def __init__(self, name, lastname, country, note, number_mobile):
        self.name = (name,)
        self.lastname = (lastname,)
        self.country = (country,)
        self.note = (note,)
        self.number_mobile = number_mobile


db.create_all()


class notesSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "lastname", "country", "note", "number_mobile")


route_create_note = Blueprint("route_create_note", __name__)

note_schema = notesSchema()
notes_schema = notesSchema(many=True)


@route_create_note.route("/register_note", methods=["POST"])
def note_create():

    name = request.json["name"]
    lastname = request.json["lastname"]
    country = request.json["country"]
    note = request.json["note"]
    number_mobile = request.json["number_mobile"]

    new_note = note(name, lastname, country, note, number_mobile)
    db.session.add(new_note)
    db.session.commit()

    return note_schema.jsonify(new_note)
