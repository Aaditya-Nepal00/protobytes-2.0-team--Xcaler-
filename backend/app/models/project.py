from app import db
from datetime import datetime
import uuid


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='ongoing')  # completed, ongoing, delayed, inactive
    budget = db.Column(db.Float)
    spent = db.Column(db.Float, default=0)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    expected_end_date = db.Column(db.DateTime)
    completion_percentage = db.Column(db.Float, default=0)
    location = db.Column(db.String(255))
    district = db.Column(db.String(100))
    province = db.Column(db.String(100))
    department = db.Column(db.String(255))
    contractor = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    category = db.Column(db.String(100))  # infrastructure, education, health, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'budget': self.budget,
            'spent': self.spent,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'expected_end_date': self.expected_end_date.isoformat() if self.expected_end_date else None,
            'completion_percentage': self.completion_percentage,
            'location': self.location,
            'district': self.district,
            'province': self.province,
            'department': self.department,
            'contractor': self.contractor,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Project {self.title}>'
