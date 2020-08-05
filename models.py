from app import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.String(), primary_key=True,nullable=True)
    rating = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    site = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    street = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    lat = db.Column(db.Float(), nullable=False)
    lng = db.Column(db.Float(), nullable=False)

    def __init__(self, id, rating, name, site, email, phone, street, city, state, lat, lng):
        self.id = id
        self.rating = rating
        self.name = name
        self.site = site
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'rating': self.rating, 
            'name': self.name,
            'site': self.site,
            'email':self.email,
            'phone': self.phone,
            'street': self.street,
            'state':self.state,
            'lat': self.lat, 
            'lng': self.lng
        }
