from flask import Blueprint, render_template

from data import SAMPLE_NOTIFICATIONS

bp = Blueprint("notifications", __name__)


@bp.route("/notifications")
def notifications():
    return render_template("notifications.html", notifications=SAMPLE_NOTIFICATIONS)
