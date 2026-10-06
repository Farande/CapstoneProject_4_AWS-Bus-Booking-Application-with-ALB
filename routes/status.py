from flask import Blueprint, render_template

from data import SAMPLE_DELAYS

bp = Blueprint("status", __name__)


@bp.route("/status")
def bus_status():
    return render_template("status.html", delays=SAMPLE_DELAYS)
