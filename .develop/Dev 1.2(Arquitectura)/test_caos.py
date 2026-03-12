from base.nucleo import Nucleo
from industria.avicola.gallinas_ponedoras.limbico import Limbico
from industria.avicola.gallinas_ponedoras.cortex import Cortex
import time

# 1. INICILIZAR
ruta = "industria/avicola/gallinas_ponedoras"
cuerpo = Nucleo(ruta)
alma_limbico = Limbico(cuerpo.adn['limbico_emocion'])
alma_cortex = Cortex(cuerpo.adn['cortex_estrategia'])

def ejecutar_test():
    print("\n==== INICIANDO TEST DE CAOS: LA MENTIRA DEL CÓRTEX ===\n")
    temp_fisica = 24.0 # Empezamos en perfecto estado

    for segundo in range(1,11):
        # A. El Córtex sueña (Predicción)
        sueño_virtual = alma_cortex.simular_realidad(temp_fisica)

        # B. Inyectamos el CAOS:
        # A partir del segundo 5, la realidad física sube locamente
        # pero el Córtex NO lo sabe en su simulación.
        if segundo >= 5:
            temp_fisica += 4.0
        else:
            temp_fisica = sueño_virtual

        # C. Procesamiento del Reptiliano
        dato_etiquetado = cuerpo.reptil.talamo_etiquetar(temp_fisica, "NIDO_TEST")

        # D. EL MOMENTO DE LA VERDAD: El Límbico juzga
        estres = alma_limbico.procesar_emocion(temp_fisica, sueño_virtual)

        # E. El Córtex intenta actuar
        orden = alma_cortex.planificar_accion(temp_fisica, estres)

        # SALIDA DE DATOS
        status = "ESTABLE" if estres < 0.5 else "¡¡¡ DESCONFIANZA !!!"
        print("--------------------------------------------------------------------------")
        print(f"SEG: {segundo} | REAL: {temp_fisica:.1f}°C | VIRTUAL: {sueño_virtual:.1f}°C")
        print(f"ESTRÉS: {estres*100:.0f}% -> {status}")
        if isinstance(orden, dict):
            print(f"ACCIÓN CÓRTEX: VENTILADORES AL {orden['ventiladores']}%")
        else:
            print(f"ACCIÓN CÓRTEX: {orden}")

        time.sleep(1)

if __name__ == "__main__":
    ejecutar_test()