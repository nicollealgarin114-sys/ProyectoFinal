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

def next_id(lista: List[dict], id_key: str) -> int
