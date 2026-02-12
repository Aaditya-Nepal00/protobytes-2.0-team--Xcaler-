from flask import Blueprint, request, jsonify
from app import db
from app.models.corruption_report import CorruptionReport

corruption_bp = Blueprint('corruption', __name__)


@corruption_bp.route('/reports', methods=['GET'])
def get_reports():
    """Get corruption reports (public view - no tracking IDs)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None)
    severity = request.args.get('severity', None)
    category = request.args.get('category', None)

    query = CorruptionReport.query

    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    if category:
        query = query.filter_by(category=category)

    pagination = query.order_by(CorruptionReport.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'reports': [r.to_public_dict() for r in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
    }), 200


@corruption_bp.route('/reports', methods=['POST'])
def submit_report():
    """Submit a corruption report (no auth required for anonymous)"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title', '').strip()
    description = data.get('description', '').strip()

    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    tracking_id = CorruptionReport.generate_tracking_id()

    report = CorruptionReport(
        title=title,
        description=description,
        tracking_id=tracking_id,
        department=data.get('department'),
        district=data.get('district'),
        province=data.get('province'),
        category=data.get('category', 'general'),
        severity=data.get('severity', 'medium'),
        anonymous=data.get('anonymous', True),
        location=data.get('location'),
        amount_involved=data.get('amount_involved'),
    )

    if report.anonymous:
        report.anonymous_hash = CorruptionReport.generate_anonymous_hash(tracking_id)

    db.session.add(report)
    db.session.commit()

    return jsonify({
        'message': 'Report submitted successfully',
        'tracking_id': tracking_id,
    }), 201


@corruption_bp.route('/reports/track/<tracking_id>', methods=['GET'])
def track_report(tracking_id):
    """Track a report by its anonymous tracking ID"""
    report = CorruptionReport.query.filter_by(tracking_id=tracking_id).first()
    if not report:
        return jsonify({'error': 'Report not found'}), 404

    return jsonify({
        'title': report.title,
        'status': report.status,
        'severity': report.severity,
        'category': report.category,
        'created_at': report.created_at.isoformat() if report.created_at else None,
        'updated_at': report.updated_at.isoformat() if report.updated_at else None,
    }), 200


@corruption_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get corruption reporting statistics"""
    total = CorruptionReport.query.count()
    by_status = {}
    for status in ['submitted', 'under_review', 'investigating', 'resolved', 'dismissed']:
        by_status[status] = CorruptionReport.query.filter_by(status=status).count()

    by_severity = {}
    for severity in ['low', 'medium', 'high', 'critical']:
        by_severity[severity] = CorruptionReport.query.filter_by(severity=severity).count()

    by_category = {}
    categories = db.session.query(CorruptionReport.category).distinct().all()
    for cat in categories:
        if cat[0]:
            by_category[cat[0]] = CorruptionReport.query.filter_by(category=cat[0]).count()

    return jsonify({
        'total': total,
        'by_status': by_status,
        'by_severity': by_severity,
        'by_category': by_category,
    }), 200
