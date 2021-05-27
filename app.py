from flask import Flask, url_for, request, redirect, render_template, flash
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension

from forms import PetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "fhgfjgfjhgf"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def root():
    pets = Pet.query.all()

    return render_template("list_pets.html", pets = pets)

@app.route("/add", methods = ["GET", "POST"])
def add_pet():
    form = PetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect(url_for('root'))

    else:
        return render_template("add_pet_form.html", form=form)


@app.route("/<int:pet_id>", methods = ["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj = pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated")

        return redirect(url_for('root'))

    else:
        return render_template("edit_pet_form.html", form=form, pet=pet)

@app.route("/api/pets/<int:pet_id>", methods = ["GET"])
def api_get_pet(pet_id):

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)
