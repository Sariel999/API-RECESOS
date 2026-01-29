from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from routes.recesos import recesos_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuracion Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    Swagger(app, config=swagger_config)

    app.register_blueprint(recesos_bp, url_prefix="/recesos")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "Method Not Allowed"}), 405

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
