from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import hashlib
import filetype
import traceback
from database.db import insert_actividad, insert_contacto, insert_tema, insert_foto, get_all_regiones, get_comunas_by_region, get_last_actividades
from utils.validations import validate_activity_form

app = Flask(__name__)
app.secret_key = "actividad_secreta"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---- API para selects dinámicos ----

@app.route('/api/regiones')
def api_regiones():
    regiones = get_all_regiones()
    return jsonify(regiones)

@app.route('/api/comunas/<int:region_id>')
def api_comunas(region_id):
    comunas = get_comunas_by_region(region_id)
    return jsonify(comunas)

# ---- Páginas web ----

@app.route('/')
def index():
    actividades = get_last_actividades(5)
    return render_template('index.html', actividades=actividades)

@app.route('/agregar_actividad', methods=['GET', 'POST'])
def agregar_actividad():
    if request.method == 'POST':
        try:
            form_data = request.form
            files = request.files
            if not validate_activity_form(form_data, files):
                flash("Hay errores en el formulario.")
                return redirect(request.url)

            comuna = form_data.get('comuna')
            sector = form_data.get('sector')
            nombre = form_data.get('organizador_nombre')
            email = form_data.get('organizador_email')
            telefono = form_data.get('organizador_telefono')

            red_social = form_data.get('contactar_por')
            identificador = form_data.get('otro_contacto') if red_social == "otra" else red_social

            inicio = form_data.get('inicio')
            termino = form_data.get('termino')
            descripcion = form_data.get('descripcion')

            tema = form_data.get('tema')
            glosa_otro = form_data.get('otro_tema') if tema == 'otro' else None

            fotos_files = files.getlist("fotos[]")
            filenames = []

            for f in fotos_files:
                if f and f.filename:
                    kind = filetype.guess(f)
                    if not kind:
                        flash(f"El archivo {f.filename} no es válido.")
                        return redirect(request.url)
                    hash_name = hashlib.sha256(secure_filename(f.filename).encode("utf-8")).hexdigest()
                    extension = kind.extension
                    final_filename = f"{hash_name}.{extension}"
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], final_filename))
                    filenames.append(final_filename)

            actividad_id = insert_actividad(comuna, sector, nombre, email, telefono, inicio, termino, descripcion)
            insert_contacto(red_social, identificador, actividad_id)
            insert_tema(tema, glosa_otro, actividad_id)
            for archivo in filenames:
                insert_foto(f"static/uploads/{archivo}", archivo, actividad_id)

            flash("Actividad registrada exitosamente.")
            return redirect(url_for('index'))

        except Exception as e:
            traceback.print_exc()
            flash(f"Ocurrió un error: {e}")
            return redirect(request.url)

    return render_template('agregar_actividad.html')

@app.route('/lista_actividades')
def lista_actividades():
    actividades = get_last_actividades(5)
    return render_template('lista_actividades.html', actividades=actividades)

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

if __name__ == '__main__':
    app.run(debug=True)
