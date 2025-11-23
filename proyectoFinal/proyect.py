import streamlit as st
import json
import os
from typing import List, Optional

# ---------- Archivos JSON ----------
CURSOS_FILE = "cursos.json"
INSTRUCTORES_FILE = "instructores.json"
ESTUDIANTES_FILE = "estudiantes.json"

# ---------- Utilidades de persistencia ----------
def load_json(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------- Helpers ----------
def find_by_id(lista: List[dict], id_key: str, id_value) -> Optional[dict]:
    for item in lista:
        if str(item.get(id_key)) == str(id_value):
            return item
    return None

def remove_by_id(lista: List[dict], id_key: str, id_value) -> bool:
    inicial = len(lista)
    lista[:] = [x for x in lista if str(x.get(id_key)) != str(id_value)]
    return len(lista) < inicial

def next_id(lista: List[dict], id_key: str) -> int:
    ids = [int(x[id_key]) for x in lista if str(x.get(id_key)).isdigit()]
    return max(ids) + 1 if ids else 1

# ---------- Cargar datos iniciales ----------
cursos = load_json(CURSOS_FILE)
instructores = load_json(INSTRUCTORES_FILE)
estudiantes = load_json(ESTUDIANTES_FILE)

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Sistema Académico", layout="wide")
st.title("📘 Sistema de Gestión Académica")

menu = st.sidebar.selectbox("Menú", ["Dashboard", "Cursos", "Instructores", "Estudiantes"])

# -------- DASHBOARD --------
if menu == "Dashboard":
    st.header("📊 Dashboard Académico")
    col1, col2, col3 = st.columns(3)
    col1.metric("Cursos", len(cursos))
    col2.metric("Instructores", len(instructores))
    col3.metric("Estudiantes", len(estudiantes))

    st.markdown("### Detalle de datos")
    with st.expander("Ver datos crudos (JSON)"):
        st.subheader("Cursos")
        st.json(cursos)
        st.subheader("Instructores")
        st.json(instructores)
        st.subheader("Estudiantes")
        st.json(estudiantes)

# -------- CURSOS --------
elif menu == "Cursos":
    st.header("📚 Gestión de Cursos")

    st.subheader("Crear curso")
    with st.form("crear_curso", clear_on_submit=True):
        nombre = st.text_input("Nombre del curso")
        creditos = st.number_input("Créditos", min_value=0.0, step=0.5, value=3.0)
        submitted = st.form_submit_button("Crear")
        if submitted:
            if not nombre.strip():
                st.warning("El nombre no puede estar vacío.")
            else:
                nuevo_id = next_id(cursos, "id")
                cursos.append({"id": nuevo_id, "nombre": nombre.strip(), "creditos": float(creditos), "instructores": []})
                save_json(CURSOS_FILE, cursos)
                st.success(f"Curso '{nombre}' creado (ID: {nuevo_id}).")

    st.subheader("Lista de cursos")
    if cursos:
        tabla = [{"ID": c["id"], "Nombre": c["nombre"], "Créditos": c.get("creditos", 0), "Instructores": ", ".join([str(i) for i in c.get("instructores", [])])} for c in cursos]
        st.table(tabla)
    else:
        st.info("No hay cursos registrados.")

    st.subheader("Editar / Eliminar curso")
    if cursos:
        ids = [str(c["id"]) + " - " + c["nombre"] for c in cursos]
        seleccion = st.selectbox("Selecciona curso", options=[""] + ids)
        if seleccion:
            sel_id = int(seleccion.split(" - ")[0])
            curso_obj = find_by_id(cursos, "id", sel_id)
            if curso_obj:
                with st.form("editar_curso"):
                    nuevo_nombre = st.text_input("Nombre", value=curso_obj["nombre"])
                    nuevos_creditos = st.number_input("Créditos", min_value=0.0, step=0.5, value=float(curso_obj.get("creditos", 0)))
                    st.write("Instructores actuales:", curso_obj.get("instructores", []))
                    assign_ids = st.text_input("Asignar instructores (IDs separados por coma) - deja vacío para no cambiar")
                    btn_edit = st.form_submit_button("Guardar cambios")
                    if btn_edit:
                        if nuevo_nombre.strip():
                            curso_obj["nombre"] = nuevo_nombre.strip()
                        curso_obj["creditos"] = float(nuevos_creditos)
                        if assign_ids.strip():
                            ids_lista = [x.strip() for x in assign_ids.split(",") if x.strip()]
                            valid_ids = []
                            for iid in ids_lista:
                                if find_by_id(instructores, "id", iid) or find_by_id(instructores, "id", int(iid)):
                                    valid_ids.append(iid)
                            curso_obj["instructores"] = valid_ids
                        save_json(CURSOS_FILE, cursos)
                        st.success("Curso actualizado.")

                if st.button("Eliminar curso"):
                    if st.confirm_button("Confirmar eliminación del curso"):
                        for est in estudiantes:
                            if "cursos" in est and str(sel_id) in [str(x) for x in est.get("cursos", [])]:
                                est["cursos"] = [x for x in est.get("cursos", []) if str(x) != str(sel_id)]
                        save_json(ESTUDIANTES_FILE, estudiantes)
                        removed = remove_by_id(cursos, "id", sel_id)
                        if removed:
                            save_json(CURSOS_FILE, cursos)
                            st.success("Curso eliminado.")
                        else:
                            st.error("No se pudo eliminar el curso.")
    else:
        st.info("No hay cursos para editar/eliminar.")

# -------- INSTRUCTORES --------
elif menu == "Instructores":
    st.header("👩‍🏫 Gestión de Instructores")

    st.subheader("Crear instructor")
    with st.form("crear_instructor", clear_on_submit=True):
        nombre = st.text_input("Nombre del instructor")
        departamento = st.text_input("Departamento")
        submitted = st.form_submit_button("Crear")
        if submitted:
            if not nombre.strip():
                st.warning("El nombre no puede estar vacío.")
            else:
                nuevo_id = next_id(instructores, "id")
                instructors_entry = {"id": nuevo_id, "nombre": nombre.strip(), "departamento": departamento.strip()}
                instructores.append(instructors_entry)
                save_json(INSTRUCTORES_FILE, instructores)
                st.success(f"Instructor '{nombre}' creado (ID: {nuevo_id}).")

    st.subheader("Lista de instructores")
    if instructores:
        tabla = [{"ID": i["id"], "Nombre": i["nombre"], "Departamento": i.get("departamento","")} for i in instructores]
        st.table(tabla)
    else:
        st.info("No hay instructores registrados.")

    st.subheader("Editar / Eliminar instructor")
    if instructores:
        ids = [str(i["id"]) + " - " + i["nombre"] for i in instructores]
        seleccion = st.selectbox("Selecciona instructor", options=[""] + ids)
        if seleccion:
            sel_id = int(seleccion.split(" - ")[0])
            inst_obj = find_by_id(instructores, "id", sel_id)
            if inst_obj:
                with st.form("editar_instructor"):
                    nuevo_nombre = st.text_input("Nombre", value=inst_obj["nombre"])
                    nuevo_depto = st.text_input("Departamento", value=inst_obj.get("departamento",""))
                    btn_edit = st.form_submit_button("Guardar cambios")
                    if btn_edit:
                        if nuevo_nombre.strip():
                            inst_obj["nombre"] = nuevo_nombre.strip()
                        inst_obj["departamento"] = nuevo_depto.strip()
                        save_json(INSTRUCTORES_FILE, instructores)
                        st.success("Instructor actualizado.")
                if st.button("Eliminar instructor"):
                    if st.confirm_button("Confirmar eliminación del instructor"):
                        for c in cursos:
                            if "instructores" in c and str(sel_id) in [str(x) for x in c.get("instructores", [])]:
                                c["instructores"] = [x for x in c.get("instructores", []) if str(x) != str(sel_id)]
                        save_json(CURSOS_FILE, cursos)
                        removed = remove_by_id(instructores, "id", sel_id)
                        if removed:
                            save_json(INSTRUCTORES_FILE, instructores)
                            st.success("Instructor eliminado.")
                        else:
                            st.error("No se pudo eliminar el instructor.")
    else:
        st.info("No hay instructores para editar/eliminar.")

# -------- ESTUDIANTES --------
elif menu == "Estudiantes":
    st.header("🧑‍🎓 Gestión de Estudiantes")

    st.subheader("Crear estudiante")
    with st.form("crear_estudiante", clear_on_submit=True):
        nombre = st.text_input("Nombre del estudiante")
        submitted = st.form_submit_button("Crear")
        if submitted:
            if not nombre.strip():
                st.warning("El nombre no puede estar vacío.")
            else:
                nuevo_id = next_id(estudiantes, "id")
                estudiantes.append({"id": nuevo_id, "nombre": nombre.strip(), "cursos": []})
                save_json(ESTUDIANTES_FILE, estudiantes)
                st.success(f"Estudiante '{nombre}' creado (ID: {nuevo_id}).")

    st.subheader("Lista de estudiantes")
    if estudiantes:
        tabla = [{"ID": e["id"], "Nombre": e["nombre"], "Cursos": ", ".join([str(x) for x in e.get("cursos", [])])} for e in estudiantes]
        st.table(tabla)
    else:
        st.info("No hay estudiantes registrados.")

    st.subheader("Editar / Inscribir / Dar de baja / Eliminar estudiante")
    if estudiantes:
        ids = [str(e["id"]) + " - " + e["nombre"] for e in estudiantes]
        seleccion = st.selectbox("Selecciona estudiante", options=[""] + ids)
        if seleccion:
            sel_id = int(seleccion.split(" - ")[0])
            est_obj = find_by_id(estudiantes, "id", sel_id)
            if est_obj:
                with st.form("editar_estudiante"):
                    nuevo_nombre = st.text_input("Nombre", value=est_obj["nombre"])
                    curso_ids_display = [str(c["id"]) + " - " + c["nombre"] for c in cursos] if cursos else []
                    curso_para_inscribir = st.selectbox("Inscribir en curso (selecciona)", options=[""] + curso_ids_display)
                    btn_save = st.form_submit_button("Guardar cambios")
                    if btn_save:
                        if nuevo_nombre.strip():
                            est_obj["nombre"] = nuevo_nombre.strip()
                        save_json(ESTUDIANTES_FILE, estudiantes)
                        st.success("Estudiante actualizado.")
                    if curso_para_inscribir:
                        curso_sel_id = int(curso_para_inscribir.split(" - ")[0])
                        if "cursos" not in est_obj:
                            est_obj["cursos"] = []
                        if curso_sel_id not in [int(x) for x in est_obj.get("cursos", [])]:
                            est_obj["cursos"].append(curso_sel_id)
                            save_json(ESTUDIANTES_FILE, estudiantes)
                            st.success("Estudiante inscrito en curso.")

                if est_obj.get("cursos"):
                    st.write("Cursos inscritos:", ", ".join([str(x) for x in est_obj.get("cursos", [])]))
                    baja_curso = st.text_input("Escribe ID de curso para dar de baja (o deja vacío)")
                    if st.button("Dar de baja"):
                        if baja_curso.strip():
                            est_obj["cursos"] = [x for x in est_obj.get("cursos", []) if str(x) != baja_curso.strip()]
                            save_json(ESTUDIANTES_FILE, estudiantes)
                            st.success("Curso retirado del estudiante.")
                        else:
                            st.warning("Escribe el ID del curso para dar de baja.")

                eliminar = st.checkbox("Confirmar eliminación")
                if st.button("Eliminar estudiante"):
                    if eliminar:
                        removed = remove_by_id(estudiantes, "id", sel_id)
                        if removed:
                            save_json(ESTUDIANTES_FILE, estudiantes)
                            st.success("Estudiante eliminado.")
                            st.experimental_rerun()
                        else:
                            st.error("No se pudo eliminar el estudiante.")
                    else:
                        st.warning("Debes marcar la casilla para confirmar.")
    else:
        st.info("No hay estudiantes para editar/eliminar.")
