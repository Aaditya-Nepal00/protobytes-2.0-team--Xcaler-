from app import db
from datetime import datetime
import uuid


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin, moderator
    avatar = db.Column(db.String(255), default=None)
    karma = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    threads = db.relationship('DiscussionThread', backref='author', lazy='dynamic',
                              foreign_keys='DiscussionThread.author_id')
    comments = db.relationship('ThreadComment', backref='author', lazy='dynamic',
                               foreign_keys='ThreadComment.author_id')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'avatar': self.avatar,
            'karma': self.karma,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def to_public_dict(self):
        """Public info only - no email"""
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'karma': self.karma,
        }

    def __repr__(self):
        return f'<User {self.email}>'
