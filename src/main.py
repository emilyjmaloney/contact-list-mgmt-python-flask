"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Contact
#from models import Contact

#configs for app
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#makes sure db is up-to-date
MIGRATE = Migrate(app, db)
db.init_app(app)

#config for API to receive incoming requests from diff domains
CORS(app)

#allows creation of 
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/contact/<int:contact_id>,', methods=['GET'])
def get_contact():
    bubu = Contact.query.filter_by().all()
    print(bubu)
    response_body = {
        "msg" :"This is a GET response"
    }
    return jsonify(response_body), 200

### Adding an endpoint (from _QUICK_START.md)
# For each endpoint you will need to have:
# 1. One `@APP` decorator that specifies the path for the expoint.
#     - You can have parameters in the url like this `<int:person_id>`
#     - You can specify what methods can be called on that endpoint like this `methods=['PUT', 'GET']`
# 2. The method that will execute when that endpoint is called (in this case `get_sinde_person`), the name of the method does not matter.
# 3. Inside the method you can speficy what logic to execute of each type of request using `if request.method == 'PUT'`
# 4. You have to return always a json and a status code (200,400,404, etc.)

        #MY ENDPOINTS
# tasks below from "Fake Contact-List API": 

# 7) Create one contact - complete
@app.route('/add', methods=['POST'])
def handle_add():
    new_contact_data = request.get_json()
    new_contact = Contact(
        full_name = new_contact_data["full_name"],
        phone = new_contact_data["phone"],
        email = new_contact_data["email"],
        address = new_contact_data["address"]
    )
    db.session.add(new_contact)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }    
    return jsonify(new_contact.serialize()), 201

# 4) Get one particular contact - complete
@app.route('/getone/<int:id>', methods=['GET'])
def handle_getone(id):
    single_contact = Contact.query.get(id)
    return jsonify(single_contact.serialize()), 200

# 5) Delete one particular contact
@app.route('/deleteone', methods=['DELETE'])
def handle_deleteone():
    delete_one = request.delete_json()
    response_body = {
        "msg": "Hello, this is your DELETE /user response "
    }
    return jsonify(delete_one), 200

# 3) Get all contacts - complete
@app.route('/getall', methods=['GET'])
def handle_getall():
    all_contacts = Contact.query.all()
    serialized_contacts = []
    for contact in all_contacts:
        serialized_contacts.append(contact.serialize())
    return jsonify(serialized_contacts), 200

# 6) Delete all contacts
# @app.route('/deleteall', methods=['DELETE'])
# def handle_deleteall():
#     delete_all = request.delete_json()
#     response_body = {
#         "msg": "Hello, this is your DELETE /user response "
#     }
#     return jsonify(add_new), 200


@app.route('/deleteall', methods=['DELETE'])
def handle_deleteall():
    add_new = request.delete_json()
    response_body = {
        "msg": "Hello, this is your DELETE /user response "
    }
    return jsonify(add_new), 200




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
