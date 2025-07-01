import pymysql
import json

DB_NAME = "tarea2"
DB_USERNAME = "root"
DB_PASSWORD = "haiti"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

with open("database/querys.json", "r", encoding="utf-8") as query_file:
    QUERY_DICT = json.load(query_file)

def get_conn():
    return pymysql.connect(
        db=DB_NAME,
        user=DB_USERNAME,
        passwd=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        charset=DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor
    )

def insert_actividad(comuna_id, sector, nombre, email, celular, inicio, termino, descripcion):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["insert_actividad"],
                           (comuna_id, sector, nombre, email, celular, inicio, termino, descripcion))
            actividad_id = cursor.lastrowid
        conn.commit()
        return actividad_id

def insert_contacto(nombre, identificador, actividad_id):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["insert_contacto"], (nombre, identificador, actividad_id))
        conn.commit()

def insert_tema(tema, glosa_otro, actividad_id):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["insert_tema"], (tema, glosa_otro, actividad_id))
        conn.commit()

def insert_foto(ruta_archivo, nombre_archivo, actividad_id):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["insert_foto"], (ruta_archivo, nombre_archivo, actividad_id))
        conn.commit()

def get_all_regiones():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM region ORDER BY nombre")
            return cursor.fetchall()

def get_comunas_by_region(region_id):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre FROM comuna WHERE region_id = %s ORDER BY nombre", (region_id,))
            return cursor.fetchall()

def get_last_actividades(limit=5):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["get_last_actividades"], (limit,))
            return cursor.fetchall()

def get_estadisticas():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["estadisticas_actividades_por_dia"])
            actividades_por_dia = cursor.fetchall()

            cursor.execute(QUERY_DICT["estadisticas_actividades_por_tema"])
            actividades_por_tema = cursor.fetchall()

            cursor.execute(QUERY_DICT["estadisticas_actividades_por_mes_momento"])
            actividades_por_mes_momento = cursor.fetchall()

    return {
        "actividades_por_dia": actividades_por_dia,
        "actividades_por_tema": actividades_por_tema,
        "actividades_por_mes_momento": actividades_por_mes_momento
    }

def insert_comentario(nombre, texto, actividad_id):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["insert_comentario"], (nombre, texto, actividad_id))
        conn.commit()

def get_comentarios_by_actividad(actividad_id):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["get_comentarios_por_actividad"], (actividad_id,))
            return cursor.fetchall()

def insert_nota(actividad_id, nota):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(QUERY_DICT["insert_nota"], (actividad_id, nota))
        conn.commit()

def get_actividades_con_promedio():
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    a.id,
                    a.nombre,
                    a.descripcion,
                    a.sector,
                    a.dia_hora_inicio,
                    c.nombre AS comuna,
                    IFNULL(ROUND(AVG(n.nota),2), NULL) AS promedio
                FROM actividad a
                JOIN comuna c ON a.comuna_id = c.id
                LEFT JOIN nota n ON a.id = n.actividad_id
                GROUP BY a.id
                ORDER BY a.dia_hora_inicio DESC
            """)
            return cursor.fetchall()

