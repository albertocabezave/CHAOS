#!/usr/bin/env python3
# -*-coding:  utf-8 -*-

"""
Editor de ADN CHAOS v.15
Version Inicial: ventana con pestañas y carga del schema maestro
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------
# Constantes
# ---------------------
# Ruta al schema maestro
RUTA_SCHEMA = os.path.join(os.path.dirname(__file__), "../../schema_maestro.json")

# ---------------------------
# Clase Principal del editor
# ---------------------------
class EditorADN:
  def __init__(self, root):
    self.root = root
    self.root.title("Editor ADN CHAOS v1.5")
    self.root.geometry("480x330")

    # Cargar schema (Si falla, sale)
    self.schema = self.cargar_schema()
    if self.schema is None:
      sys.exit(1)

    # Crear el notebook (pestañas)
    self.notebook = ttk.Notebook(root) # Crear el notebook
    self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

    # Crear los frames para cada pestaña
    self.pestañas = {}
    nombres = ["Especie", "Sensores", "Actuadores", "Reflejos", "Ciclos", "Avanzado"]
    for nombre in nombres:
      frame = ttk.Frame(self.notebook)
      self.notebook.add(frame, text=nombre)
      self.pestañas[nombre] = frame

    # Por ahora ponemos una etiqueta simple en cada pestaña
    for nombre, frame in self.pestañas.items():
      ttk.Label(frame, text=f"Pestaña {nombre} - En Construcción").pack(expand=True)
    
  def cargar_schema(self):
    # Intentar cargar el schema_maestro. Si falla, mostrar error.
    try:
      with open(RUTA_SCHEMA, "r", encoding="utf-8") as f:
        schema = json.load(f)
      return schema
    except FileNotFoundError:
      messagebox.showerror(
        "Error crítico",
        f"No se encontró el schema en:\n{os.path.abspath(RUTA_SCHEMA)}\n\n"
        "El editor se cerrará."
      )
      return None
    except json.JSONDecodeError as e:
      messagebox.showerror(
        "Error crítico",
        f"El schema no es un JSON válido\n{e}"
      )
      return None

# ---------------------------
# Bloque pricipal
#----------------------------
if __name__ == "__main__":
  root = tk.Tk()
  app = EditorADN(root)
  root.mainloop()
