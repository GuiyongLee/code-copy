from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from flask import request, jsonify, abort

db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from app.models import Bucketlist
    @app.route('/bucketlists/', methods=['POST','GET'])
    def bucketlists():
        if request.method == "POST":
            # Don't understand this line.
            name = str(request.data.get('name',''))
    
            if name:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = jsonify({
                        'id' : bucketlist.id,
                        'name' : bucketlist.name,
                        'date_created' : bucketlist.date_created,
                        'date_modified' : bucketlist.date_modified })
                response.status_code = 201
                return response
        else:
            
            bucketlists = Bucketlist.get_all()
            results = [] 
            for bucketlist in bucketlists:
                obj = {
                    'id' : bucketlist.id,
                    'name' : bucketlist.name,
                    'date_created' : bucketlist.date_created,
                    'date_modified' : bucketlist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    @app.route('/bucketlists/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)
        if request.method == 'DELETE':
            bucketlist.delete()
            return { "message":"bucketlist {} deleted.".format(bucketlist.id)}, 200
        elif request.method == 'PUT':
            name = str(request.data.get('name',''))
            
            bucketlist.name = name
            bucketlist.save()
    
            response = jsonify({
                    'id' : bucketlist.id,
                    'name' : bucketlist.name,
                    'date_created' : bucketlist.date_created,
                    'date_modified' : bucketlist.date_modified})
            response.status_code = 200
            
            return response
        else:
            response = jsonify({
                    'id' : bucketlist.id,
                    'name' : bucketlist.name,
                    'date_created' : bucketlist.date_created,
                    'date_modified' : bucketlist.date_modified})
            response.status_code = 200
            return response

    return app
