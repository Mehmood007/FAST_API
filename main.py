from flask import Flask,jsonify
from flask import request
import user_management
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


#Pessenger registration and verifications routes are below
@app.route("/pessenger_signup", methods = ['POST'])
def pessenger_signUp():
    franchise_details = request.get_json()
    signup = user_management.pessanger_signup(franchise_details)
    if signup:
        return jsonify({"message":"User Signed UP successfully"})
    return jsonify({"message":"Given email is already registered"})



@app.route("/pessengerLogin", methods = ['POST'])
def pessenger_login():

    login_credentials = request.get_json()

    login = user_management.pessanger_login(login_credentials)
    if login:
        return jsonify(login)
    return jsonify({"message":"Error in signing in to pessenger"})



@app.route("/verify_pessenger/<string:session_id>")
def verify_pessenger(session_id):
    pessenger_details = user_management.verify_pessenger_session(session_id)
    if pessenger_details:
        return jsonify(pessenger_details)
    
    return jsonify({"message":"User not authorized for this request"})



#Driver registration and verification routes are below

@app.route("/driver_signup", methods = ['POST'])
def driver_signUp():
    franchise_details = request.get_json()
    signup = user_management.driver_signup(franchise_details)
    if signup:
        return jsonify({"message":"User Signed UP successfully"})
    return jsonify({"message":"Given email already in registered"})


@app.route("/driverLogin", methods = ['POST'])
def driver_login():

    login_credentials = request.get_json()

    login = user_management.driver_login(login_credentials)
    if login:
        return jsonify(login)
    return jsonify({"message":"Error in signing in to pessenger"})



@app.route("/verify_driver/<string:session_id>")
def verify_driver(session_id):
    pessenger_details = user_management.verify_driver_session(session_id)
    if pessenger_details:
        return jsonify(pessenger_details)
    
    return jsonify({"message":"User not authorized for this request"})



#Routes related routes
#Driver routes are given below
@app.route("/add_route", methods = ['POST'])
def add_route():
    session_id = request.headers['session_id']
    driver = user_management.verify_driver_session(session_id)
    if driver:
        data = request.get_json()
        user_management.add_route(data,driver["email"])
        return jsonify({"message":"Route added successfully"})
    
    return jsonify({"message":"User is not authorized to add this route"})
    



@app.route("/delete_route", methods = ['POST'])
def delete_route():
    session_id = request.headers['session_id']
    driver = user_management.verify_driver_session(session_id)
    if driver:
        data = request.get_json()
        data["route_driver"] = driver["email"]
        user_management.delete_route(data)
        return {"message":"Route deleted successfully"}

    return jsonify({"message":"User is not authorized to delete route"})


#Pessenger related routes
@app.route("/all_routes")
def all_route():
    routes = user_management.get_all_routes()
    return jsonify(routes)


@app.route("/select_route",methods=["POST"])
def select_routes():
    session_id = request.headers['session_id']
    pessenger = user_management.verify_pessenger_session(session_id)
    if pessenger:
        route = request.get_json()["route"]
        seats = request.get_json()["seats"]
        user_management.select_route(pessenger["email"],route,seats)
        return jsonify({"message":"Route selected successfully"})

    return jsonify({"message":"User is not authorized"})




if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)