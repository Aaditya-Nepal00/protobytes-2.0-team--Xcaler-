from app import db
from datetime import datetime
import uuid


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # vote, comment, reply, report_update, system
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text)
    reference_type = db.Column(db.String(50))  # thread, comment, report
    reference_id = db.Column(db.String(36))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'reference_type': self.reference_type,
            'reference_id': self.reference_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Notification {self.type} for {self.user_id}>'
