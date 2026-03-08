from app import db
from datetime import datetime

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)  # e.g., 2.5 baths
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)       
    property_type = db.Column(db.String(20), nullable=False)  # 'House' or 'Apartment'
    photo_filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    currency = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Property {self.title}>'