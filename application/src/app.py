from flask import (
    Blueprint,
    current_app,
    Flask,
    render_template,
    abort,
    url_for,
    redirect,
    request,
)
from collections import namedtuple
import os
from models.tutor_postings import (
    search_tutor_postings,
    is_valid_subject,
    get_tutor_count,
    get_subjects,
)

frontend = Blueprint("frontend", __name__)


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(frontend)
    app.subjects = get_subjects()
    return app


Member = namedtuple("Member", ["name", "role", "profile", "image_url"])
members = {
    "usatie": Member(
        "Shun Usami",
        "Team Lead",
        "Software Engineer + Entrepreneur + Father",
        "images/usatie.jpg",
    ),
    "AdharshT": Member(
        "Adharsh Thiagarajan", "Frontend Lead", "Make Music", "images/adharsh.jpg"
    ),
    "Novedh": Member(
        "Devon Huang",
        "Backend Lead",
        "Hobby enthusiast + Dog dad + Student",
        "images/devon.jpg",
    ),
    "kimbucha": Member(
        "Kim Nguyen", "Github Master", "Yerba Mate Enthusiast", "images/kim.jpg"
    ),
    "thihaaung32": Member(
        "Thiha Aung",
        "Software Developer",
        "Reading + Exploring + Learning",
        "images/thiha.jpg",
    ),
}


@frontend.route("/")
def home():
    return redirect("/about")


@frontend.route("/about")
def about():
    return render_template(
        "about.html",
        members=members,
        subjects=current_app.subjects,
    )


@frontend.route("/search", methods=["GET"])
def search():

    selected_subject = request.args.get("subject", "All")
    search_text = request.args.get("search_text", "").strip()

    # Validate the selected subject (from models/tutor_postings)
    if not is_valid_subject(selected_subject, current_app.subjects):
        abort(400)

    # Get tutor postings and count (from models/tutor_postings)
    tutor_postings = search_tutor_postings(selected_subject, search_text)
    results_count = get_tutor_count(selected_subject, search_text)

    return render_template(
        "search_results.html",
        subjects=current_app.subjects,
        tutor_postings=tutor_postings,
        selected_subject=selected_subject,
        search_text=search_text,
        results_count=results_count,
    )


@frontend.route("/about/<name>")
def about_member_detail(name):
    member = members.get(name)
    if member:
        return render_template(
            "member_detail.html",
            member=member,
            subjects=current_app.subjects,
        )
    else:
        abort(404)


@frontend.route("/tutor_signup", methods=["GET", "POST"])
def tutor_signup():
    if request.method == "POST":
        # Process the form data here
        subject = request.form.get("subject")
        course_number = request.form.get("course_number")
        description = request.form.get("description")
        pay_rate = request.form.get("pay_rate")
        profile_picture = request.files.get("profile_picture")

        # TODO store the data in a database or carry out further processing

        return redirect(url_for("home_page"))

    return render_template(
        "TutorSignUpPage.html",
        subjects=current_app.subjects,
    )


@frontend.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # TODO: verify email and password with database

        return redirect(url_for("frontend.dashboard"))

    return render_template(
        "login.html",
        subjects=current_app.subjects,
    )


@frontend.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        # TODO check duplicate emails , check password length and reqirements?

        # TODO bcrypt password, save info into DB

        return redirect(url_for("frontend.login"))

    return render_template(
        "register.html",
        subjects=current_app.subjects,
    )


@frontend.route("/dashboard")
def dashboard():
    return render_template(
        "tutor_dashboard.html",
        subjects=current_app.subjects,
    )
