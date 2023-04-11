from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)


@app.route('/')
def index():
    response = make_response(
        {
            "message": "Hello Campers!"
        },
        200
    )
    return response

@app.route('/campers', methods=['GET', 'POST'])
def get_campers():
    if request.method == 'GET':
        return [camper.to_dict() for camper in Camper.query.all()]
    elif request.method == 'POST':
        new_camper = request.get_json()
        try:
            camper = Camper(
                name=new_camper.get('name'),
                age=new_camper.get('age')
            )
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict()
        except ValueError:
            return {'error': '400: Validation error'}, 400
        
@app.route('/campers/<int:id>')
def get_campers_by_id(id):
    campa = Camper.query.filter_by(id=id).first()
    if campa != None:
        return campa.to_dict()
    else:
        return {"error": "404: Camper not found"}, 404

    
@app.route('/activities')
def get_activities():
    return [activity.to_dict() for activity in Activity.query.all()]

@app.route('/activities/<int:id>')
def delete_activities(id):
    activity = Activity.query.filter_by(id=id).first()

    if activity != None:
        db.session.delete(activity)
        db.session.commit()
        return {'deleted':'the thing'}, 200
    else:
        return {'error': '404: Activity not found'}, 400

@app.route('/signups', methods=['POST'])
def signup():
    soop = request.get_json()
    try:
        signup = Signup(
            time=soop['time'],
            camper_id=soop['camper_id'],
            activity_id=soop['activity_id']
        )
        db.session.add(signup)
        db.session.commit()
        return signup.to_dict()
    except ValueError:
        return {'error': '400: Validation error'}, 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
