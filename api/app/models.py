from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.BINARY(16), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)

class Cleanwalk(db.Model):
    __tablename__ = 'cleanwalks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    pos_lat = db.Column(db.Float, nullable=False)
    pos_long = db.Column(db.Float, nullable=False)
    date_begin = db.Column(db.TIMESTAMP, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    address = db.Column(db.String(255), nullable=False)

class CleanwalkUser(db.Model):
    __tablename__ = 'user_cleanwalk'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    cleanwalk_id = db.Column(db.String(255), db.ForeignKey('cleanwalks.id'), primary_key=True)
    nb_person = db.Column(db.Integer, nullable=False)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable = False)
    author_id = db.Column(db.String(255), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
