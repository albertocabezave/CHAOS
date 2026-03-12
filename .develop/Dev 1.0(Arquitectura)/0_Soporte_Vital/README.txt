# El "Tallo Cerebral": Lo más crítico e inmutable.

# Especificación funcional: Sistema de Filtrado Sebsorial y Persistencia 
(Tálamo - Hipotálamo)

1. Introducción.
    Este documento detalla la arquitectura de la capa de Soporte Vital del Organismo Digital.
El objetivo es garantizar la resciliencia del sistema ante fallos de hardware(ruido) y 
situaciones catastróficas(incendio/fallo total), separando la clasificación de datos de la
ejecución de acciones.

2. Arquitectura del Tálamo(Filtro de Integridad)
    El Tálamo como un procesador de señales de baja latencia (60 Hz). Su única responsabilidad
es asigna un Estado de Señal a cada pulso entrante basándose en tres capas de validación.

2.1. Capas de validación.
    1. Capa de Integridad (Hardware): Valida la persistencia de voltaje/señal del sensor.
    Si falla, etiqueta como SORDERA.

    2. Capa de Realidad Física(Límite Universal): Define el rango en que el sensor opera del
    forma fiable.

        - Ejemplo: Un sensor de ambiente que marca 150°C se sale del "Universo de Posibilidad
        Física" para una granja avícola. Resultado: RUIDO.

    3. Capa de Seguridad Biológica-Física(Límite Operativo): Rango de bienestar para el 
    sujeto(animales) u objeto(Materiales).