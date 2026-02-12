from flask import Blueprint, request, jsonify
from app import db
from app.models.law import Law

laws_bp = Blueprint('laws', __name__)


@laws_bp.route('', methods=['GET'])
def get_laws():
    """Get all laws with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)

    query = Law.query.filter_by(is_active=True)

    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(
            db.or_(
                Law.title.ilike(f'%{search}%'),
                Law.content.ilike(f'%{search}%'),
                Law.tags.ilike(f'%{search}%'),
            )
        )

    pagination = query.order_by(Law.year_enacted.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'laws': [l.to_summary_dict() for l in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
    }), 200


@laws_bp.route('/<law_id>', methods=['GET'])
def get_law(law_id):
    """Get a single law with full details"""
    law = Law.query.get(law_id)
    if not law:
        return jsonify({'error': 'Law not found'}), 404
    return jsonify(law.to_dict()), 200


@laws_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get unique law categories"""
    categories = db.session.query(Law.category).distinct().all()
    return jsonify([c[0] for c in categories if c[0]]), 200
