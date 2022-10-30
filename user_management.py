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



def pessanger_login(login_credentials):
    pessenger = db.pessengers.find({"email":login_credentials['email'],'pass':login_credentials['pass']})
    try:
        pessenger = parse_json(pessenger[0])
        session = dict(pessenger['_id'])['$oid']+str(uuid.uuid4())
        db.sessions.insert_one({'session_id':session,'user_previliges':'pessenger',"email": pessenger["email"]})
        pessenger['session_id'] = session
        return pessenger
    except IndexError:
        return False

def pessanger_signup(franchise_details):
    franchise_details["history"] = []
    db.pessengers.insert_one(franchise_details)
    return True


def verify_session_session(session_id):
    sessions = db.sessions.find({'session_id':session_id})
    try:
        session = parse_json(sessions[0])
        if session['user_previliges'] == 'pessenger':
            user = parse_json(db.pessengers.find({'email':session['email']})[0])
            return user
        return False

    except IndexError:
        return False



def add_route(route_details):
    db.routes.insert_one(route_details)
    return True



def get_all_routes():
    routes = db.routes.find({})
    return parse_json(routes)


def delete_route(route_details):
    db.routes.delete_many(route_details)
    return True


def parse_json(data):
    return json.loads(json_util.dumps(data))