from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields

crud = Flask(__name__)

crud.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://krypton612:12345@localhost:3306/api_notes"
crud.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(crud)
ma = Marshmallow(crud)


class notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    country = db.Column(db.String(150))
    note = db.Column(db.String(255))
    number_mobile = db.Column(db.String(20))

    def __init__(self, name, lastname, country, note, number_mobile):
        self.name = name
        self.lastname = lastname
        self.country = country
        self.note = note
        self.number_mobile = number_mobile


db.create_all()


class notesSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "lastname", "country", "note", "number_mobile")


note_schema = notesSchema()
notes_schema = notesSchema(many=True)


@crud.route("/notes", methods=["GET"])
def all_notes():
    all_note = notes.query.all()
    resultados = notes_schema.dump(all_note)
    return jsonify(resultados)


@crud.route("/register_note", methods=["POST"])
def note_create():

    name = request.json["name"]
    lastname = request.json["lastname"]
    country = request.json["country"]
    note = request.json["note"]
    number_mobile = request.json["number_mobile"]

    new_note = notes(name, lastname, country, note, number_mobile)

    db.session.add(new_note)
    db.session.commit()

    return note_schema.jsonify(new_note)


@crud.route("/notes/<id>", methods=["GET"])
def get_note_id(id):
    one_note = notes.query.get(id)
    return note_schema.jsonify(one_note)


@crud.route("/notes/delete/<id>", methods=["DELETE"])
def delete(id):
    one_note_delte = notes.query.get(id)
    db.session.delete(one_note_delte)
    db.session.commit()

    return jsonify({"message": "Eliminado correctamente"})


@crud.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hola bienvenido a la mejor api de pruebas"})


if __name__ == "__main__":
    crud.run(debug=True, port=4000, host="0.0.0.0")
