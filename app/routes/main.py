from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app import db
from app.models import Complaint
from app.forms import ComplaintForm, TrackForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/report", methods=["GET", "POST"])
def report():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            complaint_id=Complaint.generate_complaint_id(),
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=(form.phone.data or "").strip(),
            category=form.category.data,
            location=form.location.data.strip(),
            description=form.description.data.strip(),
            status="Pending",
            priority="Medium",
        )
        db.session.add(complaint)
        db.session.commit()
        flash(f"Your complaint has been registered successfully. Complaint ID: {complaint.complaint_id}", "success")
        return redirect(url_for("main.track_result", complaint_id=complaint.complaint_id))
    return render_template("report.html", form=form)


@main_bp.route("/track", methods=["GET", "POST"])
def track():
    form = TrackForm()
    if form.validate_on_submit():
        return redirect(url_for("main.track_result", complaint_id=form.complaint_id.data.strip()))
    return render_template("track.html", form=form)


@main_bp.route("/track/<complaint_id>")
def track_result(complaint_id):
    complaint = Complaint.query.filter_by(complaint_id=complaint_id).first()
    if not complaint:
        flash("No complaint found with that ID. Please check and try again.", "danger")
        return redirect(url_for("main.track"))
    return render_template("track_result.html", complaint=complaint)
