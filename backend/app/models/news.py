from app import db
from datetime import datetime
import uuid


class NewsArticle(db.Model):
    __tablename__ = 'news_articles'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)  # AI-generated summary
    source = db.Column(db.String(255))
    source_url = db.Column(db.String(500))
    category = db.Column(db.String(100))  # governance, corruption, budget, development
    image_url = db.Column(db.String(500))
    published_date = db.Column(db.DateTime)
    tags = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'source': self.source,
            'source_url': self.source_url,
            'category': self.category,
            'image_url': self.image_url,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'tags': self.tags.split(',') if self.tags else [],
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<NewsArticle {self.title}>'
