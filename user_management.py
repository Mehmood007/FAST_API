import flask_pymongo
import json
from bson import json_util
import uuid

#Connection with Database
try:
    mongo = flask_pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo.fast
    

    
    mongo.server_info()
except:
    print("Error cannot connect to db")



def pessanger_login(login_credentials):
    pessenger = db.pessengers.find({"email":login_credentials['email'],'password':login_credentials['password']})
    try:
        pessenger = parse_json(pessenger[0])
        session = dict(pessenger['_id'])['$oid']+str(uuid.uuid4())
        db.sessions.insert_one({'session_id':session,'user_previliges':'pessenger',"email": pessenger["franchise_id"]})
        pessenger['session_id'] = session
        return pessenger
    except IndexError:
        return False

def pessanger_signup(pessenger_details):
    pessenger_details["history"] = []
    db.pessengers.insert_one(pessenger_details)
    return True


def verify_session_session(session_id):
    sessions = db.sessions.find({'session_id':session_id})
    try:
        session = parse_json(sessions[0])
        if session['user_previliges'] == 'pessenger':
            return True
        return False

    except IndexError:
        return False


def parse_json(data):
    return json.loads(json_util.dumps(data))