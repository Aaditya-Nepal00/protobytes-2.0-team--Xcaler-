from app import db
from datetime import datetime
import uuid
import hashlib
import secrets


class CorruptionReport(db.Model):
    __tablename__ = 'corruption_reports'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tracking_id = db.Column(db.String(64), unique=True, nullable=False)  # anonymous tracking token
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(255))
    district = db.Column(db.String(100))
    province = db.Column(db.String(100))
    category = db.Column(db.String(100))  # bribery, embezzlement, fraud, nepotism, etc.
    severity = db.Column(db.String(50), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(50), default='submitted')  # submitted, under_review, investigating, resolved, dismissed
    evidence_files = db.Column(db.Text)  # JSON list of file paths (encrypted)
    anonymous = db.Column(db.Boolean, default=True)
    anonymous_hash = db.Column(db.String(64))  # SHA-256 hash for anonymous ID
    reporter_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)  # null if anonymous
    location = db.Column(db.String(255))
    amount_involved = db.Column(db.Float)
    date_of_incident = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def generate_tracking_id():
        """Generate a unique anonymous tracking ID"""
        return secrets.token_hex(16)

    @staticmethod
    def generate_anonymous_hash(data):
        """Generate SHA-256 hash for anonymous identification"""
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'tracking_id': self.tracking_id,
            'title': self.title,
            'description': self.description,
            'department': self.department,
            'district': self.district,
            'province': self.province,
            'category': self.category,
            'severity': self.severity,
            'status': self.status,
            'anonymous': self.anonymous,
            'location': self.location,
            'amount_involved': self.amount_involved,
            'date_of_incident': self.date_of_incident.isoformat() if self.date_of_incident else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_public_dict(self):
        """Public info - no tracking ID or reporter info"""
        data = self.to_dict()
        data.pop('tracking_id', None)
        return data

    def __repr__(self):
        return f'<CorruptionReport {self.title}>'
