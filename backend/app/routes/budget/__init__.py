from flask import Blueprint, request, jsonify
from app import db
from app.models.budget import Budget

budget_bp = Blueprint('budget', __name__)


@budget_bp.route('', methods=['GET'])
def get_budgets():
    """Get budget data with filtering"""
    fiscal_year = request.args.get('fiscal_year', None)
    sector = request.args.get('sector', None)
    level = request.args.get('level', None)
    ministry = request.args.get('ministry', None)

    query = Budget.query

    if fiscal_year:
        query = query.filter_by(fiscal_year=fiscal_year)
    if sector:
        query = query.filter_by(sector=sector)
    if level:
        query = query.filter_by(level=level)
    if ministry:
        query = query.filter_by(ministry=ministry)

    budgets = query.order_by(Budget.allocated.desc()).all()

    return jsonify({
        'budgets': [b.to_dict() for b in budgets],
        'total': len(budgets),
    }), 200


@budget_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get budget summary by sector"""
    fiscal_year = request.args.get('fiscal_year', '2080/81')

    budgets = Budget.query.filter_by(fiscal_year=fiscal_year).all()

    sector_summary = {}
    for b in budgets:
        if b.sector not in sector_summary:
            sector_summary[b.sector] = {'allocated': 0, 'spent': 0, 'released': 0}
        sector_summary[b.sector]['allocated'] += b.allocated or 0
        sector_summary[b.sector]['spent'] += b.spent or 0
        sector_summary[b.sector]['released'] += b.released or 0

    total_allocated = sum(s['allocated'] for s in sector_summary.values())
    total_spent = sum(s['spent'] for s in sector_summary.values())

    return jsonify({
        'fiscal_year': fiscal_year,
        'total_allocated': total_allocated,
        'total_spent': total_spent,
        'utilization_rate': round((total_spent / total_allocated * 100), 1) if total_allocated > 0 else 0,
        'sectors': sector_summary,
    }), 200


@budget_bp.route('/sectors', methods=['GET'])
def get_sectors():
    """Get unique sectors"""
    sectors = db.session.query(Budget.sector).distinct().all()
    return jsonify([s[0] for s in sectors if s[0]]), 200


@budget_bp.route('/fiscal-years', methods=['GET'])
def get_fiscal_years():
    """Get available fiscal years"""
    years = db.session.query(Budget.fiscal_year).distinct().order_by(Budget.fiscal_year.desc()).all()
    return jsonify([y[0] for y in years if y[0]]), 200
