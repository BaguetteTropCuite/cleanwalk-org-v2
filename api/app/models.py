from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.BINARY(16), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class Organization(db.Model):
    __tablename__ = 'organizations'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    description = db.Column(db.String(255), nullable=True)
    web_site = db.Column(db.String(255), nullable=True)
    social_medias = db.Column(db.JSON, nullable=True)
    banner_img = db.Column(db.String(255), nullable=True)
    last_event = db.Column(db.TIMESTAMP, nullable=True)

    # Relation vers User
    user = db.relationship('User', backref=db.backref('organization', uselist=False))

class Cleanwalk(db.Model):
    __tablename__ = 'cleanwalks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    pos_lat = db.Column(db.Float, nullable=False)
    pos_long = db.Column(db.Float, nullable=False)
    date_begin = db.Column(db.TIMESTAMP, nullable=False)
    img_url = db.Column(db.String(255), nullable=True)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable = False)
    address = db.Column(db.String(255), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)

class CleanwalkUser(db.Model):
    __tablename__ = 'user_cleanwalk'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    cleanwalk_id = db.Column(db.String(255), db.ForeignKey('cleanwalks.id'), primary_key=True)
    nb_person = db.Column(db.Integer, nullable=False)
    is_host = db.Column(db.Boolean, nullable=False)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.String(255), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    description = db.Column(db.Text, nullable = False)
    published = db.Column(db.Boolean, nullable=False)
    preview_picture = db.Column(db.String(255), nullable=True)

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=False)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), nullable=False)

class Categorie_article(db.Model):
    __tablename__ = 'categories_article'
    id_category = db.Column(db.Integer,db.ForeignKey('categories.id'), primary_key=True)
    id_article = db.Column(db.Integer,db.ForeignKey('articles.id'), primary_key=True)
