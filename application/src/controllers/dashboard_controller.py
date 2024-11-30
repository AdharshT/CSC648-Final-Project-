# Class: CSC-648-848 Fall 2024
# Filename: dashboard_controller.py
# Author(s): Devon Huang, Thiha Aung
# Created: 2024-11-14
# Description: This file contains the route for users to a list with list_users_tutor_postings

from flask import (
    Blueprint,
    current_app,
    session,
    render_template,
    redirect,
    url_for,
)
from models.tutor_postings import list_tutor_postings
from config import get_db_connection

dashboard_blueprint = Blueprint("dashboard_backend", __name__)


@dashboard_blueprint.route("/dashboard", methods=["GET"])
def dashboard():
    # Check if the user is logged in by verifying the session
    user_id = session.get("user_id")
    if not user_id:
        current_app.logger.warning("Unauthorized access attempt to dashboard.")
        return redirect(
            url_for("frontend.login_form")
        )  # Redirect to login if not logged in

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch all tutor postings for the in-session user
        tutor_postings = list_tutor_postings(cursor, user_id)
        current_app.logger.info(
            f"Loaded {len(tutor_postings)} tutor postings for user ID {user_id}."
        )

    except Exception as e:
        current_app.logger.error(f"Failed to load tutor postings: {e}")
        return f"Failed to load tutor postings: {e}", 500

    finally:
        cursor.close()
        conn.close()

    # Render the dashboard template with the tutor postings
    return render_template("tutor_dashboard.html", tutor_postings=tutor_postings)