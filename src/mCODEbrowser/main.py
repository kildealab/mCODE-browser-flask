from flask import Flask, render_template, jsonify
from flask_wtf.csrf import CSRFProtect

from dotenv import dotenv_values
from pathlib import Path
from werkzeug.exceptions import HTTPException


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

config = dotenv_values(BASE_DIR / '.env')

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config.update(
            dict(
                SECRET_KEY=config.get('SECRET_KEY'),
                WTF_CSRF_SECRET_KEY=config.get('WTF_CSRF_SECRET_KEY'),
                SUPABASE_URL=config.get('SUPABASE_URL'),
                SUPABASE_API_KEY=config.get('SUPABASE_API_KEY'),
            )
        )
        csrf.init_app(app)
        app.static_folder = config.get('STATIC_ROOT', BASE_DIR / "static")

        # routes '/api/...'
        from api.routes import api
        app.register_blueprint(api)

    @app.errorhandler(Exception)
    def handle_global_exception(e):
        """Global error handler for all unhandled exceptions."""

        # Case 1: Handle intentional HTTP errors (404, 400, 405, etc.)
        if isinstance(e, HTTPException):
            response = {
                "error": e.name,
                "message": e.description,
                "status_code": e.code
            }
            return jsonify(response), e.code

        # Case 2: Handle unhandled code bugs/crashes (500 Internal Server Error)
        # Log the full traceback so developers can fix the root bug
        app.logger.error(f"Server Error: {str(e)}", exc_info=True)

        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server.",
            "status_code": 500
        }
        return jsonify(response), 500

    @app.route('/', methods=['GET'])
    def home():
        return render_template("index.html")

    return app
