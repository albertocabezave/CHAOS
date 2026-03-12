class Reptiliano:
    def __init__(self, adn_industria):
        #El Reptiliano recibe su parte del ADN al nacer.
        self.seguridad = adn_industria['reptiliano_seguridad']
        self.identidad = adn_industria['identidad']

    def talamo_etiquetar(self, valor_crudo, id_sensor):
        """
        Le da sentido al dato crudo.
        En el futuro, aquí es donde vincularé el pin físico
        con un nombre
        """
        etiqueta = f"Lectura_{id_sensor} _{self.identidad['especifico']}"
        return {"etiqueta": etiqueta, "valor": valor_crudo}

    def hipotalamo_vigilar(self, dato_etiquetado):
        """
        Compara el dato con los limites de muerte.
        Retorna True si todo está OK, False si hay que entrear en SHOCK.
        """
        valor = dato_etiquetado['valor']
        limite_alto = self.seguridad['temp_critica_alta']
        limite_bajo = self.seguridad['temp_critica_baja']

        if valor >= limite_alto or valor <= limite_bajo:
            print(f"[ALERTA CRÍTICA] {dato_etiquetado['etiqueta']} fuera de rango: {valor}!")
            return "MODO_SHOCK"

            return "ESTADO_ESTABLE"