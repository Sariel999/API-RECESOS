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
    summary: Listar o buscar recesos
    description: Endpoint para obtener recesos registrados. Si no se envía
      ningún parámetro, se listan todos los recesos. Si se envía el parámetro
      nombre por la URL, se filtran los recesos por dicho nombre.
    parameters:
      - name: nombre
        in: query
        type: string
        required: false
        description: Nombre del receso a buscar mediante parámetro por URL.
    responses:
      200:
        description: Lista de recesos obtenida correctamente.
        examples:
          application/json:
            - id: 17
              id_t: 8
              hora_inicio: "08:00:00"
              hora_fin: "08:15:00"
              hora_total: "00:15:00"
              nombre: "ALMUERZO"
              descripcion: "Receso principal"
              tipo: "NORMAL"
      500:
        description: Error interno del servidor.
        examples:
          application/json:
            error: "Error interno"
            detail: "Error inesperado al procesar la solicitud"
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
    summary: Crear un nuevo receso
    description: Endpoint para registrar un nuevo receso enviando los datos
      en el cuerpo de la petición en formato JSON.
    parameters:
      - in: body
        name: body
        required: true
        description: Datos del receso a registrar.
        schema:
          type: object
          required:
            - id_t
            - hora_inicio
            - hora_fin
            - total
            - nombre
            - descripcion
            - tipo
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
        description: Receso creado correctamente.
        examples:
          application/json:
            id: 20
            id_t: 1
            hora_inicio: "08:00:00"
            hora_fin: "09:00:00"
            hora_total: "01:00:00"
            nombre: "ALMUERZO"
            descripcion: "Receso principal"
            tipo: "NORMAL"
      400:
        description: Datos inválidos enviados en el cuerpo de la petición.
        examples:
          application/json:
            error: "Datos invalidos"
            detail:
              - loc: ["id_t"]
                msg: "field required"
                type: "value_error.missing"
      500:
        description: Error interno del servidor.
        examples:
          application/json:
            error: "Error interno"
            detail: "Error de conexión con la base de datos"
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
    summary: Actualizar un receso existente
    description: Endpoint para actualizar un receso existente. El identificador
      del receso se envía en la URL y los nuevos datos se envían en el cuerpo
      de la petición.
    parameters:
      - name: receso_id
        in: path
        type: integer
        required: true
        description: Identificador del receso a actualizar.
      - in: body
        name: body
        required: true
        description: Nuevos datos del receso.
    responses:
      200:
        description: Receso actualizado correctamente.
        examples:
          application/json:
            id: 17
            id_t: 8
            hora_inicio: "08:30:00"
            hora_fin: "08:45:00"
            hora_total: "00:15:00"
            nombre: "ALMUERZO"
            descripcion: "Receso actualizado"
            tipo: "NORMAL"
      404:
        description: Receso no encontrado.
        examples:
          application/json:
            error: "Receso no encontrado"
      400:
        description: Datos inválidos enviados en el cuerpo de la petición.
        examples:
          application/json:
            error: "Datos invalidos"
            detail:
              - loc: ["nombre"]
                msg: "field required"
                type: "value_error.missing"
      500:
        description: Error interno del servidor.
        examples:
          application/json:
            error: "Error interno"
            detail: "Error inesperado al actualizar el receso"
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
