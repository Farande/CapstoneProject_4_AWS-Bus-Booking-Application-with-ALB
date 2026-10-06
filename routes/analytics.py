from flask import Blueprint, render_template

from data import SAMPLE_ANALYTICS

bp = Blueprint("analytics", __name__)


@bp.route("/analytics")
def analytics():
    return render_template("analytics.html", analytics=SAMPLE_ANALYTICS)
