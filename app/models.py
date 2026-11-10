from datetime import datetime, timezone
import string
import random

from app import db


class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    priority = db.Column(db.String(20), nullable=False, default="Medium")
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    @staticmethod
    def generate_complaint_id():
        prefix = "FMC"
        year = datetime.now(timezone.utc).year
        suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        candidate = f"{prefix}-{year}-{suffix}"
        while Complaint.query.filter_by(complaint_id=candidate).first():
            suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            candidate = f"{prefix}-{year}-{suffix}"
        return candidate

    def to_dict(self):
        return {
            "id": self.id,
            "complaint_id": self.complaint_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "category": self.category,
            "location": self.location,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "admin_notes": self.admin_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Complaint {self.complaint_id}>"


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Admin {self.username}>"
