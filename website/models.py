from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#Creates a class named Note that is like a database
class Note(db.Model):
    #Declares the fields in the database 
    
    #primary_key means that every entry is uniquely identified for
    #each user
    id = db.Column(db.Integer, primary_key=True)
    #This means that the data has a max 10000 characters long
    data = db.Column(db.String(10000))
    #This sets the date to the current time 
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #Foreign key creates a link between two tables
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    #sets primary key to make each one unique
    id = db.Column(db.Integer, primary_key=True)
    #Sets email to be unique
    # ( if someone enters the same email when signing up, that 
    # gives them an error)
    email = db.Column(db.String(150), unique=True)
    #password is set to be a max 150 characters long
    password = db.Column(db.String(150))
    #first name is set to be max 150 characters long
    first_name = db.Column(db.String(150))
    #notes is set to have a relationship with the Notes table
    notes = db.relationship('Note')