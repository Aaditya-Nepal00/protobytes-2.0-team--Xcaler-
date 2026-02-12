from app import db
from datetime import datetime
import uuid


class DiscussionThread(db.Model):
    __tablename__ = 'discussion_threads'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    anonymous_name = db.Column(db.String(100))  # e.g. "Anonymous Citizen #4829"
    category = db.Column(db.String(100))  # governance, corruption, budget, law, general
    tags = db.Column(db.String(500))  # comma-separated
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    is_pinned = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    comments = db.relationship('ThreadComment', backref='thread', lazy='dynamic',
                               order_by='ThreadComment.created_at')
    votes = db.relationship('ThreadVote', backref='thread', lazy='dynamic')

    @property
    def score(self):
        return self.upvotes - self.downvotes

    def to_dict(self, include_content=True):
        data = {
            'id': self.id,
            'title': self.title,
            'author': self.author.to_public_dict() if self.author and not self.is_anonymous else None,
            'is_anonymous': self.is_anonymous,
            'anonymous_name': self.anonymous_name if self.is_anonymous else None,
            'category': self.category,
            'tags': self.tags.split(',') if self.tags else [],
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'score': self.score,
            'comment_count': self.comment_count,
            'view_count': self.view_count,
            'is_pinned': self.is_pinned,
            'is_locked': self.is_locked,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_content:
            data['content'] = self.content
        return data

    def __repr__(self):
        return f'<DiscussionThread {self.title}>'


class ThreadComment(db.Model):
    __tablename__ = 'thread_comments'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = db.Column(db.String(36), db.ForeignKey('discussion_threads.id'), nullable=False)
    parent_id = db.Column(db.String(36), db.ForeignKey('thread_comments.id'), nullable=True)  # for nesting
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    anonymous_name = db.Column(db.String(100))
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Self-referential for nested comments
    replies = db.relationship('ThreadComment', backref=db.backref('parent', remote_side=[id]),
                              lazy='dynamic')
    votes = db.relationship('ThreadVote', backref='comment', lazy='dynamic',
                            foreign_keys='ThreadVote.comment_id')

    @property
    def score(self):
        return self.upvotes - self.downvotes

    def to_dict(self, depth=0, max_depth=3):
        data = {
            'id': self.id,
            'thread_id': self.thread_id,
            'parent_id': self.parent_id,
            'content': self.content if not self.is_deleted else '[deleted]',
            'author': self.author.to_public_dict() if self.author and not self.is_anonymous else None,
            'is_anonymous': self.is_anonymous,
            'anonymous_name': self.anonymous_name if self.is_anonymous else None,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'score': self.score,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reply_count': self.replies.count() if self.replies else 0,
        }
        if depth < max_depth:
            data['replies'] = [r.to_dict(depth=depth + 1, max_depth=max_depth)
                               for r in self.replies.filter_by(is_deleted=False).all()]
        return data

    def __repr__(self):
        return f'<ThreadComment on thread {self.thread_id}>'


class ThreadVote(db.Model):
    __tablename__ = 'thread_votes'
 
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    thread_id = db.Column(db.String(36), db.ForeignKey('discussion_threads.id'), nullable=True)
    comment_id = db.Column(db.String(36), db.ForeignKey('thread_comments.id'), nullable=True)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure a user can only vote once per thread/comment
    __table_args__ = (
        db.UniqueConstraint('user_id', 'thread_id', name='unique_thread_vote'),
        db.UniqueConstraint('user_id', 'comment_id', name='unique_comment_vote'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'thread_id': self.thread_id,
            'comment_id': self.comment_id,
            'vote_type': self.vote_type,
        }

    def __repr__(self):
        return f'<ThreadVote {self.vote_type} by {self.user_id}>'
