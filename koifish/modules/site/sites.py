from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

module = Blueprint("site", __name__)


@module.route("/")
def index():
    return redirect(url_for("dashboard.index"))
