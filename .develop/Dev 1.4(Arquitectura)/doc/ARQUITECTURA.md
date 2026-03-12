===========================================================================================
*******************************************************************************************
# ARQUITECTURA DE ORGANISMOS DIGITALES
## Versión 1.4
### Sistema de Control Cognitivo Universal
*******************************************************************************************
### Arquitecto Pricipal: Alberto Cabeza | El Vigía, Mérida, Venezuela | 2026
*******************************************************************************************
===========================================================================================
------------------------------------------------------------------------------------------
## Resumen Ejecutivo
Este documento formaliza la arquitectura técnica y las bases científicas del Sistema de 
Organismos Digitales, unframework de control inteligente inspirado en la cognición 
biológica. El sistema no es un programa lineal sino un organismo digital desacoplado 
en tres capas: ADN(datos de configuración), SOMA(motor de procesamiento) y MUNDO(entorno 
sensorial). Su aplicación inicial es la automatización ambiental de una granja de 
codornices(ROBUSTO'S) en El Vigía, Mérida, Venezuela, pero su diseño ontológico lo hace 
universalmente aplicable a cualquier industria de control sin modificar la lógica central.

La arquitectura cognitiva implementa un ciclo de cinco etapas:
--Neurocepción, Atención, Modelo del Mundo y Motivación-- respaldado por teorías 
neurocientíficas de primer nivel, incluyendo la Teoría del Espacio de Trabajo Global 
(Baars, 1988), la Hipótesis de Marcador Somático(Damasio, 1994) y la Teoría de la 
Codificación Predictiva(Friston, 2010).
-------------------------------------------------------------------------------------------
## 1. Fundamentos Folosófico/Técnicos
El principio rector del sistema es la Entropía Mínima: toda solucion debe tender hacia la menor complejidad posible manteniendo la mayor funcionalidad. Este principio tiene raíz 
directa en el Segundo Principio de Energía libre de Karl Friston, que postula que los 
sistemas cognitivos biológicos operan minimizando constantemente la sorpresa o 
incertidumbre sobre su entorno. Para decirlo de forma mas intuitiva, el sistema debe tener 
una baja densidad de interacciones entre sus elementos para evitar aumentar la entropía.

La separación en tres capas (ADN/SOMA/MUNDO) no es arbitraria. Reproduce el desacoplamiento
fundamental que la biología ha perfeccionado durante cientos de millones de años: el 
genotipo(ADN) contiene el manual de instrucciones, el fenotipo(SOMA) es su expresión física
y conductual, y el nicho ecológico (MUNDO) es el entorno que presiona y moldea la conducta.
Esta separación garantiza que la lóica de control sea Universal y que todos los datos
cambien entre aplicaciones.
-------------------------------------------------------------------------------------------
## 1.1 Analogías Biológicas Formalizadas

### ADN -> Genotipo:
    Archivos JSON que contienen la identidad, el hardware disponible y los parámetros
    cognitivos. Son inmutables durante la ejecución; solo se modifican deliberadamente 
    mediante el editorADN.

### SOMA -> Fenotipo:
    Motor C++ (o Python en la fase de validación) que interpreta el ADN y ejecuta el ciclo 
    cognitivo. No conoce la industria ni la especie que controla; solo sabe procesar
    sensores y actuar sobre actuadores.

### MUNDO -> Nicho Ecológico:
    Carpeta de archivos que representa el estado actual del entorno. Puede ser alimentada
    por sensores físicos reales, por un microcontrolador externo o por un simulador 
    (Gemelo Digital).
-------------------------------------------------------------------------------------------
## 2. Arquitectura Cognitiva - El Ciclo de los 5 Procesos
El núcleo del sistema es un ciclo de procesamiento que replica los mecanismo fundamentales
de la cognición biológica. Cada etapa tiene un correlato neurocientífico documentado y una
implementación computacional directa.
-------------------------------------------------------------------------------------------
### 2.1 Neurocepción - La percepción Integrada
La neurocepción es el proceso de integración de toda la información disponible antes de que
comience cualquier procesamiento cognitivo. El sistema implmenta cuatro canales 
percetuales, análogos a los sistemas sensoriales del sistema nervioso:

### Introspección:
    Monitoreo del estado interno del sistema: temperatura objetivo, fotoperiodo, niveles de
    confort. Análogo a la interocepcion humana, procesada por la insula cortical.
    > Fuente: Craig, A.D. (2002). "How do you feel? Interoception: the sense of de 
    physiological condition of the body." Nature Reviews Neuroscience.

### Exterocepción:
    Captura de variables del entorno externo a través de sensores(temperatura ambiente, 
    humedad).
    Procesada por corteza sensorial primaria y secundaria.

### Propiocepcion:
    Verificación del estado del propio hardware: actuadores encendidos/apagados, consumo 
    eléctrico. Análogo al sistema propioceptivo muscular.
    > Fuente: Sherrington, C.S.(1906). "The Integrative Action of the Nervous System."

### Nocicepción:
    Detección de estados de daño o amenaza: sobrecarga eléctrica, temperatura de fiebre.
    Análogo a los nociceptores periféricos. Los umbrales son configurables en el ADN.
-------------------------------------------------------------------------------------------
## 2.2 Atención - El Filtro de Prioridades:

    La Atención determina que información merece procesamiento profundo y que puede 
    ignorarse. El sistema implementa un scheduler de prioridades ponderadas: cada variable
    sensorial tiene un peso de Atención(0.0 a 1.0) definido en el ADN. Las variables con
    mayor peso consumen mas ciclo de procesamiento.

    Base científica: La Tería del Espacio de Trabajo Global(Global Workspace Theory) de 
    Bernard Baars(1988) postula que la conciencia emerge cuando la información sensorial
    compite y gana acceso a un "espacio de trabajo" central de capacidad limitada. El
    mecanismo de pesos del sistema replica este proceso de competencia: un peso de 
    Atención de 0.98 para la temperatura significa que ese sensor casi siempre gana el 
    acceso al procesamiento central.

    > Fuente I: Baars, B.J. (1988). A Cognitive Theory of Consciousness. Cambrigde 
    University Press.

    > Fuente II: Dehaene, S., Changeux, J.P.(2011).
    "Experimental and Theoretical Approaches to Conscious Processing." Neuron.
-------------------------------------------------------------------------------------------
## 2.3 Emociones - El Sistema de Evaluación

    Las 
