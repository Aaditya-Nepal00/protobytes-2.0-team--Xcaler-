from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
import os

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.projects import projects_bp
    from app.routes.tenders import tenders_bp
    from app.routes.budget import budget_bp
    from app.routes.corruption import corruption_bp
    from app.routes.laws import laws_bp
    from app.routes.forum import forum_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(tenders_bp, url_prefix='/api/tenders')
    app.register_blueprint(budget_bp, url_prefix='/api/budget')
    app.register_blueprint(corruption_bp, url_prefix='/api/corruption')
    app.register_blueprint(laws_bp, url_prefix='/api/laws')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')

    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'Sachet API is running'}, 200

    with app.app_context():
        from app.models import (User, Project, Tender, TenderBid, Budget,
                                CorruptionReport, Law, DiscussionThread,
                                ThreadComment, ThreadVote, NewsArticle, Notification)
        db.create_all()

    return app
