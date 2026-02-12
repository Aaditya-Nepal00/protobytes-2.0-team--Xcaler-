from app import db
from datetime import datetime
import uuid


class Tender(db.Model):
    __tablename__ = 'tenders'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    organization = db.Column(db.String(255))
    budget = db.Column(db.Float)
    deadline = db.Column(db.DateTime)
    published_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='open')  # open, closed, awarded, cancelled
    category = db.Column(db.String(100))
    location = db.Column(db.String(255))
    district = db.Column(db.String(100))
    source_url = db.Column(db.String(500))
    awarded_to = db.Column(db.String(255))
    awarded_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bids = db.relationship('TenderBid', backref='tender', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'organization': self.organization,
            'budget': self.budget,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'status': self.status,
            'category': self.category,
            'location': self.location,
            'district': self.district,
            'source_url': self.source_url,
            'awarded_to': self.awarded_to,
            'awarded_amount': self.awarded_amount,
            'bid_count': self.bids.count() if self.bids else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Tender {self.title}>'


class TenderBid(db.Model):
    __tablename__ = 'tender_bids'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tender_id = db.Column(db.String(36), db.ForeignKey('tenders.id'), nullable=False)
    bidder_name = db.Column(db.String(255), nullable=False)
    bid_amount = db.Column(db.Float, nullable=False)
    technical_score = db.Column(db.Float)
    financial_score = db.Column(db.Float)
    status = db.Column(db.String(50), default='submitted')  # submitted, evaluated, awarded, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tender_id': self.tender_id,
            'bidder_name': self.bidder_name,
            'bid_amount': self.bid_amount,
            'technical_score': self.technical_score,
            'financial_score': self.financial_score,
            'status': self.status,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
        }

    def __repr__(self):
        return f'<TenderBid {self.bidder_name} - {self.bid_amount}>'
