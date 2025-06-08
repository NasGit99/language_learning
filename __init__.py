from flask import Flask, render_template
import sys
import os

from templates.blueprints.main_bp import main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
   program = create_app()
   program.run(host="0.0.0.0", port=8000, debug=True)
