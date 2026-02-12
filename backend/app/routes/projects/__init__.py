from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('', methods=['GET'])
def get_projects():
    """Get all projects with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None)
    category = request.args.get('category', None)
    district = request.args.get('district', None)
    province = request.args.get('province', None)

    query = Project.query

    if status:
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
    if district:
        query = query.filter_by(district=district)
    if province:
        query = query.filter_by(province=province)

    pagination = query.order_by(Project.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'projects': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
    }), 200


@projects_bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get a single project"""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify(project.to_dict()), 200


@projects_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get project statistics"""
    total = Project.query.count()
    completed = Project.query.filter_by(status='completed').count()
    ongoing = Project.query.filter_by(status='ongoing').count()
    delayed = Project.query.filter_by(status='delayed').count()
    inactive = Project.query.filter_by(status='inactive').count()

    total_budget = db.session.query(db.func.sum(Project.budget)).scalar() or 0
    total_spent = db.session.query(db.func.sum(Project.spent)).scalar() or 0

    return jsonify({
        'total': total,
        'completed': completed,
        'ongoing': ongoing,
        'delayed': delayed,
        'inactive': inactive,
        'total_budget': total_budget,
        'total_spent': total_spent,
    }), 200
