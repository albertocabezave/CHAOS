import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class ArquitectoADN:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Especies v1.0 - Alberto Cabeza")
        self.root.geometry("480x380")
        
        self.ruta_archivo = None
        # Plantilla Maestra: Define la estructura mínima de un organismo
        self.plantilla = {
            "manual_fabricacion": {
                "identidad": "Nueva_Especie",
                "id_organismo": "ID_00",
                "hardware_soma": {
                    "actuadores": [],
                    "sensores_externos": [],
                    "sensores_internos": []
                }
            },
            "manual_funcionamiento": {
                "neurocepcion": {
                    "introspeccion": {"temp_objetivo": 20.0, "margen_confort": 1.0, "fotoperiodo_horas": 12},
                    "exterocepcion": {"fuente": "sensores_externos", "variables": []},
                    "propioceccion": {"cuerpo": "hardware_soma", "verificacion": "estado_actuadores"},
                    "nocicepcion": {"miedo_por_fiebre": 40.0, "daño_por_sobrecarga_amp": 5.0}
                },
                "pesos_procesadores": {"atencion": 0.5, "emociones": 0.5, "motivacion": 0.5}
            }
        }
        self.datos_adn = self.plantilla.copy()
        self.crear_interfaz()

    def crear_interfaz(self):
        # Barra de Herramientas
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side="top", fill="x", padx=10, pady=5)
        
        ttk.Button(toolbar, text="Nuevo ADN", command=self.nuevo_adn).pack(side="left")
        ttk.Button(toolbar, text="Cargar Existente", command=self.cargar_archivo).pack(side="left")
        ttk.Button(toolbar, text="Guardar Cambios", command=self.guardar_archivo).pack(side="left")
        ttk.Button(toolbar, text="Guardar Como...", command=self.guardar_como).pack(side="left")

        # Área de edición con scroll
        self.canvas = tk.Canvas(self.root)
        scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.frame_edit = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.frame_edit, anchor="nw")
        self.canvas.configure(yscrollcommand=scroll_y.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        
        self.frame_edit.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def nuevo_adn(self):
        """Reinicia la interfaz con la estructura de la plantilla"""
        self.ruta_archivo = None
        self.datos_adn = json.loads(json.dumps(self.plantilla)) # Copia profunda
        self.refrescar_ui()

    def cargar_archivo(self):
        self.ruta_archivo = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if self.ruta_archivo:
            with open(self.ruta_archivo, 'r') as f:
                self.datos_adn = json.load(f)
            self.refrescar_ui()

    def refrescar_ui(self):
        for w in self.frame_edit.winfo_children(): w.destroy()
        
        # --- Identidad ---
        self.ent_id = self.crear_seccion_texto("IDENTIDAD DEL ORGANISMO", 
                     self.datos_adn["manual_fabricacion"]["identidad"])

        # --- Pesos (Sliders) ---
        ttk.Label(self.frame_edit, text="PESOS PROCESADORES", font=('Arial', 10, 'bold')).pack(pady=5)
        self.sliders = {}
        for k, v in self.datos_adn["manual_funcionamiento"]["pesos_procesadores"].items():
            f = ttk.Frame(self.frame_edit); f.pack(fill="x", padx=20)
            ttk.Label(f, text=k).pack(side="left")
            s = ttk.Scale(f, from_=0.0, to=1.0); s.set(v); s.pack(side="right", fill="x", expand=True)
            self.sliders[k] = s

        # --- Hardware (Actuadores y Sensores) ---
        self.txt_act = self.crear_seccion_area("ACTUADORES (Separados por coma)", 
                     ", ".join(self.datos_adn["manual_fabricacion"]["hardware_soma"]["actuadores"]))
        
        # --- Nocicepción ---
        ttk.Label(self.frame_edit, text="UMBRALES NOCICEPCIÓN", font=('Arial', 10, 'bold')).pack(pady=5)
        self.ent_noci = {}
        noci = self.datos_adn["manual_funcionamiento"]["neurocepcion"]["nocicepcion"]
        for k, v in noci.items():
            f = ttk.Frame(self.frame_edit); f.pack(fill="x", padx=20)
            ttk.Label(f, text=k).pack(side="left")
            e = ttk.Entry(f); e.insert(0, str(v)); e.pack(side="right")
            self.ent_noci[k] = e

    def crear_seccion_texto(self, titulo, valor):
        ttk.Label(self.frame_edit, text=titulo, font=('Arial', 10, 'bold')).pack(pady=5)
        e = ttk.Entry(self.frame_edit); e.insert(0, valor); e.pack(fill="x", padx=20)
        return e

    def crear_seccion_area(self, titulo, valor):
        ttk.Label(self.frame_edit, text=titulo, font=('Arial', 10, 'bold')).pack(pady=5)
        t = tk.Text(self.frame_edit, height=3, width=50); t.insert("1.0", valor); t.pack(padx=20)
        return t

    def recolectar_datos(self):
        """Extrae los datos de la UI y los vuelca al diccionario datos_adn"""
        self.datos_adn["manual_fabricacion"]["identidad"] = self.ent_id.get()
        # Actualizar Sliders
        for k, s in self.sliders.items():
            self.datos_adn["manual_funcionamiento"]["pesos_procesadores"][k] = round(s.get(), 2)
        # Actualizar Actuadores
        act_raw = self.txt_act.get("1.0", "end-1c")
        self.datos_adn["manual_fabricacion"]["hardware_soma"]["actuadores"] = [a.strip() for a in act_raw.split(",") if a.strip()]
        # Actualizar Nocicepción
        for k, e in self.ent_noci.items():
            self.datos_adn["manual_funcionamiento"]["neurocepcion"]["nocicepcion"][k] = float(e.get())

    def guardar_archivo(self):
        if not self.ruta_archivo: return self.guardar_como()
        self.recolectar_datos()
        with open(self.ruta_archivo, 'w') as f:
            json.dump(self.datos_adn, f, indent=4)
        messagebox.showinfo("OK", "Archivo guardado.")

    def guardar_como(self):
        self.ruta_archivo = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if self.ruta_archivo: self.guardar_archivo()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArquitectoADN(root)
    root.mainloop()