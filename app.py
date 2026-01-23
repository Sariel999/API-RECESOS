from flask import Flask, jsonify
from flask_cors import CORS
from receso_service import RecesoService

app = Flask(__name__)
CORS(app)

service = RecesoService()

@app.route("/recesos", methods=["GET"])
def obtener_recesos():
    return jsonify(service.recuperar_todos())

if __name__ == "__main__":
    app.run(debug=True)
