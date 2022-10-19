from flask import Flask,jsonify
from flask import request
import user_management
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/pessengerLogin", methods = ['POST'])
def pessenger_login():
    login_credentials = request.get_json()
    login = user_management.pessanger_login(login_credentials)
    if login:
        return jsonify(login)
    return jsonify({"message":"Error in signing in to pessenger"})


@app.route("/pessenger_signup", methods = ['POST'])
def pessenger_signUp():
    franchise_details = request.get_json()
    signup = user_management.pessanger_signup(franchise_details)
    if signup:
        return jsonify({"message":"User Signed UP successfully"})
    return jsonify({"message":"Error in signing up pessenger"})


@app.route("/verify_pessenger/<string:session_id>")
def verify_franchise(session_id):
    pessenger_details = user_management.pessanger_login(session_id)
    if pessenger_details:
        return jsonify(pessenger_details)
    
    return jsonify({"message":"User not authorized for this request"})


if __name__ == "__main__":
    app.run(debug=True)