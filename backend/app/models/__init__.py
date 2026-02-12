# Import all models
from app.models.user import User
from app.models.project import Project
from app.models.tender import Tender, TenderBid
from app.models.budget import Budget
from app.models.corruption_report import CorruptionReport
from app.models.law import Law
from app.models.forum import DiscussionThread, ThreadComment, ThreadVote
from app.models.news import NewsArticle
from app.models.notification import Notification

__all__ = [
    'User', 'Project', 'Tender', 'TenderBid', 'Budget',
    'CorruptionReport', 'Law', 'DiscussionThread', 'ThreadComment',
    'ThreadVote', 'NewsArticle', 'Notification'
]
