from flask import Blueprint, render_template

from data import SAMPLE_AI_ASSISTANT

bp = Blueprint("assistant", __name__)


@bp.route("/assistant")
@bp.route("/ai-assistant")
def assistant():
    return render_template("assistant.html", suggestions=SAMPLE_AI_ASSISTANT)
