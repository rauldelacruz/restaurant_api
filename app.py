import os
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#\copy restaurants(id,rating,name,site,email, phone, street, city, state, lat, lng) FROM '~/Downloads/restaurantes.csv' DELIMITERS ',' CSV HEADER;
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Restaurant

@app.route("/restaurants", methods=['POST'])
def create_restaurant():
    req = request.get_json()
    id = req['id']
    rating = req['rating']
    name = req['name']
    site = req['site']
    phone = req['phone']
    email = req['email']
    street = req['street']
    state = req['state']
    city = req['city']
    state = req['state']
    lat = req['lat']
    lng = req['lng']
    try:
        restaurant = Restaurant(
            id = id,
            rating = rating,
            name = name,
            site = site,
            email = email,
            phone = phone,
            street = street,
            city = city,
            state = state,
            lat = lat,
            lng = lng
        )
        db.session.add(restaurant)
        db.session.commit()
        return  make_response("",201)
    except Exception as e:
	    return make_response("",409)

@app.route('/restaurants' ,methods = ['GET'])
def get_all():
    try:
        restaurants = Restaurant.query.all()
        return make_response(jsonify([e.serialize() for e in restaurants]),200)
    except Exception as e:
	    return make_response("",404)

@app.route('/restaurants/<id_>', methods = ['GET'])
def get_by_id(id_):
    try:
        restaurant = Restaurant.query.filter_by(id=id_).first()
        return make_response(jsonify(restaurant.serialize()), 200)
    except Exception as e:
	    return make_response("",404)

@app.route('/restaurants/<id_>', methods=['DELETE'])
def delete_restaurant(id_):
    try:
        restaurant = Restaurant.query.filter_by(id=id_).first()
        db.session.delete(restaurant)
        db.session.commit()
        return make_response("",200)
    except Exception as e:
        return make_response("",404)

@app.route("/restaurants//<id_>", methods=['PUT'])
def update_restaurant_by_id(id_):
    try:
        restaurant = Restaurant.query.filter_by(id=id_).first()
        req = request.get_json()
        if req.get('rating'):
            restaurant.rating = req['rating']
        if req.get('name'):
            restaurant.name = req['name']
        if req.get('site'):
            restaurant.site = req['site']
        if req.get('phone'):
            restaurant.phone = req['phone']
        if req.get('email'):
            restaurant.email = req['email']
        if req.get('street'):
            restaurant.street = req['street']
        if req.get('state'):
            restaurant.state = req['state']
        if req.get('city'):
            restaurant.city = req['city']
        if req.get('state'):
            restaurant.state = req['state']
        if req.get('lat'):
            restaurant.lat = req['lat']
        if req.get('lng'):
            restaurant.lng = req['lng']
        db.session.commit()
        return make_response("",200)
    except Exception as e:
        return make_response("",404)

@app.route('/statistics', methods = ['GET'])
def get_stats():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        radius = request.args.get('radius')
        sql = "SELECT COUNT(*) AS count,ROUND(AVG(rating),2) as avg,ROUND(stddev_pop(rating),3) as std FROM restaurants r WHERE ST_DWithin(ST_MakePoint(r.lat,r.lng), ST_MakePoint({}, {}), {}, true)"
        result = db.session.execute(sql.format(latitude, longitude, radius))
        stats = result.first()
        a = jsonify(count=stats['count'],
                    avg=float(stats['avg']),
                    std=float(stats['std']))     
        return make_response(a, 200)
    except Exception as e:
        print(e)
        return make_response("",400)

if __name__ == '__main__':
    app.run()