# =================================================================
# ARCHIVO: main.py
# ARQUITECTO: Alberto
# FUNCIÓN: Sistema Nervioso Central (Conecta IA y Mundo Virtual)
# =================================================================

from base.nucleo import Nucleo
from industria.avicola.gallinas_ponedoras.limbico import Limbico
from industria.avicola.gallinas_ponedoras.cortex import Cortex
from simulacion.mundo import EntornoFisico
from simulacion.sensores_virtuales import SensorVirtual
import time

def ejecutar_sistema():
    # 1. CARGA DE CONFIGURACIÓN (ADN)
    ruta_adn = "industria/avicola/gallinas_ponedoras"
    
    # 2. INICIALIZACIÓN DE LA IA
    cerebro_base = Nucleo(ruta_adn) 
    alma_limbico = Limbico(cerebro_base.adn['limbico_emocion']) 
    alma_cortex = Cortex(cerebro_base.adn['cortex_estrategia']) 
    
    # 3. INICIALIZACIÓN DEL MUNDO VIRTUAL Y SENSORES
    mundo_real = EntornoFisico(temp_inicial=28.0)
    
    # CREAMOS DOS SENSORES (Dos instancias de la misma clase)
    sensor_interno = SensorVirtual(nombre="DHT22_Nido", margen_error=0.2)
    sensor_externo = SensorVirtual(nombre="DHT22_Calle", margen_error=0.5)
    
    print(f"\n=== SISTEMA {cerebro_base.adn['identidad']['especifico'].upper()} CON DOBLE SENSOR INICIADO ===")
    
    potencia_actuadores = 0 

    try:
        while True:
            # --- FASE 1: FÍSICA REAL (Recibimos DOS valores del mundo) ---
            t_int_fisica, t_ext_fisica = mundo_real.actualizar(potencia_actuadores)
            
            # --- FASE 2: PERCEPCIÓN (Cada sensor lee su parte) ---
            lectura_int = sensor_interno.capturar(t_int_fisica)
            lectura_ext = sensor_externo.capturar(t_ext_fisica)
            
            # --- FASE 3: SIMULACIÓN INTERNA (El Córtex sueña con la interna) ---
            prediccion_interna = alma_cortex.simular_realidad(lectura_int)
            
            # --- FASE 4: VIGILANCIA (El Reptiliano cuida la interna) ---
            dato_etiquetado = cerebro_base.reptil.talamo_etiquetar(lectura_int, "NIDO_1")
            estado_vital = cerebro_base.reptil.hipotalamo_vigilar(dato_etiquetado)
            
            if estado_vital == "MODO_SHOCK":
                print("\n[!!!] REPTILIANO: CALOR CRÍTICO INTERNO")
                cerebro_base.ejecutar_protoclo_choque()
                break 
                
            nivel_estres = alma_limbico.procesar_emocion(lectura_int, prediccion_interna)
            
            # --- FASE 5: TOMA DE DECISIÓN (Ahora con visión total) ---
            # OJO: Aquí le pasamos AMBAS lecturas al Córtex
            orden_ejecutiva = alma_cortex.planificar_accion(lectura_int, lectura_ext, nivel_estres)
            
            if isinstance(orden_ejecutiva, dict):
                potencia_actuadores = list(orden_ejecutiva.values())[0]
                accion_texto = f"POTENCIA: {potencia_actuadores}%"
            else:
                accion_texto = f"ESTADO: {orden_ejecutiva}"
                potencia_actuadores = 0 
            
            # --- MONITOR DE CONTROL (Lo que ves en tu Canaima) ---
            print(f"INT: {lectura_int}°C | EXT: {lectura_ext}°C | ESTRÉS: {nivel_estres*100:.1f}%")
            print(f"DECISIÓN: {accion_texto}")
            print("-" * 65)
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Sistema detenido por el Arquitecto.")

if __name__ == "__main__":
    ejecutar_sistema()