===========================================================================================

# Ciclo de vida del Cerebro Base(Loop)
    Todo software de control funciona en un bucle infinito.
    El "corazón" del núcleo hace esto repetidamente: 
        1. Leer: Obtiene el dato del sensor de temperatura.
        2. Proteger(Reptil): Revisa si ese dato significa que el sistema
        va a explotar.
        3. Filtrar(Límbico): Limpia el dato(quita el ruido) y lo guarda en la memoria.
        4. Consultar(Cortex): Le pasa el dato limpio al Cortex y le pregunta "Qué hacemos?".
        5. Actuar: Ejecuta la orden en el ventilador o válvula.

    1. El Reptiliano (La Barrera de Fuego)
    Es el primer filtro. Su código es una simple comparación.
        - Entrada: Temperatura actual.
        - Referencia: Temperatura Crítica(Obtenida del Cortex).
        - Lógica: Sin T_actual >= T_crítica -> [ESTADO DE PÁNICO - Activa Protocolo de
        emergencia y envía una señal de ERROR].
            - Si no -> PASA EL DATO al Límbico.

    2. El Límbico(El Suavizador)
    Este es el mas interesante. No queremos que el ventilador se vuelva loco si el sensor da
    un salto falso. Usaremos un Promedio Movil.
        - Memoria: Una lista (buffer) de las últimas 10 lecturas(Dependiendo de la industria).
        - Lógica:
            1. Recibe el dato del Reptiliano.
            2. Lo mete en una lista y saca el mas viejo.
            3. Calcula el promedio de la lista(T_estable).
            4. RESULTADO: Entrega T_estable al Córtex.

    3. El Núcleo (El Director de Orquesta)
    El Núcleo es el que tiene los "cables" conectados a las carpetas. Su función es 
    asegurar que el Reptiliano y el Límbico hablen entre ellos.

    El contrato de seguridad: Si el Reptiliano detecta peligro, el Núcleo tiene la orden
    de no dejar que el dato llegue al Límbico ni al Córtex. Se corta el puente.

===========================================================================================

    El viaje de un DATO(De la Granja al Actuador)
    Imaginemos que el sensor detecta un cambio. El dato tiene que sobrevivir a una carrera
    de obstáculos antes de convertirse en una acción:
        1. Nivel de voltaje(Núcleo): El dato entra. Es sólo un número bruto (ej. 38.5).

        2. El Muro de Fuego(Reptiliano): El sistema pregunta, Éste núnero destruye el
         hardware?
            - Si el límite es 45.0, el 38.5 pasa.
            - Si el número fuera 46.0, el Reptiliano mata el proceso inmediatamente. Y 
            ejecuta el Protocolo de seguridad.
        
        3. La Cámara de Calma(Límbico): El 38.5 entra en una fila con los últimos 9 datos
        recibidos.
            - Se suma con los anteriores y se divide.
            - El resultado es un número "suave"(ej. 38.2). Esto evita que un error de un 
            milisegundo active un motor gigante por gusto.

        4. La Mesa de Estrategia(Córtex): El dato suave (ej. 38.2) llega aquí.
            - El Cortex consulta su manual (el .json).
            - Dice: "Para 38.2°C en una Granja Avícola, necesito ventiladores al 80%.

        5. El Brazo(Núcleo): El Córtex le devuelve la orden al Núcleo, y este mueve 
        físicamente el ventilador.

        Nota importante: El tiempo del latido debe ser de 1 vez por segundo, ya que si lo 
        hace muy rápido saturaría la memoria. Aunque dependiendo de la industria este número
        podría necesitar cambiarse.