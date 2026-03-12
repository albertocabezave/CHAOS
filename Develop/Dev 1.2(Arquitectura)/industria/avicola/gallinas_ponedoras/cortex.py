class Cortex:
    def __init__(self, adn_config):
        # El Córtex es un cascarón: su mente es el JSON
        self.objetivo = adn_config.get('temperatura_objetivo', 24.0)
        self.margen_confort = adn_config.get('margen_confort', 2.0)
        # Aquí es donde el sistema se vuelve 'tuyo'
        self.estrategia = adn_config.get('modo_operacion', 'EFICIENTE')

    def planificar_accion(self, temp_int, temp_ext, estres):
        """
        Lógica de decisión pura: Envía órdenes a los recursos disponibles.
        """
        # 1. Definimos la intensidad de la respuesta (0 a 100)
        diferencia = temp_int - self.objetivo
        intensidad = min(int(diferencia * 20), 100) if diferencia > 0 else 0

        # 2. EL MAPA DE ACCIÓN: Aquí es donde la IA decide QUÉ usar
        # Si afuera está más fresco, el RECURSO_A (Ventilación) es eficiente.
        if temp_ext < temp_int:
            return {
                "sistema_aire_externo": intensidad,
                "nebulizadores": intensidad // 2  # Solo un poco de agua
            }
        
        # Si afuera es un horno, el RECURSO_A es peligroso.
        # Usamos RECURSO_B (Circulación interna o Enfriamiento activo)
        else:
            return {
                "sistema_aire_externo": 5, # Mínimo legal para oxígeno
                "enfriamiento_interno": intensidad, # Aire acondicionado o hielo
                "nebulizadores": 100 if temp_int > 35 else 0 # ¡Emergencia!
            }

    def simular_realidad(self, lectura_actual):
        """
        El Sueño del Córtex para el Límbico.
        """
        # Predice que en el próximo segundo bajará un poco por la inercia
        return round(lectura_actual - 0.05, 2)