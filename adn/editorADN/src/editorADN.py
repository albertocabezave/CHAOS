#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Editor de ADN para el sistema CHAOS v1.5.
Compatible con el schema maestro definitivo (schema_maestro.json).
Permite crear, editar y validar archivos de configuración de especies.
"""

import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from jsonschema import Draft7Validator, ValidationError

# ----------------------------------------------------------------------
# Configuración de rutas: buscamos schema_maestro.json dos carpetas arriba
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_SCHEMA = os.path.join(BASE_DIR, "../../schema_maestro.json")

try:
    with open(RUTA_SCHEMA, "r", encoding="utf-8") as f:
        SCHEMA = json.load(f)
    VALIDADOR = Draft7Validator(SCHEMA)
except FileNotFoundError:
    # Mostrar error y salir
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Error Crítico",
        f"No se encontró el schema maestro en:\n{RUTA_SCHEMA}\n\n"
        "El editor no puede continuar. Asegúrate de que el archivo existe."
    )
    root.destroy()
    sys.exit(1)
except json.JSONDecodeError as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(
        "Error Crítico",
        f"El archivo schema_maestro.json no es JSON válido:\n{e}"
    )
    root.destroy()
    sys.exit(1)


def validar_adn(adn):
    """
    Valida un diccionario ADN contra el schema maestro.
    Lanza una excepción ValueError si hay errores.
    """
    errores = list(VALIDADOR.iter_errors(adn))
    if errores:
        mensajes = []
        for error in errores:
            ruta = " -> ".join(str(p) for p in error.path) if error.path else "raíz"
            mensajes.append(f"[{ruta}] {error.message}")
        raise ValueError("\n".join(mensajes))


def convertir_tipo(valor):
    """
    Intenta convertir un string a número o booleano según su forma.
    Si es 'true' o 'false' (insensible) devuelve bool.
    Si se puede convertir a int (sin decimales) devuelve int.
    Si se puede convertir a float devuelve float.
    Si no, devuelve el string original.
    """
    v = valor.strip()
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    # Probar entero
    try:
        return int(v)
    except ValueError:
        pass
    # Probar float
    try:
        return float(v)
    except ValueError:
        pass
    # Si no, string
    return v


class EditorADN:
    """
    Ventana principal del editor de ADN.
    Organiza la edición en pestañas.
    """

    def __init__(self, root):
        self.root = root
        root.title("Editor de ADN CHAOS v1.5")
        root.geometry("480x330")
        root.minsize(480, 330)

        # ---- Estado interno (ADN en construcción) ----
        self.adn = {
            "schema_version": "1.5",
            "especie": {},
            "sensores": {},
            "actuadores": {},
            "reflejos": [],
            "ciclos": {
                "reptil": {"frecuencia_hz": 100, "prioridad_hilo": "maxima"},
                "cognitivo": {
                    "frecuencia_hz": 1.0,
                    "factor_decaimiento_activacion": 0.7,
                    "factor_decaimiento_valencia": 0.7,
                    "umbral_activacion_por_error": 1.0,
                    "peso_motivacion": 1.0,
                    "factor_prediccion": 0.2,
                    "prioridad_hilo": "normal"
                }
            },
            "metadata": {"autor": "", "fecha_creacion": "", "version": "", "comentarios": ""},
            "debug": {"nivel_log": "info", "modo_operacion": "normal", "traza_eventos": False},
            "logs": {"nivel_detalle": "importante", "formato_timestamp": "unix", "retencion_dias": 30}
        }

        # ---- Variables para los campos ----
        self.especie_vars = {}
        self.metadata_vars = {}
        self.debug_vars = {}
        self.logs_vars = {}
        self.ciclos_vars = {}
        self.sensor_listbox = None
        self.act_listbox = None
        self.ref_listbox = None

        # ---- Crear un frame superior que contendrá el notebook con scroll ----
        top_frame = ttk.Frame(root)
        top_frame.pack(side="top", fill="both", expand=True)

        # Canvas dentro del top_frame (solo para el notebook)
        self.canvas = tk.Canvas(top_frame, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interior que contendrá el notebook
        self.inner_frame = ttk.Frame(self.canvas)
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Ajustar ancho del frame interior al canvas
        def configurar_ancho(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", configurar_ancho)

        # ---- Notebook (dentro del inner_frame) ----
        self.notebook = ttk.Notebook(self.inner_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # ---- Crear las pestañas ----
        self.frame_especie = ttk.Frame(self.notebook)
        self.frame_sensores = ttk.Frame(self.notebook)
        self.frame_actuadores = ttk.Frame(self.notebook)
        self.frame_reflejos = ttk.Frame(self.notebook)
        self.frame_ciclos = ttk.Frame(self.notebook)
        self.frame_avanzado = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_especie, text="Especie")
        self.notebook.add(self.frame_sensores, text="Sensores")
        self.notebook.add(self.frame_actuadores, text="Actuadores")
        self.notebook.add(self.frame_reflejos, text="Reflejos")
        self.notebook.add(self.frame_ciclos, text="Ciclos")
        self.notebook.add(self.frame_avanzado, text="Avanzado")

        # ---- Construir pestañas (llamadas a métodos) ----
        self._construir_especie()
        self._construir_sensores()
        self._construir_actuadores()
        self._construir_reflejos()
        self._construir_ciclos()
        self._construir_avanzado()

                # ---- Frame inferior fijo (botones + barra) ----
        bottom_frame = ttk.Frame(root)
        bottom_frame.pack(side="bottom", fill="x")


        # Botones
        frame_botones = ttk.Frame(bottom_frame)
        frame_botones.pack(fill="x", pady=(5, 0))

        botones_inner = ttk.Frame(frame_botones)
        botones_inner.pack(expand=True)

        ttk.Button(botones_inner, text="Abrir ADN", command=self.abrir_adn).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_inner, text="Guardar ADN", command=self.guardar_adn).pack(side=tk.LEFT, padx=5)
        ttk.Button(botones_inner, text="Validar ADN", command=self.validar_adn_actual).pack(side=tk.LEFT, padx=5)

        # Barra de estado
        self.status_bar = ttk.Label(bottom_frame, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill="x", pady=(2, 0))

        # ---- Scroll con rueda (opcional) ----
        def on_mousewheel(event):
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        # ---- Vincular actualización de estado ----
        self.notebook.bind("<<NotebookTabChanged>>", self._actualizar_estado)

    # ------------------------------------------------------------------
    # Métodos auxiliares
    # ------------------------------------------------------------------
    def _actualizar_estado(self, event=None):
        """Actualiza la barra de estado con información resumida del ADN."""
        num_sensores = len(self.adn["sensores"])
        num_actuadores = len(self.adn["actuadores"])
        num_reflejos = len(self.adn["reflejos"])
        nombre_especie = self.adn["especie"].get("nombre", "Sin nombre")
        self.status_bar.config(
            text=f"Especie: {nombre_especie} | "
                 f"Sensores: {num_sensores} | Actuadores: {num_actuadores} | Reflejos: {num_reflejos}"
        )

    def _crear_ventana_campos(self, titulo, campos, tipos=None, valores_iniciales=None,
                              combos=None, callback_guardar=None):
        """
        Crea una ventana emergente con campos de entrada.
        - titulo: título de la ventana.
        - campos: lista de nombres de campo (claves).
        - tipos: dict opcional con el tipo esperado para algunos campos (por ahora solo usado en validación).
        - valores_iniciales: dict opcional con valores por defecto.
        - combos: dict opcional con lista de opciones para Combobox (nombre_campo: lista_opciones).
        - callback_guardar: función que se llamará al guardar, recibe el dict de valores (strings).
        """
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.transient(self.root)
        win.grab_set()

        vars_campos = {}
        row = 0

        for campo in campos:
            # Etiqueta
            ttk.Label(win, text=campo.replace("_", " ").capitalize()).grid(
                row=row, column=0, sticky="w", padx=5, pady=2
            )

            var = tk.StringVar()
            if valores_iniciales and campo in valores_iniciales:
                var.set(str(valores_iniciales[campo]))

            # Si es Combobox
            if combos and campo in combos:
                widget = ttk.Combobox(win, textvariable=var, values=combos[campo], state="readonly")
                if combos[campo] and not var.get():
                    var.set(combos[campo][0])
            else:
                widget = ttk.Entry(win, textvariable=var, width=40)

            widget.grid(row=row, column=1, padx=5, pady=2)
            vars_campos[campo] = var
            row += 1

        def guardar():
            # Recoger valores
            valores = {campo: var.get().strip() for campo, var in vars_campos.items()}

            # Validar campos obligatorios (ninguno vacío)
            for campo, valor in valores.items():
                if not valor:
                    messagebox.showerror("Error", f"El campo '{campo}' es obligatorio.")
                    return

            # Validaciones de tipo básicas si se especificaron
            if tipos:
                for campo, tipo in tipos.items():
                    if campo in valores:
                        try:
                            if tipo == "float":
                                float(valores[campo])
                            elif tipo == "int":
                                int(valores[campo])
                        except ValueError:
                            messagebox.showerror("Error", f"El campo '{campo}' debe ser un número ({tipo}).")
                            return

            if callback_guardar:
                callback_guardar(valores)

            win.destroy()

        ttk.Button(win, text="Guardar", command=guardar).grid(row=row, column=0, columnspan=2, pady=10)

    # ------------------------------------------------------------------
    # Pestaña Especie
    # ------------------------------------------------------------------
    def _construir_especie(self):
        campos = ["nombre", "industria", "tipo", "descripcion"]
        for i, campo in enumerate(campos):
            ttk.Label(self.frame_especie, text=campo.capitalize()).grid(
                row=i, column=0, sticky="w", padx=5, pady=5
            )
            var = tk.StringVar()
            ttk.Entry(self.frame_especie, textvariable=var, width=50).grid(
                row=i, column=1, padx=5, pady=5
            )
            self.especie_vars[campo] = var

        # Valores por defecto de ejemplo
        self.especie_vars["nombre"].set("Galpón de Codornices Lote A")
        self.especie_vars["industria"].set("Avicultura")
        self.especie_vars["tipo"].set("Galpón de Cría")
        self.especie_vars["descripcion"].set("Sistema de control para galpón de codornices.")

    # ------------------------------------------------------------------
    # Pestaña Sensores
    # ------------------------------------------------------------------
    def _construir_sensores(self):
        # Lista de sensores
        self.sensor_listbox = tk.Listbox(self.frame_sensores, width=50)
        self.sensor_listbox.grid(row=0, column=0, rowspan=5, padx=5, pady=5, sticky="nsew")

        scroll_sensores = ttk.Scrollbar(self.frame_sensores, orient="vertical", command=self.sensor_listbox.yview)
        scroll_sensores.grid(row=0, column=1, rowspan=5, sticky="ns")
        self.sensor_listbox.config(yscrollcommand=scroll_sensores.set)

        ttk.Button(self.frame_sensores, text="Agregar Sensor", command=self._agregar_sensor).grid(
            row=0, column=2, padx=5, pady=5
        )
        ttk.Button(self.frame_sensores, text="Editar Sensor", command=self._editar_sensor).grid(
            row=1, column=2, padx=5, pady=5
        )
        ttk.Button(self.frame_sensores, text="Eliminar Sensor", command=self._eliminar_sensor).grid(
            row=2, column=2, padx=5, pady=5
        )

    def _agregar_sensor(self, valores_iniciales=None):
        """
        Ventana para agregar/editar sensor.
        """
        campos = [
            "nombre", "tipo", "unidad",
            "rango_operativo_min", "rango_operativo_max",
            "rango_optimo_min", "rango_optimo_max",
            "umbral_estres_min", "umbral_estres_max",
            "critico", "peso_atencion",
            "ubicacion", "descripcion"
        ]
        tipos_numericos = {
            "rango_operativo_min": "float",
            "rango_operativo_max": "float",
            "rango_optimo_min": "float",
            "rango_optimo_max": "float",
            "umbral_estres_min": "float",
            "umbral_estres_max": "float",
            "peso_atencion": "float"
        }
        combos = {
            "critico": ["true", "false"]
        }

        def guardar_sensor(valores):
            # Validar rangos (min <= max)
            try:
                r_op_min = float(valores["rango_operativo_min"])
                r_op_max = float(valores["rango_operativo_max"])
                if r_op_min > r_op_max:
                    messagebox.showerror("Error", "Rango operativo: el mínimo debe ser <= máximo.")
                    return
                r_opt_min = float(valores["rango_optimo_min"])
                r_opt_max = float(valores["rango_optimo_max"])
                if r_opt_min > r_opt_max:
                    messagebox.showerror("Error", "Rango óptimo: el mínimo debe ser <= máximo.")
                    return
                u_est_min = float(valores["umbral_estres_min"])
                u_est_max = float(valores["umbral_estres_max"])
                if u_est_min > u_est_max:
                    messagebox.showerror("Error", "Umbral de estrés: el mínimo debe ser <= máximo.")
                    return
            except ValueError as e:
                messagebox.showerror("Error", f"Error en valores numéricos: {e}")
                return

            # Validar nombre (solo letras, números, _)
            nombre = valores["nombre"]
            if not nombre.replace("_", "").isalnum():
                messagebox.showerror("Error", "El nombre del sensor solo puede contener letras, números y guion bajo.")
                return

            # Evitar duplicados (si no es el mismo nombre en edición)
            if nombre in self.adn["sensores"] and (not valores_iniciales or valores_iniciales["nombre"] != nombre):
                messagebox.showerror("Error", f"Ya existe un sensor con el nombre '{nombre}'.")
                return

            # Convertir critico a booleano
            critico_val = valores["critico"].lower().strip()
            critico_bool = critico_val in ["true", "verdadero", "si", "1", "yes"]

            # Construir objeto sensor
            sensor = {
                "tipo": valores["tipo"],
                "unidad": valores["unidad"],
                "rango_operativo": [r_op_min, r_op_max],
                "rango_optimo": [r_opt_min, r_opt_max],
                "umbral_estres": [u_est_min, u_est_max],
                "critico": critico_bool,
                "peso_atencion": float(valores["peso_atencion"])
            }
            # Opcionales
            if valores.get("ubicacion"):
                sensor["ubicacion"] = valores["ubicacion"]
            if valores.get("descripcion"):
                sensor["descripcion"] = valores["descripcion"]

            # Si es edición y cambió el nombre, eliminar el anterior
            if valores_iniciales and valores_iniciales["nombre"] != nombre:
                del self.adn["sensores"][valores_iniciales["nombre"]]

            self.adn["sensores"][nombre] = sensor
            self._actualizar_lista_sensores()

        self._crear_ventana_campos(
            titulo="Agregar/Editar Sensor",
            campos=campos,
            tipos=tipos_numericos,
            valores_iniciales=valores_iniciales,
            combos=combos,
            callback_guardar=guardar_sensor
        )

    def _editar_sensor(self):
        seleccion = self.sensor_listbox.curselection()
        if not seleccion:
            messagebox.showinfo("Editar", "Selecciona un sensor de la lista.")
            return
        nombre = self.sensor_listbox.get(seleccion[0])
        sensor = self.adn["sensores"][nombre]

        # Preparar valores iniciales para el formulario
        valores = {
            "nombre": nombre,
            "tipo": sensor.get("tipo", ""),
            "unidad": sensor.get("unidad", ""),
            "rango_operativo_min": str(sensor["rango_operativo"][0]),
            "rango_operativo_max": str(sensor["rango_operativo"][1]),
            "rango_optimo_min": str(sensor["rango_optimo"][0]),
            "rango_optimo_max": str(sensor["rango_optimo"][1]),
            "umbral_estres_min": str(sensor["umbral_estres"][0]),
            "umbral_estres_max": str(sensor["umbral_estres"][1]),
            "critico": "true" if sensor.get("critico", False) else "false",
            "peso_atencion": str(sensor.get("peso_atencion", 0.5)),
            "ubicacion": sensor.get("ubicacion", ""),
            "descripcion": sensor.get("descripcion", "")
        }
        self._agregar_sensor(valores_iniciales=valores)

    def _eliminar_sensor(self):
        seleccion = self.sensor_listbox.curselection()
        if not seleccion:
            return
        nombre = self.sensor_listbox.get(seleccion[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar sensor '{nombre}'?"):
            del self.adn["sensores"][nombre]
            self._actualizar_lista_sensores()

    def _actualizar_lista_sensores(self):
        self.sensor_listbox.delete(0, tk.END)
        for nombre in sorted(self.adn["sensores"].keys()):
            self.sensor_listbox.insert(tk.END, nombre)
        self._actualizar_estado()

    # ------------------------------------------------------------------
    # Pestaña Actuadores
    # ------------------------------------------------------------------
    def _construir_actuadores(self):
        self.act_listbox = tk.Listbox(self.frame_actuadores, width=50)
        self.act_listbox.grid(row=0, column=0, rowspan=5, padx=5, pady=5, sticky="nsew")

        scroll_act = ttk.Scrollbar(self.frame_actuadores, orient="vertical", command=self.act_listbox.yview)
        scroll_act.grid(row=0, column=1, rowspan=5, sticky="ns")
        self.act_listbox.config(yscrollcommand=scroll_act.set)

        ttk.Button(self.frame_actuadores, text="Agregar Actuador", command=self._agregar_actuador).grid(
            row=0, column=2, padx=5, pady=5
        )
        ttk.Button(self.frame_actuadores, text="Editar Actuador", command=self._editar_actuador).grid(
            row=1, column=2, padx=5, pady=5
        )
        ttk.Button(self.frame_actuadores, text="Eliminar Actuador", command=self._eliminar_actuador).grid(
            row=2, column=2, padx=5, pady=5
        )

    def _agregar_actuador(self, valores_iniciales=None):
        campos = ["nombre", "tipo", "estado_inicial", "valores_posibles", "ubicacion", "descripcion", "potencia", "tiempo_respuesta"]
        tipos_numericos = {"potencia": "float", "tiempo_respuesta": "float"}

        def guardar_actuador(valores):
            # Validar nombre
            nombre = valores["nombre"]
            if not nombre.replace("_", "").isalnum():
                messagebox.showerror("Error", "El nombre del actuador solo puede contener letras, números y guion bajo.")
                return
            if nombre in self.adn["actuadores"] and (not valores_iniciales or valores_iniciales["nombre"] != nombre):
                messagebox.showerror("Error", f"Ya existe un actuador con el nombre '{nombre}'.")
                return

            # Procesar valores_posibles (separados por comas)
            valores_posibles = [v.strip() for v in valores["valores_posibles"].split(",") if v.strip()]
            if not valores_posibles:
                messagebox.showerror("Error", "Debes especificar al menos un valor posible.")
                return

            # estado_inicial debe estar en valores_posibles (aplicando conversión de tipo)
            estado_inicial_str = valores["estado_inicial"].strip()
            # Convertir estado_inicial al tipo correspondiente para comparar
            estado_inicial_conv = convertir_tipo(estado_inicial_str)
            # Convertir cada valor posible a su tipo correspondiente para comparar
            valores_posibles_conv = [convertir_tipo(v) for v in valores_posibles]
            if estado_inicial_conv not in valores_posibles_conv:
                messagebox.showerror("Error",
                                     f"El estado inicial '{estado_inicial_str}' debe estar en valores_posibles {valores_posibles}")
                return

            # Construir objeto actuador
            actuador = {
                "tipo": valores["tipo"],
                "estado_inicial": estado_inicial_conv,  # guardamos con tipo real
                "valores_posibles": valores_posibles_conv  # guardamos con tipos reales
            }
            # Opcionales
            if valores.get("ubicacion"):
                actuador["ubicacion"] = valores["ubicacion"]
            if valores.get("descripcion"):
                actuador["descripcion"] = valores["descripcion"]
            if valores.get("potencia"):
                try:
                    actuador["potencia"] = float(valores["potencia"])
                except ValueError:
                    pass
            if valores.get("tiempo_respuesta"):
                try:
                    actuador["tiempo_respuesta"] = float(valores["tiempo_respuesta"])
                except ValueError:
                    pass

            if valores_iniciales and valores_iniciales["nombre"] != nombre:
                del self.adn["actuadores"][valores_iniciales["nombre"]]

            self.adn["actuadores"][nombre] = actuador
            self._actualizar_lista_actuadores()

        self._crear_ventana_campos(
            titulo="Agregar/Editar Actuador",
            campos=campos,
            tipos=tipos_numericos,
            valores_iniciales=valores_iniciales,
            callback_guardar=guardar_actuador
        )

    def _editar_actuador(self):
        seleccion = self.act_listbox.curselection()
        if not seleccion:
            messagebox.showinfo("Editar", "Selecciona un actuador de la lista.")
            return
        nombre = self.act_listbox.get(seleccion[0])
        act = self.adn["actuadores"][nombre]

        # Convertir valores_posibles a string separado por comas para edición
        valores_posibles_str = ", ".join(str(v) for v in act.get("valores_posibles", []))

        valores = {
            "nombre": nombre,
            "tipo": act.get("tipo", ""),
            "estado_inicial": str(act.get("estado_inicial", "")),
            "valores_posibles": valores_posibles_str,
            "ubicacion": act.get("ubicacion", ""),
            "descripcion": act.get("descripcion", ""),
            "potencia": str(act.get("potencia", "")),
            "tiempo_respuesta": str(act.get("tiempo_respuesta", ""))
        }
        self._agregar_actuador(valores_iniciales=valores)

    def _eliminar_actuador(self):
        seleccion = self.act_listbox.curselection()
        if not seleccion:
            return
        nombre = self.act_listbox.get(seleccion[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar actuador '{nombre}'?"):
            del self.adn["actuadores"][nombre]
            self._actualizar_lista_actuadores()

    def _actualizar_lista_actuadores(self):
        self.act_listbox.delete(0, tk.END)
        for nombre in sorted(self.adn["actuadores"].keys()):
            self.act_listbox.insert(tk.END, nombre)
        self._actualizar_estado()

    # ------------------------------------------------------------------
    # Pestaña Reflejos
    # ------------------------------------------------------------------
    def _construir_reflejos(self):
        self.ref_listbox = tk.Listbox(self.frame_reflejos, width=50)
        self.ref_listbox.grid(row=0, column=0, rowspan=5, padx=5, pady=5, sticky="nsew")

        scroll_ref = ttk.Scrollbar(self.frame_reflejos, orient="vertical", command=self.ref_listbox.yview)
        scroll_ref.grid(row=0, column=1, rowspan=5, sticky="ns")
        self.ref_listbox.config(yscrollcommand=scroll_ref.set)

        ttk.Button(self.frame_reflejos, text="Agregar Reflejo", command=self._agregar_reflejo).grid(
            row=0, column=2, padx=5, pady=5
        )
        ttk.Button(self.frame_reflejos, text="Editar Reflejo", command=self._editar_reflejo).grid(
            row=1, column=2, padx=5, pady=5
        )
        ttk.Button(self.frame_reflejos, text="Eliminar Reflejo", command=self._eliminar_reflejo).grid(
            row=2, column=2, padx=5, pady=5
        )

    def _agregar_reflejo(self, valores_iniciales=None, indice_edicion=None):
        campos = [
            "nombre", "sensor", "operador", "umbral",
            "actuador", "accion", "histeresis", "tiempo_bloqueo", "prioridad",
            "descripcion"
        ]
        tipos_numericos = {
            "umbral": "float",
            "histeresis": "float",
            "tiempo_bloqueo": "float",
            "prioridad": "int"
        }

        # Obtener listas de sensores y actuadores para combos
        sensores_disponibles = list(self.adn["sensores"].keys())
        actuadores_disponibles = list(self.adn["actuadores"].keys())
        operadores = [">", "<", ">=", "<=", "=="]

        def guardar_reflejo(valores):
            # Validar existencia de sensor y actuador
            if valores["sensor"] not in self.adn["sensores"]:
                messagebox.showerror("Error", f"El sensor '{valores['sensor']}' no existe.")
                return
            if valores["actuador"] not in self.adn["actuadores"]:
                messagebox.showerror("Error", f"El actuador '{valores['actuador']}' no existe.")
                return

            # Convertir tipos numéricos
            try:
                umbral = float(valores["umbral"])
                histeresis = float(valores["histeresis"])
                tiempo_bloqueo = float(valores["tiempo_bloqueo"])
                prioridad = int(valores["prioridad"])
            except ValueError as e:
                messagebox.showerror("Error", f"Error en valores numéricos: {e}")
                return

            # Convertir accion al tipo adecuado (puede ser string, number, boolean)
            accion = convertir_tipo(valores["accion"])

            # Verificar que la acción esté entre los valores posibles del actuador
            actuador = self.adn["actuadores"][valores["actuador"]]
            if accion not in actuador["valores_posibles"]:
                messagebox.showerror("Error",
                                     f"La acción '{valores['accion']}' no está en los valores posibles del actuador {actuador['valores_posibles']}")
                return

            reflejo = {
                "nombre": valores["nombre"],
                "sensor": valores["sensor"],
                "operador": valores["operador"],
                "umbral": umbral,
                "actuador": valores["actuador"],
                "accion": accion,
                "histeresis": histeresis,
                "tiempo_bloqueo": tiempo_bloqueo,
                "prioridad": prioridad
            }
            if valores.get("descripcion"):
                reflejo["descripcion"] = valores["descripcion"]

            if indice_edicion is not None:
                self.adn["reflejos"][indice_edicion] = reflejo
            else:
                self.adn["reflejos"].append(reflejo)

            self._actualizar_lista_reflejos()

        combos = {
            "operador": operadores,
            "sensor": sensores_disponibles,
            "actuador": actuadores_disponibles
        }

        self._crear_ventana_campos(
            titulo="Agregar/Editar Reflejo",
            campos=campos,
            tipos=tipos_numericos,
            valores_iniciales=valores_iniciales,
            combos=combos,
            callback_guardar=guardar_reflejo
        )

    def _editar_reflejo(self):
        seleccion = self.ref_listbox.curselection()
        if not seleccion:
            messagebox.showinfo("Editar", "Selecciona un reflejo de la lista.")
            return
        idx = seleccion[0]
        reflejo = self.adn["reflejos"][idx]

        valores = {
            "nombre": reflejo.get("nombre", ""),
            "sensor": reflejo.get("sensor", ""),
            "operador": reflejo.get("operador", ""),
            "umbral": str(reflejo.get("umbral", 0)),
            "actuador": reflejo.get("actuador", ""),
            "accion": str(reflejo.get("accion", "")),
            "histeresis": str(reflejo.get("histeresis", 0)),
            "tiempo_bloqueo": str(reflejo.get("tiempo_bloqueo", 0)),
            "prioridad": str(reflejo.get("prioridad", 1)),
            "descripcion": reflejo.get("descripcion", "")
        }
        self._agregar_reflejo(valores_iniciales=valores, indice_edicion=idx)

    def _eliminar_reflejo(self):
        seleccion = self.ref_listbox.curselection()
        if not seleccion:
            return
        idx = seleccion[0]
        nombre = self.adn["reflejos"][idx].get("nombre", "Sin nombre")
        if messagebox.askyesno("Confirmar", f"¿Eliminar reflejo '{nombre}'?"):
            del self.adn["reflejos"][idx]
            self._actualizar_lista_reflejos()

    def _actualizar_lista_reflejos(self):
        self.ref_listbox.delete(0, tk.END)
        for i, ref in enumerate(self.adn["reflejos"]):
            nombre = ref.get("nombre", f"Reflejo {i+1}")
            self.ref_listbox.insert(tk.END, nombre)
        self._actualizar_estado()

    # ------------------------------------------------------------------
    # Pestaña Ciclos
    # ------------------------------------------------------------------
    def _construir_ciclos(self):
        # Variables para los campos
        self.ciclos_vars = {}

        # Marco para Ciclo Reptil
        lbl_reptil = ttk.Label(self.frame_ciclos, text="Ciclo Reptil", font=("Arial", 10, "bold"))
        lbl_reptil.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        ttk.Label(self.frame_ciclos, text="frecuencia_hz:").grid(row=1, column=0, sticky="w", padx=5)
        self.ciclos_vars["reptil_frecuencia"] = tk.StringVar(value=str(self.adn["ciclos"]["reptil"]["frecuencia_hz"]))
        ttk.Entry(self.frame_ciclos, textvariable=self.ciclos_vars["reptil_frecuencia"], width=10).grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(self.frame_ciclos, text="prioridad_hilo:").grid(row=2, column=0, sticky="w", padx=5)
        self.ciclos_vars["reptil_prioridad"] = tk.StringVar(value=self.adn["ciclos"]["reptil"]["prioridad_hilo"])
        ttk.Combobox(self.frame_ciclos, textvariable=self.ciclos_vars["reptil_prioridad"],
                     values=["maxima", "alta", "normal", "baja"], state="readonly").grid(row=2, column=1, sticky="w", padx=5)

        # Separador
        ttk.Separator(self.frame_ciclos, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        # Marco para Ciclo Cognitivo
        lbl_cog = ttk.Label(self.frame_ciclos, text="Ciclo Cognitivo", font=("Arial", 10, "bold"))
        lbl_cog.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

        campos_cog = [
            ("frecuencia_hz", "cog_frecuencia"),
            ("factor_decaimiento_activacion", "cog_fact_act"),
            ("factor_decaimiento_valencia", "cog_fact_val"),
            ("umbral_activacion_por_error", "cog_umbral"),
            ("peso_motivacion", "cog_peso"),
            ("factor_prediccion", "cog_pred"),
            ("prioridad_hilo", "cog_prioridad")
        ]
        row = 5
        for etiqueta, var_name in campos_cog:
            ttk.Label(self.frame_ciclos, text=etiqueta + ":").grid(row=row, column=0, sticky="w", padx=5)
            if "prioridad" in var_name:
                # Combobox
                self.ciclos_vars[var_name] = tk.StringVar(value=self.adn["ciclos"]["cognitivo"][etiqueta])
                ttk.Combobox(self.frame_ciclos, textvariable=self.ciclos_vars[var_name],
                             values=["maxima", "alta", "normal", "baja"], state="readonly").grid(row=row, column=1, sticky="w", padx=5)
            else:
                self.ciclos_vars[var_name] = tk.StringVar(value=str(self.adn["ciclos"]["cognitivo"][etiqueta]))
                ttk.Entry(self.frame_ciclos, textvariable=self.ciclos_vars[var_name], width=10).grid(row=row, column=1, sticky="w", padx=5)
            row += 1

    # ------------------------------------------------------------------
    # Pestaña Avanzado (metadata, debug, logs)
    # ------------------------------------------------------------------
    def _construir_avanzado(self):
        # Usamos un Notebook interno para organizar
        sub_notebook = ttk.Notebook(self.frame_avanzado)
        sub_notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Metadata
        frame_meta = ttk.Frame(sub_notebook)
        sub_notebook.add(frame_meta, text="Metadata")
        campos_meta = ["autor", "fecha_creacion", "version", "comentarios"]
        for i, campo in enumerate(campos_meta):
            ttk.Label(frame_meta, text=campo).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar(value=self.adn["metadata"].get(campo, ""))
            self.metadata_vars[campo] = var
            ttk.Entry(frame_meta, textvariable=var, width=40).grid(row=i, column=1, padx=5, pady=5)

        # Debug
        frame_debug = ttk.Frame(sub_notebook)
        sub_notebook.add(frame_debug, text="Debug")
        ttk.Label(frame_debug, text="nivel_log:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.debug_vars["nivel_log"] = tk.StringVar(value=self.adn["debug"]["nivel_log"])
        ttk.Combobox(frame_debug, textvariable=self.debug_vars["nivel_log"],
                     values=["debug", "info", "warn", "error"], state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_debug, text="modo_operacion:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.debug_vars["modo_operacion"] = tk.StringVar(value=self.adn["debug"]["modo_operacion"])
        ttk.Combobox(frame_debug, textvariable=self.debug_vars["modo_operacion"],
                     values=["normal", "test", "simulacion"], state="readonly").grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_debug, text="traza_eventos:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.debug_vars["traza_eventos"] = tk.BooleanVar(value=self.adn["debug"]["traza_eventos"])
        ttk.Checkbutton(frame_debug, variable=self.debug_vars["traza_eventos"]).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Logs
        frame_logs = ttk.Frame(sub_notebook)
        sub_notebook.add(frame_logs, text="Logs")
        ttk.Label(frame_logs, text="nivel_detalle:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.logs_vars["nivel_detalle"] = tk.StringVar(value=self.adn["logs"]["nivel_detalle"])
        ttk.Combobox(frame_logs, textvariable=self.logs_vars["nivel_detalle"],
                     values=["minimo", "importante", "completo"], state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_logs, text="formato_timestamp:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.logs_vars["formato_timestamp"] = tk.StringVar(value=self.adn["logs"]["formato_timestamp"])
        ttk.Combobox(frame_logs, textvariable=self.logs_vars["formato_timestamp"],
                     values=["unix", "iso8601"], state="readonly").grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_logs, text="retencion_dias:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.logs_vars["retencion_dias"] = tk.StringVar(value=str(self.adn["logs"]["retencion_dias"]))
        ttk.Entry(frame_logs, textvariable=self.logs_vars["retencion_dias"], width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

    # ------------------------------------------------------------------
    # Operaciones con archivos
    # ------------------------------------------------------------------
    def abrir_adn(self):
        """Carga un archivo ADN existente y actualiza la interfaz."""
        archivo = filedialog.askopenfilename(
            title="Abrir ADN",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if not archivo:
            return

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            # Validar contra el schema
            validar_adn(datos)

            # Reemplazar el ADN actual
            self.adn = datos

            # Actualizar todas las pestañas
            self._actualizar_desde_adn()

            self.status_bar.config(text=f"Cargado: {os.path.basename(archivo)}")
            messagebox.showinfo("Éxito", "ADN cargado correctamente.")

        except ValidationError as e:
            messagebox.showerror("Error de validación", f"El archivo no cumple el schema:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def guardar_adn(self):
        """Recoge los datos de la interfaz, valida y guarda en archivo."""
        # Actualizar adn con los datos de las pestañas
        self._actualizar_adn_desde_interfaz()

        # Validar
        try:
            validar_adn(self.adn)
        except ValueError as e:
            messagebox.showerror("Error de Validación", f"El ADN no es válido:\n{e}")
            return

        # Guardar
        archivo = filedialog.asksaveasfilename(
            title="Guardar ADN",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if archivo:
            try:
                with open(archivo, "w", encoding="utf-8") as f:
                    json.dump(self.adn, f, indent=2, ensure_ascii=False)
                self.status_bar.config(text=f"Guardado: {os.path.basename(archivo)}")
                messagebox.showinfo("Éxito", "ADN guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def validar_adn_actual(self):
        """Valida el ADN actual sin guardar."""
        self._actualizar_adn_desde_interfaz()
        try:
            validar_adn(self.adn)
            messagebox.showinfo("Validación", "El ADN es válido según el schema.")
        except ValueError as e:
            messagebox.showerror("Validación fallida", f"Errores encontrados:\n{e}")

    # ------------------------------------------------------------------
    # Sincronización entre interfaz y modelo de datos
    # ------------------------------------------------------------------
    def _actualizar_adn_desde_interfaz(self):
        """Vuelca los valores de las pestañas al diccionario self.adn."""

        # Especie
        self.adn["especie"] = {k: v.get() for k, v in self.especie_vars.items()}

        # Ciclos
        try:
            self.adn["ciclos"]["reptil"]["frecuencia_hz"] = float(self.ciclos_vars["reptil_frecuencia"].get())
            self.adn["ciclos"]["reptil"]["prioridad_hilo"] = self.ciclos_vars["reptil_prioridad"].get()

            self.adn["ciclos"]["cognitivo"]["frecuencia_hz"] = float(self.ciclos_vars["cog_frecuencia"].get())
            self.adn["ciclos"]["cognitivo"]["factor_decaimiento_activacion"] = float(self.ciclos_vars["cog_fact_act"].get())
            self.adn["ciclos"]["cognitivo"]["factor_decaimiento_valencia"] = float(self.ciclos_vars["cog_fact_val"].get())
            self.adn["ciclos"]["cognitivo"]["umbral_activacion_por_error"] = float(self.ciclos_vars["cog_umbral"].get())
            self.adn["ciclos"]["cognitivo"]["peso_motivacion"] = float(self.ciclos_vars["cog_peso"].get())
            self.adn["ciclos"]["cognitivo"]["factor_prediccion"] = float(self.ciclos_vars["cog_pred"].get())
            self.adn["ciclos"]["cognitivo"]["prioridad_hilo"] = self.ciclos_vars["cog_prioridad"].get()
        except ValueError as e:
            # No lanzamos excepción, solo mostramos advertencia, pero el guardado fallará en validación
            messagebox.showwarning("Advertencia", f"Error en valores numéricos de ciclos: {e}")

        # Metadata
        self.adn["metadata"] = {k: v.get() for k, v in self.metadata_vars.items()}

        # Debug
        self.adn["debug"] = {
            "nivel_log": self.debug_vars["nivel_log"].get(),
            "modo_operacion": self.debug_vars["modo_operacion"].get(),
            "traza_eventos": self.debug_vars["traza_eventos"].get()
        }

        # Logs
        try:
            retencion = int(self.logs_vars["retencion_dias"].get())
        except ValueError:
            retencion = 30  # valor por defecto
        self.adn["logs"] = {
            "nivel_detalle": self.logs_vars["nivel_detalle"].get(),
            "formato_timestamp": self.logs_vars["formato_timestamp"].get(),
            "retencion_dias": retencion
        }

        # Nota: sensores, actuadores y reflejos ya se actualizan en sus propios métodos
        # No necesitamos hacer nada aquí, porque se modifican directamente en las listas.

    def _actualizar_desde_adn(self):
        """Actualiza todos los widgets de la interfaz con los datos del ADN cargado."""

        # Especie
        for campo, var in self.especie_vars.items():
            var.set(self.adn["especie"].get(campo, ""))

        # Ciclos
        reptil = self.adn["ciclos"].get("reptil", {})
        self.ciclos_vars["reptil_frecuencia"].set(str(reptil.get("frecuencia_hz", 100)))
        self.ciclos_vars["reptil_prioridad"].set(reptil.get("prioridad_hilo", "maxima"))

        cog = self.adn["ciclos"].get("cognitivo", {})
        self.ciclos_vars["cog_frecuencia"].set(str(cog.get("frecuencia_hz", 1.0)))
        self.ciclos_vars["cog_fact_act"].set(str(cog.get("factor_decaimiento_activacion", 0.7)))
        self.ciclos_vars["cog_fact_val"].set(str(cog.get("factor_decaimiento_valencia", 0.7)))
        self.ciclos_vars["cog_umbral"].set(str(cog.get("umbral_activacion_por_error", 1.0)))
        self.ciclos_vars["cog_peso"].set(str(cog.get("peso_motivacion", 1.0)))
        self.ciclos_vars["cog_pred"].set(str(cog.get("factor_prediccion", 0.2)))
        self.ciclos_vars["cog_prioridad"].set(cog.get("prioridad_hilo", "normal"))

        # Metadata
        meta = self.adn.get("metadata", {})
        for campo, var in self.metadata_vars.items():
            var.set(meta.get(campo, ""))

        # Debug
        debug = self.adn.get("debug", {})
        self.debug_vars["nivel_log"].set(debug.get("nivel_log", "info"))
        self.debug_vars["modo_operacion"].set(debug.get("modo_operacion", "normal"))
        self.debug_vars["traza_eventos"].set(debug.get("traza_eventos", False))

        # Logs
        logs = self.adn.get("logs", {})
        self.logs_vars["nivel_detalle"].set(logs.get("nivel_detalle", "importante"))
        self.logs_vars["formato_timestamp"].set(logs.get("formato_timestamp", "unix"))
        self.logs_vars["retencion_dias"].set(str(logs.get("retencion_dias", 30)))

        # Actualizar listas
        self._actualizar_lista_sensores()
        self._actualizar_lista_actuadores()
        self._actualizar_lista_reflejos()

        self._actualizar_estado()


# ----------------------------------------------------------------------
# Punto de entrada
# ----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EditorADN(root)
    root.mainloop()