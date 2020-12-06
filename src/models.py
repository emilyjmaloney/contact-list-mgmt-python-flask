from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Below is how we declare a class, we can use this as an example,
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
        #Our goal is to create our own class and make it work with the contact list with react, day 18.
        # create a model that we can create as we want, and then create the columns that will store all our information.
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(400), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=False, nullable=False)
    # tell python how to print the class object on the console
    def __repr__(self):
        return '<Contact %r>' % self.full_name
        # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id":self.id,
            "salute":f"hello {self.full_name}",
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone
        }

