from flask import Blueprint, render_template, request, redirect, session

from data import SAMPLE_COMPLAINTS

bp = Blueprint("complaints", __name__)


@bp.route("/complaints", methods=["GET", "POST"])
def complaints():
    complaints_list = list(session.get("demo_complaints", SAMPLE_COMPLAINTS))

    if request.method == "POST":
        complaint = {
            "id": len(complaints_list) + 101,
            "title": request.form.get("title", "New complaint"),
            "category": request.form.get("category", "General"),
            "status": "In Review",
            "message": request.form.get("message", "No description provided")
        }
        complaints_list.insert(0, complaint)
        session["demo_complaints"] = complaints_list
        return redirect("/complaints")

    return render_template("complaints.html", complaints=complaints_list)
