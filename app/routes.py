from flask import render_template

from app import flask_app


@flask_app.route("/")
@flask_app.route("/about_me")
def about_me():
    return render_template("about_me.html")
