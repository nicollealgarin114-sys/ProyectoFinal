import streamlit as st
import json
import os


DATA_FILE = "data.json"


# ===================== PERSISTENCIA =====================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"estudiantes": [], "cursos": [], "instructores": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ===================== INTERFAZ =====================

st.set_page_config(page_title="Sistema Académico", layout="wide")

st.title("📘 Sistema de Gestión Académica")

data = load_data()


# ===================== SIDEBAR =====================

op = st.sidebar.radio(
    "Menú",
    [
        "Estudiantes",
        "Cursos",
        "Instructores",
        "Dashboard"
    ]
)


# ===================== ESTUDIANTES =====================

if op == "Estudiantes":

    st.header("👩‍🎓 Gestión de Estudiantes")

    nombre = st.text_input("Nombre del estudiante")
    
    if st.button("Registrar"):
        if nombre == "":
            st.warning("Campo vacío")
        else:
            data["estudiantes"].append({"nombre": nombre})
            save_data(data)
            st.success("Estudiante registrado.")

    st.subheader("Listado")
    st.table(data["estudiantes"])


# ===================== CURSOS =====================

elif op == "Cursos":

    st.header("📚 Gestión de Cursos")

    curso = st.text_input("Nombre del curso")

    if st.button("Registrar curso"):
        if curso == "":
            st.warning("No puede estar vacío")
        else:
            data["cursos"].append({"nombre": curso})
            save_data(data)
            st.success("Curso guardado.")

    st.subheader("Cursos registrados")
    st.table(data["cursos"])


# ===================== INSTRUCTORES =====================

elif op == "Instructores":

    st.header("👨‍🏫 Gestión de Instructores")

    instructor = st.text_input("Nombre del instructor")

    if st.button("Registrar instructor"):
        data["instructores"].append({"nombre": instructor})
        save_data(data)
        st.success("Instructor registrado")

    st.subheader("Listado")
    st.table(data["instructores"])


# ===================== DASHBOARD =====================

elif op == "Dashboard":

    st.header("📊 Dashboard Académico")

    col1, col2, col3 = st.columns(3)

    col1.metric("Estudiantes registrados", len(data["estudiantes"]))
    col2.metric("Cursos registrados", len(data["cursos"]))
    col3.metric("Instructores registrados", len(data["instructores"]))

    st.divider()

    st.subheader("📌 Información general")
    st.json(data)
