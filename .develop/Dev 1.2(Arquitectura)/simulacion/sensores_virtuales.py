import random

class SensorVirtual:
    def __init__(self, nombre, margen_error=0.5):
        self.nombre = nombre
        self.margen_error = margen_error 
        self.esta_vivo = True

    def capturar(self, temp_fisica_real):
        """ 
        Toma la temperatura real del mundo y le añade el ruido 
        propio del hardware para que la IA aprenda a filtrar.
        """
        if not self.esta_vivo:
            return -999.0 
            
        # Aplicamos la entropía del sensor (el ruido del DHT22)
        error_muestreo = random.uniform(-self.margen_error, self.margen_error)
        
        return round(temp_fisica_real + error_muestreo, 2)

    def simular_fallo(self):
        """ Simula que se desconectó un cable o se quemó el sensor """
        self.esta_vivo = False