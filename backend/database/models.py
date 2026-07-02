from datetime import datetime
from .db import db

class History(db.Model):
    __tablename__ = "history"
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    pemasukan = db.Column(
        db.Float,
        nullable=False
    )
    total_pengeluaran = db.Column(
        db.Float,
        nullable=False
    )
    saldo = db.Column(
        db.Float,
        nullable=False
    )
    target = db.Column(
        db.Float,
        nullable=False
    )
    deadline = db.Column(
        db.Integer,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    def to_dict(self):
        return {
            "id": self.id,
            "pemasukan": self.pemasukan,
            "total_pengeluaran": self.total_pengeluaran,
            "saldo": self.saldo,
            "target": self.target,
            "deadline": self.deadline,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }