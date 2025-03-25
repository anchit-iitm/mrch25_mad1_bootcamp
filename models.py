from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore

db = SQLAlchemy()

class user(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True) #
    email = db.Column(db.String(120), unique=True, nullable=False) #
    password = db.Column(db.String(120), nullable=False) #
    name = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, default=True) #
    fs_uniquifier = db.Column(db.String(120), nullable=False) #
    roles = db.relationship('role', secondary='RolesUser', backref=db.backref('users', lazy='dynamic')) #

class role(db.Model, RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True) #
    name = db.Column(db.String(120), nullable=False) #

class RolesUser(db.Model):
    __tablename__ = 'RolesUser'
    id = db.Column(db.Integer, primary_key=True) #
    user_id = db.Column(db.Integer, db.ForeignKey('User.id')) #
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id')) #

user_datastore = SQLAlchemyUserDatastore(db, user, role)

