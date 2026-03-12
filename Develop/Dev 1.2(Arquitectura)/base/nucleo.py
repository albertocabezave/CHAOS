import json
import time
import os
from .reptiliano import Reptiliano # Importamos al guardaespaldas

class Nucleo:
    def __init__(self, ruta_industria):
        self.ruta_adn = os.path.join(ruta_industria, "parametros.json")
        self.adn = self.cargar_adn()

        # Gestamos al Reptiliano dentro del Núcleo
        self.reptil = Reptiliano(self.adn)
        self.esta_vivo = True

    def cargar_adn(self):
         with open(self.ruta_adn, 'r') as f:
            return json.load(f)

    def latir(self):
        print(f"--- SISTEMA {self.adn['identidad']['especifico'].upper()} ACTIVO ---")

        while self.esta_vivo:
            # 1. Captura(Nervio)
            lectura_fisica = 25.0 # Imagina que esto sube a 43.0 para probar

            # 2. El Reptiliano hace su magia
            dato_etiquetado = self.reptil.talamo_etiquetar(lectura_fisica, "SENSOR_APHA")
            estado = self.reptil.hipotalamo_vigilar(dato_etiquetado)

            if estado == "MODO_SHOCK":
                self.ejecutar_protoclo_choque()
                break

            print(f"[OK] {dato_etiquetado['etiqueta']}: {dato_etiquetado['valor']}°C")
            time.sleep(1)

    def ejecutar_protoclo_choque(self):
        protocolo = self.adn['reptiliano_seguridad']['protocolo_choque']
        print(f"!!! LOBOTOMÍA DIGITAL !!! Ejecutando: {protocolo}")
        self.esta_vivo = False

    # Inicio
    if __name__ == "__main__":
        # Puedo probarcambiando la ruta a la de hidrocarburos si ya creaste ese ADN
        instancia = Nucleo("industria/avicola/gallinas_ponedoras")
        instancia.latir()