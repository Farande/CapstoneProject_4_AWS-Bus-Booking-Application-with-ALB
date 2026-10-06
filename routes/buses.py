from flask import Blueprint, render_template, request

from db import get_db_connection, safe_close
from data import get_sample_buses

bp = Blueprint("buses", __name__)


@bp.route("/buses")
def buses():
    source = (request.args.get("source") or "").strip()
    destination = (request.args.get("destination") or "").strip()

    result = get_sample_buses(source, destination)
    connection = get_db_connection()

    if connection is not None:
        try:
            with connection.cursor() as cursor:
                if source and destination:
                    sql = """
                    SELECT *
                    FROM Buses
                    WHERE source=%s
                    AND destination=%s
                    """
                    cursor.execute(sql, (source, destination))
                else:
                    cursor.execute("SELECT * FROM Buses")

                result = cursor.fetchall()
        except Exception:
            result = get_sample_buses(source, destination)
        finally:
            safe_close(connection)

    return render_template("buses.html", buses=result)
