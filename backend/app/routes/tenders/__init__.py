from flask import Blueprint, request, jsonify
from app import db
from app.models.tender import Tender, TenderBid

tenders_bp = Blueprint('tenders', __name__)


@tenders_bp.route('', methods=['GET'])
def get_tenders():
    """Get all tenders with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None)

    query = Tender.query
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Tender.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'tenders': [t.to_dict() for t in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
    }), 200


@tenders_bp.route('/<tender_id>', methods=['GET'])
def get_tender(tender_id):
    """Get a tender with its bids"""
    tender = Tender.query.get(tender_id)
    if not tender:
        return jsonify({'error': 'Tender not found'}), 404

    data = tender.to_dict()
    data['bids'] = [b.to_dict() for b in tender.bids.all()]
    return jsonify(data), 200


@tenders_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get tender statistics"""
    total = Tender.query.count()
    open_count = Tender.query.filter_by(status='open').count()
    closed = Tender.query.filter_by(status='closed').count()
    awarded = Tender.query.filter_by(status='awarded').count()
    total_value = db.session.query(db.func.sum(Tender.budget)).scalar() or 0

    return jsonify({
        'total': total,
        'open': open_count,
        'closed': closed,
        'awarded': awarded,
        'total_value': total_value,
    }), 200
