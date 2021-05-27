from models import db, Pet
from app import app

db.drop_all()
db.create_all()

Pet.query.delete()

db.session.add(Pet(
    name = "Leo",
    species = "Lion",
    age = "3",
    available = True
))

db.session.commit()