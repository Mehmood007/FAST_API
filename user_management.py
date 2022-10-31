import flask_pymongo
import json
from bson import json_util
import uuid

#Connection with Database
try:
    client = flask_pymongo.MongoClient("mongodb://my_team:X3Njg1cRrj9QT5Ks@ac-ga3haug-shard-00-00.59spobs.mongodb.net:27017,ac-ga3haug-shard-00-01.59spobs.mongodb.net:27017,ac-ga3haug-shard-00-02.59spobs.mongodb.net:27017/?ssl=true&replicaSet=atlas-ugvkvk-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.fast

    

    
    client.server_info()
except:
    print("Error cannot connect to db")



#Below funcitons are related to pessenger
def pessanger_signup(franchise_details):
    similar_emails = parse_json(db.pessengers.find({"email":franchise_details["email"]}))
    if similar_emails:
        return False
    franchise_details["history"] = []
    db.pessengers.insert_one(franchise_details)
    return True


def pessanger_login(login_credentials):
    pessenger = db.pessengers.find({"email":login_credentials['email'],'password':login_credentials['password']})
    try:
        pessenger = parse_json(pessenger[0])
        session = dict(pessenger['_id'])['$oid']+str(uuid.uuid4())
        db.sessions.insert_one({'session_id':session,'user_previliges':'pessenger',"email": pessenger["email"]})
        pessenger['session_id'] = session
        return pessenger
    except IndexError:
        return False



def verify_pessenger_session(session_id):
    sessions = db.sessions.find({'session_id':session_id})
    try:
        session = parse_json(sessions[0])
        if session['user_previliges'] == 'pessenger':
            user = parse_json(db.pessengers.find({'email':session['email']})[0])
            return user
        return False

    except IndexError:
        return False



#Below are drivers routes
def driver_signup(franchise_details):
    similar_emails = parse_json(db.drivers.find({"email":franchise_details["email"]}))
    if similar_emails:
        return False
    franchise_details["history"] = []
    db.drivers.insert_one(franchise_details)
    return True


def driver_login(login_credentials):
    pessenger = db.drivers.find({"email":login_credentials['email'],'password':login_credentials['password']})
    try:
        pessenger = parse_json(pessenger[0])
        session = dict(pessenger['_id'])['$oid']+str(uuid.uuid4())
        db.sessions.insert_one({'session_id':session,'user_previliges':'driver',"email": pessenger["email"]})
        pessenger['session_id'] = session
        return pessenger
    except IndexError:
        return False



def verify_driver_session(session_id):
    sessions = db.sessions.find({'session_id':session_id})
    try:
        session = parse_json(sessions[0])
        if session['user_previliges'] == 'driver':
            user = parse_json(db.drivers.find({'email':session['email']})[0])
            return user
        return False

    except IndexError:
        return False




#Below are routes functions
#Driver's related routes
def add_route(route_details,drivers_mail):
    driver_history = parse_json(db.drivers.find({"email":drivers_mail})[0]['history'])
    driver_history.append(route_details)
    db.drivers.find_one_and_update({'email': drivers_mail},{'$set':{'history': driver_history}})
    route_details["route_driver"] = drivers_mail
    route_details["bookings"] = []
    route_details["seats"] = [False for i in range(15)]
    db.routes.insert_one(route_details)
    return True


def delete_route(route_details):
    db.routes.delete_many(route_details)
    return True

#Pessenger's related routes
def get_all_routes():
    routes = db.routes.find({})
    return parse_json(routes)


def select_route(pessenger_mail,route,seats):
    route_details = parse_json(db.routes.find({route})[0])
    print(route_details)
    for i in seats:
        route_details["seats"][i]=True

    route_details["bookings"].append(pessenger_mail)
    print("\n\n\nWorking here\n\n\n")
    db.routes.find_one_and_update({"_id":dict(route['_id'])['$oid']},{'$set':route_details})

    return True

    
    


def parse_json(data):
    return json.loads(json_util.dumps(data))