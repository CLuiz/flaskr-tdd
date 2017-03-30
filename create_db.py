# create db

from app import db
from models import Flaskr


# create db and d table
db.create_all()

# commit the changes
db.session.commit()
