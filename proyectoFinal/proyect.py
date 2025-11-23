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

    st.m
