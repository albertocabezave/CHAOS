class Limbico:
    def __init__(self, adn_limbico):
        self.config = adn_limbico
        self.memoria = []
        self.nivel_estres = 0.0 # 0.0 (Calma) a 1.0 (Pánico)
        self.umbral_mentira = adn_limbico['umbral_sorpresa']

    def procesar_emocion(self, dato_real, dato_virtual=None):
        """
        Compara la realidad con la Memoria y con el sueño del Córtex
        """
        # 1. Guardar en memoria de corto plazo
        self.memoria.append(dato_real)
        if len(self.memoria) > 10: self.memoria.pop(0)

        # 2. Detectar "Sorpresa" (Salto brusco en la realidad)
        if len(self.memoria) > 1:
            salto = abs(self.memoria[-1] - self.memoria[-2])
            if salto > self.umbral_mentira:
                self.nivel_estres += 0.02
                print(f"[LÍMBICO] ¡SOPRESA! Salto de {salto}°C detectado.")
            else:
                self.nivel_estres -= 0.05 # Se calma si es estable

        # 3. Detectar "Mentira" (Diferencia con el Gemelo Digital)
        if dato_virtual is not None:
            error_prediccion = abs(dato_real - dato_virtual)
            if error_prediccion > self.umbral_mentira:
                self.nivel_estres += 0.3
                print(f"[LÍMBICO] ¡ESTRÉS! El Cortéx está alucinando. Error: {error_prediccion} °C")

        # limitar el estrés
        self.nivel_estres = max(0.0, min(1.0, self.nivel_estres))

        return self.nivel_estres