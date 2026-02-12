from app import db
from datetime import datetime
import uuid


class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fiscal_year = db.Column(db.String(20), nullable=False)  # e.g. "2080/81"
    ministry = db.Column(db.String(255))
    department = db.Column(db.String(255))
    sector = db.Column(db.String(100))  # education, health, infrastructure, etc.
    program = db.Column(db.String(255))
    allocated = db.Column(db.Float, default=0)
    released = db.Column(db.Float, default=0)
    spent = db.Column(db.Float, default=0)
    level = db.Column(db.String(50))  # federal, provincial, local
    province = db.Column(db.String(100))
    source = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def utilization_rate(self):
        if self.allocated and self.allocated > 0:
            return round((self.spent / self.allocated) * 100, 1)
        return 0

    def to_dict(self):
        return {
            'id': self.id,
            'fiscal_year': self.fiscal_year,
            'ministry': self.ministry,
            'department': self.department,
            'sector': self.sector,
            'program': self.program,
            'allocated': self.allocated,
            'released': self.released,
            'spent': self.spent,
            'utilization_rate': self.utilization_rate,
            'level': self.level,
            'province': self.province,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Budget {self.sector} {self.fiscal_year}>'
