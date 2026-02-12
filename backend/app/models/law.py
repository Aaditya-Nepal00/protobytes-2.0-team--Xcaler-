from app import db
from datetime import datetime
import uuid


class Law(db.Model):
    __tablename__ = 'laws'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    title_nepali = db.Column(db.String(255))
    content = db.Column(db.Text)
    content_nepali = db.Column(db.Text)
    simplified = db.Column(db.Text)  # AI-simplified version
    simplified_nepali = db.Column(db.Text)
    category = db.Column(db.String(100))  # constitutional, civil, criminal, etc.
    year_enacted = db.Column(db.Integer)
    amendment_year = db.Column(db.Integer)
    source = db.Column(db.String(255))
    source_url = db.Column(db.String(500))
    related_laws = db.Column(db.Text)  # JSON list of related law IDs
    faq = db.Column(db.Text)  # JSON list of FAQ items
    tags = db.Column(db.String(500))  # comma-separated tags
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'title_nepali': self.title_nepali,
            'content': self.content,
            'content_nepali': self.content_nepali,
            'simplified': self.simplified,
            'simplified_nepali': self.simplified_nepali,
            'category': self.category,
            'year_enacted': self.year_enacted,
            'amendment_year': self.amendment_year,
            'source': self.source,
            'source_url': self.source_url,
            'related_laws': self.related_laws,
            'faq': self.faq,
            'tags': self.tags,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def to_summary_dict(self):
        """Shorter version for list views"""
        return {
            'id': self.id,
            'title': self.title,
            'title_nepali': self.title_nepali,
            'simplified': self.simplified[:200] + '...' if self.simplified and len(self.simplified) > 200 else self.simplified,
            'category': self.category,
            'year_enacted': self.year_enacted,
            'tags': self.tags,
        }

    def __repr__(self):
        return f'<Law {self.title}>'
