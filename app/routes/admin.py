from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app import db
from app.models import Complaint, Admin
from app.forms import AdminLoginForm, ComplaintUpdateForm
from werkzeug.security import check_password_hash, generate_password_hash

admin_bp = Blueprint("admin", __name__)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please sign in to access the admin dashboard.", "warning")
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data.strip()).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            session["admin_logged_in"] = True
            session["admin_user"] = admin.username
            flash("Welcome back, Administrator.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_user", None)
    flash("You have been signed out.", "info")
    return redirect(url_for("main.index"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    status_filter = request.args.get("status", "all")
    query = Complaint.query
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    complaints = query.order_by(Complaint.created_at.desc()).all()
    total = Complaint.query.count()
    pending = Complaint.query.filter_by(status="Pending").count()
    in_progress = Complaint.query.filter_by(status="In Progress").count()
    resolved = Complaint.query.filter_by(status="Resolved").count()
    return render_template("admin/dashboard.html",
                           complaints=complaints, status_filter=status_filter,
                           total=total, pending=pending, in_progress=in_progress, resolved=resolved)


@admin_bp.route("/complaint/<int:complaint_id>/update", methods=["POST"])
@login_required
def update_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    form = ComplaintUpdateForm()
    if form.validate_on_submit():
        complaint.status = form.status.data
        complaint.priority = form.priority.data
        complaint.admin_notes = (form.admin_notes.data or "").strip() or None
        db.session.commit()
        flash(f"Complaint {complaint.complaint_id} updated successfully.", "success")
    else:
        flash("Failed to update complaint. Please check the form.", "danger")
    return redirect(url_for("admin.dashboard"))
