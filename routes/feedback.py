from flask import Blueprint, render_template, request, redirect, session

from data import SAMPLE_FEEDBACK

bp = Blueprint("feedback", __name__)


@bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    feedback_list = list(session.get("demo_feedback", SAMPLE_FEEDBACK))

    if request.method == "POST":
        review = {
            "name": request.form.get("name", "Passenger"),
            "rating": int(request.form.get("rating", 5)),
            "comment": request.form.get("comment", "Travel experience was excellent.")
        }
        feedback_list.insert(0, review)
        session["demo_feedback"] = feedback_list
        return redirect("/feedback")

    return render_template("feedback.html", feedbacks=feedback_list)
