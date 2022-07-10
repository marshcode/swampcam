import os

from swampcam.web import templates

import flask

def create():
    template_dir = os.path.dirname(os.path.abspath(templates.__file__))
    app = flask.Flask("admin", template_folder=template_dir)


    @app.route("/")
    def index():
        # return the rendered template
        return flask.render_template("index.html")

    return app