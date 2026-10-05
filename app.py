"""Application entry point. All the actual page logic now lives in
routes/<feature>.py - this file just builds the app and wires it up."""

from flask import Flask

from ai_widget import register_ai_widget
from auth_utils import seed_default_accounts

from routes.home import bp as home_bp
from routes.auth import bp as auth_bp
from routes.buses import bp as buses_bp
from routes.booking import bp as booking_bp
from routes.history import bp as history_bp
from routes.ticket import bp as ticket_bp
from routes.assistant import bp as assistant_bp
from routes.complaints import bp as complaints_bp
from routes.lost_found import bp as lost_found_bp
from routes.status import bp as status_bp
from routes.notifications import bp as notifications_bp
from routes.analytics import bp as analytics_bp
from routes.feedback import bp as feedback_bp
from routes.admin import bp as admin_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "bus-booking-secret-key"

    seed_default_accounts()
    register_ai_widget(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(buses_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(lost_found_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
