from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from services.receso_service import RecesoService

recesos_bp = Blueprint("recesos", __name__)
service = RecesoService()

@recesos_bp.get("")
def get_recesos():
    """
    Obtener recesos
    ---
    tags:
      - Recesos
    parameters:
      - name: nombre
        in: query
        type: string
        required: false
        description: Nombre del receso para filtrar (ej. ALMUERZO)
    responses:
      200:
        description: Lista de recesos
    """
    nombre = request.args.get("nombre")
    if nombre is not None and nombre.strip() != "":
        return jsonify(service.buscar_por_nombre(nombre.strip())), 200
    return jsonify(service.listar()), 200


@recesos_bp.post("")
def post_receso():
    """
    Crear un receso
    ---
    tags:
      - Recesos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            id_t:
              type: integer
              example: 1
            hora_inicio:
              type: string
              example: "08:00:00"
            hora_fin:
              type: string
              example: "09:00:00"
            total:
              type: string
              example: "01:00:00"
            nombre:
              type: string
              example: "ALMUERZO"
            descripcion:
              type: string
              example: "Receso principal"
            tipo:
              type: string
              example: "NORMAL"
    responses:
      201:
        description: Receso creado correctamente
      400:
        description: Datos inválidos
      500:
        description: Error interno
    """
    data = request.get_json(silent=True) or {}
    try:
        receso = service.crear(data)
        return jsonify(receso), 201
    except ValidationError as ve:
        return jsonify({"error": "Datos invalidos", "detail": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Error interno", "detail": str(e)}), 500


@recesos_bp.put("/<int:receso_id>")
def put_receso(receso_id: int):
    """
    Actualizar un receso
    ---
    tags:
      - Recesos
    parameters:
      - name: receso_id
        in: path
        type: integer
        required: true
        description: ID del receso a actualizar
      - in: body
        name: body
        required: true
    responses:
      200:
        description: Receso actualizado correctamente
      404:
        description: Receso no encontrado
      400:
        description: Datos inválidos
      500:
        description: Error interno
    """
    data = request.get_json(silent=True) or {}
    try:
        receso = service.actualizar(receso_id, data)
        if receso is None:
            return jsonify({"error": "Receso no encontrado"}), 404
        return jsonify(receso), 200
    except ValidationError as ve:
        return jsonify({"error": "Datos invalidos", "detail": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Error interno", "detail": str(e)}), 500
