from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import hashlib
import filetype
import traceback
from datetime import datetime

from database.db import (
    insert_actividad, insert_contacto, insert_tema, insert_foto,
    get_all_regiones, get_comunas_by_region, get_last_actividades,
    get_estadisticas, get_conn, insert_comentario, get_comentarios_by_actividad,
    get_actividades_con_promedio, insert_nota
)
from utils.validations import validate_activity_form

app = Flask(__name__)
app.secret_key = "actividad_secreta"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    actividades = get_last_actividades(5)
    return render_template('index.html', actividades=actividades)

@app.route('/agregar_actividad', methods=['GET', 'POST'])
def agregar_actividad():
    # Aquí va tu código ya existente...
    pass  # (No te repito todo por espacio, usa tu código original aquí)

@app.route('/lista_actividades')
def lista_actividades():
    actividades = get_last_actividades(5)
    return render_template('lista_actividades.html', actividades=actividades)

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/api/estadisticas')
def api_estadisticas():
    try:
        datos = get_estadisticas()
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/actividad/<int:actividad_id>/comentarios', methods=['GET'])
def obtener_comentarios(actividad_id):
    comentarios = get_comentarios_by_actividad(actividad_id)
    return jsonify(comentarios)

@app.route('/actividad/<int:actividad_id>/comentarios', methods=['POST'])
def agregar_comentario(actividad_id):
    data = request.get_json()
    nombre = data.get("nombre", "").strip()
    texto = data.get("texto", "").strip()
    errores = []

    if not nombre or len(nombre) < 3 or len(nombre) > 80:
        errores.append("Nombre entre 3 y 80 caracteres.")
    if not texto or len(texto) < 5:
        errores.append("Texto mínimo 5 caracteres.")

    if errores:
        return jsonify({"errores": errores}), 400

    insert_comentario(nombre, texto, actividad_id)
    return jsonify({"mensaje": "Comentario agregado correctamente."})

@app.route('/actividades_realizadas')
def actividades_realizadas():
    actividades = get_actividades_con_promedio()
    return render_template('actividades_realizadas.html', actividades=actividades)

@app.route('/api/actividad/<int:actividad_id>/notas', methods=['POST'])
def guardar_nota(actividad_id):
    data = request.get_json()
    nota = data.get('nota')

    try:
        nota = int(nota)
        if nota < 1 or nota > 7:
            return jsonify({"error": "La nota debe estar entre 1 y 7."}), 400
    except:
        return jsonify({"error": "Nota inválida."}), 400

    insert_nota(actividad_id, nota)
    return jsonify({"mensaje": "Nota guardada correctamente."})

if __name__ == '__main__':
    app.run(debug=True)


