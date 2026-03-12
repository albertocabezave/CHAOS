import random

class EntornoFisico:
    def __init__(self, temp_inicial=28.0, inercia=0.2, ganancia_pasiva=0.4):
        self.temp_interior = temp_inicial
        # Simulamos el calor de la calle en El Vigía (34 grados)
        self.temp_exterior = 34.0  
        self.inercia = inercia
        self.ganancia_pasiva = ganancia_pasiva

    def actualizar(self, potencia_actuadores):
        """
        Calcula la nueva temperatura basándose en el intercambio de aire.
        """
        # Calculamos la diferencia (Delta)
        diferencial = self.temp_exterior - self.temp_interior
        
        # FÍSICA: Si afuera está más caliente, subir la potencia mete calor.
        # Si afuera está más frío, subir la potencia enfría.
        intercambio = (potencia_actuadores / 100.0) * self.inercia * diferencial
        
        # El sol sigue calentando el galpón (ganancia pasiva)
        self.temp_interior += self.ganancia_pasiva + intercambio
        
        # Un toque de caos ambiental (entropía)
        self.temp_interior += random.uniform(-0.02, 0.02)
        
        # El clima de afuera también se mueve un poco
        self.temp_exterior += random.uniform(-0.03, 0.03)
        
        # DEVOLVEMOS DOS VALORES: Interior y Exterior
        return round(self.temp_interior, 2), round(self.temp_exterior, 2)