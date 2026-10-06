from flask import Blueprint, render_template, request, redirect, session

from data import SAMPLE_LOST_FOUND

bp = Blueprint("lost_found", __name__)


@bp.route("/lost-found", methods=["GET", "POST"])
def lost_found():
    items = list(session.get("demo_lost_found", SAMPLE_LOST_FOUND))

    if request.method == "POST":
        item = {
            "id": len(items) + 201,
            "item": request.form.get("item", "Unidentified item"),
            "location": request.form.get("location", "Terminal"),
            "status": "Reported",
            "owner": "Pending"
        }
        items.insert(0, item)
        session["demo_lost_found"] = items
        return redirect("/lost-found")

    return render_template("lost_found.html", items=items)
