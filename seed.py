from app import create_app, db
from app.models import Admin, Complaint
from werkzeug.security import generate_password_hash
import os
import sys

app = create_app()

with app.app_context():
    db.create_all()

    username = os.environ.get("ADMIN_USERNAME") or "admin"
    password = os.environ.get("ADMIN_PASSWORD")

    if not password:
        print("ERROR: ADMIN_PASSWORD environment variable is missing or empty. "
              "Set ADMIN_PASSWORD before running seed.py.")
        sys.exit(1)

    existing = Admin.query.filter_by(username=username).first()
    if not existing:
        admin = Admin(username=username, password_hash=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created: {username}")

    sample = [
        {"name": "Aarav Sharma", "email": "aarav@college.edu", "phone": "9876543210",
         "category": "electricity", "location": "Hostel B - Room 312",
         "description": "Ceiling fan in Room 312 is not working since morning. Switchboard sparking noticed.",
         "status": "Pending", "priority": "High"},
        {"name": "Sneha Reddy", "email": "sneha@college.edu", "phone": "9123456780",
         "category": "plumbing", "location": "Girls Hostel - 2nd Floor Washroom",
         "description": "Water leakage from the washroom tap. Floor is always wet causing slip hazard.",
         "status": "In Progress", "priority": "High"},
        {"name": "Rohan Mehta", "email": "rohan@college.edu", "phone": "9988776655",
         "category": "internet", "location": "Library - Reading Hall",
         "description": "Wi-Fi signal is very weak in the reading hall. Cannot access online resources.",
         "status": "Resolved", "priority": "Medium"},
        {"name": "Kavya Iyer", "email": "kavya@college.edu", "phone": "9011223344",
         "category": "cleanliness", "location": "Canteen Courtyard",
         "description": "Garbage bins not emptied for two days. Bad smell in the courtyard area.",
         "status": "Pending", "priority": "Medium"},
        {"name": "Arjun Singh", "email": "arjun@college.edu", "phone": "8765432109",
         "category": "furniture", "location": "Lecture Hall 5",
         "description": "Two benches in Lecture Hall 5 have broken legs. Unsafe for students.",
         "status": "Rejected", "priority": "Low"},
    ]
    for s in sample:
        exists = Complaint.query.filter_by(email=s["email"], location=s["location"]).first()
        if not exists:
            c = Complaint(
                complaint_id=Complaint.generate_complaint_id(),
                status=s["status"], priority=s["priority"],
                **{k: v for k, v in s.items() if k not in ("status", "priority")}
            )
            db.session.add(c)
    db.session.commit()
    print("Sample complaints ensured.")
