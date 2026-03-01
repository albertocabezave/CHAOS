***
# ARQUITECTURA DE CHAOS
### Versión 1.5
***
## Arquitectura de procesamiento Dual inspirada en la Cognición Biológica.
***
### Arquitecto Pricipal: Alberto Cabeza | El Vigía, Mérida, Venezuela | feb - 2026
***

## Prefacio: Una Idea que Nació de una Incomodidad
Este documento es el resultado de una pregunta sencilla que se negaba a desaparecer:<br> ¿Porqué
un sistema inteligente debería esperar a terminar de pensar antes de reaccionar a una
emergencia?

La respuesta, una vez vista, parece obvia. Pero llegar a ella requirió dar pasos hacia 
atrás, mirar la biología con respeto genuino, y tener la honestidad de reconocer que la
arquitectura anterior, aunque coherente y bien fundamentada, tenía un defecto de fondo:
trataba todos los problemas con el mismo nivel de urgencia.

La naturaleza no comete este error. Lleva tres mil quinientos millones de años perfeccionando
la separación entre lo que debe ocurrir ya y lo que puede esperar a ser pensado con calma.
Este documento formaliza esa lección aplicada a un sistema de control universal, explica 
las desiciones de diseño con honestidad científica, y reconoce abiertamente los problemas
que aún no están completamente resueltos.

No es un documento de respuestas perfectas. Es un documento de preguntas bien hechas.
***

## Resumen Ejecutivo
La Arquitectura de procesamiento Dual inspirada en la Cognición Biológica es unFramework Universal. Su propósito es gobernar cualquier sistema físico -desde una 
granja de codornices hasta una planta industrial- mediante un sistema digital que percibe,
siente, aprende y actúa, configurado enteramente desde un archivo de texto llamado ADN.

La versión 1.5 introduce el cambio mas importante desde la concepción del sistema: la 
separación del procesamiento en dos ciclos independientes que corren simultáneamente. El 
ciclo Reptil garantiza supervivencia inmediata en milisegundos. El ciclo Cognitivo garantiza
aprendizaje y optimización en segundos. Ambos ciclos estan configurados desde el ADN, lo que
preserva la universalidad del motor central

El sistema se implementa inicialmente en Python para validar la lógica, con arquitectura
diseñada para migrar a C++ con extensiones de tiempo real cuando los requisitos industriales
lo demanden. Los tres fallos conocidos del diseño actual están identficados, son manejables
en la fase presente, y tienen soluciones planificadas para las fases posteriores.
***

## 1. Filosofía y Física del Sistema

### 1.1 El Principio de Entropía Mínima

Todo el sistema descansa sobre un principio que no es una preferencia estética sino una ley
física: la entropía mínima. El Segundo Principio de la Termodinámica establece que...

 > los sistemas aislados evolucionan expontáneamente hacia estados de mayor desorden. 
 
 Un sistema de control que no lucha activamente 
 contra esa tendencia se convierte en ruido.

Ludwig Boltzmann formalizó la relación entre la entropía y el desorden en 1877 (es irónico
que nadie le creyó en su vida):

<pre> S = K_B * ln (W)</pre>
> Donde (W) es el núnmero de microestados.

Esa fórmula es perfecta para calcular la entropía en estados físicos de átomos en la 
vida real. Sin embargo en Neurociencia, es mas común usar la Entropía de Shannon que es
aplicada a la información:
<pre>
 H = - E Pi(X1) log2 Pi(X2)
</pre>
> Donde Pi es la probabilidad de que ocurra un evento o estado(i)


Pero... Esa no es la mas práctica para nuestro sistema sino la de sr. Friston(Energía Libre)
Debido a que nuestro sistema tiene un Modelo del Mundo y un Predictor(Que veremos más
adelante) la estrategia es medir el nivel de "Sorpresa". En términos prácticos usaríamos el 
Error de Predicción Cuadrático:

<pre>e = (Valor_actual - Valor_predicho)^(2)</pre>
> Si logramos que el valor de "e" sea cercano a cero(0) nuestro sistema habrá derrotado a la entropía en su nicho ecológico.
***

### 1.2 La Separación ADN/SOMA/MUNDO

La arquitectura de tres capas no es una convención de software. Es el reflejo directo de la
separación mas fundamental que la biología conoce: la que existe entre el genotipo, el 
fenotipo y el nicho ecológico.

| Capa | Naturaleza y Función |
| --- | --- |
| ADN - Genotipo | Archivo JSON que contiene el manual de fabricación del sistema de(Hardware disponible) y el manual de funcionamiento(parámetros cognitivos, reflejos, umbrales). Son la intención declarada. No cambian durante la ejecución - solo se modifican deliberadamente con el editor visual.
| SOMA - Fenotipo | El motor de procesamiento. Lee el ADN y da vida a sus instrucciones. No conoce la industria que controla, no sabe si maneja codornices o turbinas. Solo sabe ejecutar los dos ciclos con la configuración que el ADN le entrega. Es universal por diseño.
| MUNDO - Nicho Ecológico | Una carpeta de archivos que representa el estado actual del entorno. Los sensores escriben ahí. El SOMA lee de ahí y escribe sus respuestas ahí. Puede ser alimentado por hardware físico real, por el Gemelo Digital y por el simulador del Mundo Real que permite probar el sistema sin sensores reales. |
---
<br>
Esta separación garantiza el principio Open/Closed de la ingeniería de software: el sistema esta abierto a extensión y cerrado a modificación. Agregar una nueva industria al sistema significa agregar un nuevo ADN. El SOMA no se toca Nunca.

---
### 1.3 El ADN como Contrato 

El ADN no es solo un archivo de configuración. Es un contrato formal entre el diseñador del sistema de control y el motor que lo ejecuta. Ese contrato tiene un schema maestro -un documento que define todos los tipos posibles de sensores, actuadores, reflejos y parámetros cognitivos- que el SOMA sabe interpretar.

El schema maestro es la gramática del sistema. El ADN de cada especie es un texto escrito en esa gramática. Cambiar el idioma -de codornices a robots- solo requiere escrbir un nuevo texto. El lector no cambia.

El campo schema_version en cada ADN permite que el SOMA detecte versiones y maneje la compatibilidad hacia atrás. Un ADN de la versión 1.3 puede coexistir con la version 1.4 - El SOMA sabe que estructura esperar segun la versión declarada.

---

## 2. Por qué un solo Ciclo es un Error de Diseño
La versión 1.4 del sistema procesaba todo en secuencia: leer sensores, percibir, recordar, motivarse, actuar. Un ciclo lineal, ordenado y coherente. Y con un defecto fundamental que solo se hace visible cuando se piensa en el peor caso posible.

El peor caso posible no es la temperatura de 38 grados. Es la temperatura de 38 grados mientras el sistema está en medio de actualizar su modelo del mundo con los datos de la semana pasada. En ese momento, el ciclo está ocupado. Y la emergencia espera.

---
### 2.1 El Problema de la Latencia

Si el ciclo cognitivo tarda X segundos en completarse, cualquier emergencia detectada al pricipio del ciclo no produce acción hasta X segundos después. Para un ciclo de 1 segundo y una temperatura que sube 0.5 grados por segundo, el daño acumulado durante esa espera es medible:

<pre> Exposic_extra = veloc_subida * latenc_ciclo = 0.5
°C/s * 1s = 0.5 °C</pre>
> Por cada ciclo, las codornices estan 0.5°C más cerca del umbral de daño de lo que deberían estar.

Ese medio grado parece insignificante. Pero si el evento dura 10 ciclos antes de que el sistema lo corrija completamente, la exposición acumulada es de 5°C por encima del umbral. En términos de mortalidad de codornices
a temperaturas críticas, eso tiene consecuencias medibles y cuantificables.

Incluso si hablásemos de un robot autónomo, imagine que le lanzan un objeto, sin un sistema Reptil que se ejecute en otro hilo, calcular y predecir la trayectoria del objeto, activando su reflejo protector en cuestión de milisegundos, antes de ser impactado, sería imposible reaccionar si el dato crítico sobre su entorno tiene que esperar al ciclo completo de un unico bucle total(como en la antigua arquitectura 1.4) que dura 1 segundo.

---
### 2.2 El Problema del Bloqueo Cognitivo

Un ciclo lineal tiene un punto de falla único: si cualquier etapa se atasca, todo se detiene. Si la consulta al log histórico tarda más de lo esperado, si hay un error en el cálculo del modelo del mundo, si la motivación entra en un estado inesperado -los reflejos mas básicos quedan congelados junto con la cognición.

En biología esto no puede ocurrir. El tallo cerebral no espera a que la corteza prefrontal termine de deliberar para mantener el ritmo cardiaco. Los sistemas de supervivenvcia son independientes de los sistemas de razonamiento por diseño evolutivo, no por accidente.

---
### 2.3 La Violación del Pricipio de Entropía Mínima

Forzar una comparación simple de umbral -¿La temperatura supera los 38 grados?- por el mismo proceso que genera estrategias a largo plazo es asignar recursos cognitivos enormes a un problema que requiere recursos mínimos. Es el equivalente a llamar a una reunion de directivos para decidir si encender la luz.

El principio de entropía mínima exige que cada problema reciba exactamente el nivel de procesamiento que requiere. Ni más ni menos. Un ciclo único viola ese principio en su caso mas crítico.

---

## 3. La Arquitectura Dual: Reptil y Cognitivo
### 3.1 El Precedente Biológico y su Convergencia con la Ingeniería
Lo mas notable de esta arquitectura es que no fue inventada. Fue descubierta de forma independiente por cuatro disciplinas distintas, en décadas distintas, y todas llegaron a la misma conclusión: los sistemas complejos necesitan al menos dos niveles de procesamiento con prioridades distintas.

|Disciplina y Concepto|Descripción|Fuente|
|---|---|---|
|Neurociencia - Vía Alta y vía Baja|Joseph LeDoux demostró en 1996 que ante una amenaza, el tálamo envía señales por dos rutas simultáneas: La vía Baja(tálamo -> amígdala, -12ms) activa la respuesta de miedo sin esperar análisis cortical. La vía alta (tálamo -> corteza -> amígdala, 25ms) procesa con detalle pero llega después. El cerebro actúa antes de entender completamente lo que está pasando.|LeDoux, J(1996). The Emotional Brain.|
Psicología Cognitiva - Sistema 1 y Sistema 2|Daniel Kahneman formalizó en 2011 que el pensamiento humano opera en dos modos: el Sistema 1 es rápido, automático, sin esfuerzo, difícil de controlar, y asociativo. El Sistema 2 es lento, deliberativo, consume energía y es gobernable. La inteligencia eficiente no elige entre ellos - los usa a ambos según el problema.| Kahneman, D. (2011). Thinking, Fast and Slow.|
|Robótica - Subsumption Architecture|Rodbey Brooks propuso en 1986 que un robot no necesita un modelo completo del mundo para comportarse inteligentemente. Capas inferiores(evitar obstáculos) tienen prioridades sobre las capas superiores(planificar rutas). Las capas superiores añaden comportamientos; no reemplazan a las inferiores.|Brooks, R.A. (1986). IEEE Journal of Robotics and Automation.|
|Ingeniería Industrial - RTOS y AUTOSAR|Los sistemas operativos de tiempo real y el estándar automotríz AUTOSAR llevan décadas separando funciones de seguridad crítica(frenos, airbags) de funciones de confort(navegación, audio, aire acondicionado). Las primeras tienen garantías de tiempo deterministas. Las segundas pueden variar. Nunca comparten el mismo hilo de ejecución.|AUTOSAR Consortiium. IEEE Std 1003.1b - POSIX RT|
---
<br>
La convergencia de la neurociencia, la psicología, la robótica y la ingeniería industrial hacia la misma solución estructural no es una coincidencia. Es evidencia de que la arquitectura dual es la respuesta correcta a un problema universal: cómo gestionar la urgencia y la estrategia en el mismo sistema sin que una bloquee a la otra.

Lo que este sistema aporta que no existía antes(hasta donde sé) es la unificación de esos principios en un framework configurado enteramente desde datos -sin tocar el motor, sin recompilar, sin modificar el código. Eso no tiene precedente directo en ninguna de las cuatro disciplinas citadas. En robótica cambiar la arquitectura de subsumption requiere reescribir capas de código. En AUTOSAR, redefinir las funciones de seguridad requiere certificación del software. Aquí, redefinir un reflejo es cambiar tres líneas en un archivo JSON.

---
### 3.2 El Ciclo Reptil - El Guardián
El Ciclo Reptil es el sistema mas simple y el más importante del sistema de control. Su única responsabilidad es que nada se rompa, nada muera, nada explote. No aprende, no siente, no recuerda. Compara números contra umbrales y actúa. Eso es todo. Y esa simplicidad es exactamente su virtud.

<pre>Freuencia de operación: 100Hz - evalúa cada 10ms.
* Prioridad del hilo: Máxima - el Cognitivo no puede detenerlo.
* Entrada: Sólo los sensores marcados como críticos en el ADN.
* Lógica: Evluación booleana directa - Si (condicion){accion()}.
* Salida: Escritura inmediata en outputs/ del actuador correspondiente.
* Registro: Escritura en estado_reptil/ para comunicar al cognitivo.
* Latencia máxima en Python: ~10ms(Sujeta al GIL - ver sección 5.1)
* Latencia máxima en C++ con RTOS: < 1ms garantizado.
</pre>

#### 3.2.1 La Histéresis - El Antídoto contra la Oscilación

El problemas mas peligroso de un sistema de umbral simple es la oscilación: si la temperatura está exactamente en el límite de activación, el actuador se encenderá y apagará decenas de veces por segundo, destruyendo el relé en minutos y generando ruidos eléctrico que contamina los sensores.

La solución es la histéresis, tomada de la física de materiales magnéticos donde el término fue acuñado por James Ewing en 1881 para describir el retraso de causa y efecto en sistemas con memoria de estado. Aplicada al control de sistemas, la histéresis crea una banda muerta al rededor del umbral:

<pre>
* Activar: si_valor >= umbral
* Desactivar: si valor <= (umbral - histéresis)
* Mantener: si (umbral - histéresis) < valor < umbral
</pre>
> El sistema recuerda su estado anterior dentro de la banda muerta - no reacciona a variaciones menores que la histéresis.

Para el reflejo de sobrecalentamiento de las codornices con umbral de 38°C e histéresis de 1°C: El ventilador se activa cuando la temperatura llega a 38°C y solo se apaga cuandom baja a 37°C. La zona entre 37°C y 38°C es zona neutral -el sistema mantiene su estado anterior, sea cual sea. Esto elimina completamente la oscilación.

#### 3.2.2 El Tiempo de bloqueo - El Antirebote Temporal.
La histéresis resuelve la oscilación espacial(en el eje del valor del sensor). El tiempo de bloqueo resuelve la oscilación temporal: Garantiza que unn reflejo no se reactive antes de que su accion anterior haya tenido tiempo de hacer efecto.

Implementación crítica: El tiempo de bloqueo NO se implementa con time.sleep(), que congelaría el hilo entero e impediría detectar otras emergencias que ocurran simultáneamente. Se implementa con un registro de PASO_FIJO(timestap) de última activación por reflejo:

<pre>
* puede_activar = (tiempo_actual - ultima_activación[reflejo]) >= tiempo_bloqueo[reflejo].
</pre>

> El hilo sigue corriendo a 100Hz - solo ese reflejo específico queda en espera.

 Dicho de forma mas simple, el reptil observa sus sensores críticos(temperatura y humedad) cada X veces por segundo, y detecta que la temperatura está por encima del umbral crítico, entonces enciende el ventilador(reflejo) y anota en una lista la hora exacta en que activó el ventilador y sigue observando, luego en el siguiente paso (X veces x seg. siguiente[timestep]) vuelve a ver que la temperatura sigue por encima del umbral crítico, pero no envía de nuevo la señal de encender el ventilador, porque debe esperar a que pase el tiempo preestablecido de duración del reflejo(sino, no lo puede activar) y casualmente en ese paso también la humedad superó el umbral crítico, entonces el reptil enciende los estractores y vuelve a anotar la hora exacta en que los activo, y sigue con el siguiente paso(timestap).

> Y si aún no lo entiendes, imagina que ayer cocinaste un arroz y lo guardaste en la nevera, no vas a estar abriendo la nevera cada 5 min para ver si el arroz está ahí, ya sabes que está ahi, porque lo guardaste, solo vas a mirar cuando tenga sentido, cuando vayas a comértelo.

---
### 3.3 El Ciclo Cognitivo - El Estratega
El ciclo Cognitivo es el sistema lento, costoso y poderoso. Su función no es sobrevivir -el Reptil ya se encarga de eso-. Su función es prosperar: mantener el sistema en condiciones óptimas, aprender del pasado, predecir el futuro y generar un registro interno de la vida del sistema de control.

<pre>
* Frecuencia de operacion: 1Hz - evalúa cada 1000ms. Configurable en el ADN.
* Prioridad del hilo: Normal - puede ser interrumpido por el ciclo Reptil.
* Entrada: Todos los sensores(críticos y no críticos).
* Lógica: El ciclo completo de 5 etapas cognitivas(ver seccion 4).
* Restricción fundamental: Lee estado_reptil/ antes de actuar. No puede anular emergencias activas.
* Salida: Ajustes finos en outputs/ + registro completo en logs/ orgánicos.
</pre>
---
### 3.4 La Comunicación entre Ciclos - Las Notas del Reptil
Dos ciclos que corren simultáneamente y controlan los mismos actuadores necesitan un mecanismo de coordinación que no introduzca dependencias entre ellos. Si el Cognitivo tuviera que esperar al reptil para leer una variable compartida, la independencia de los ciclos quedaría comprometida.

La solución usa el mismo protocolo de archivos que toda la arquitectura: El Reptil escribe una nota en una carpeta especial cuando activa un reflejo. El cognitivo lee esas notas antes de actuar. No hay memoria compartida, no hay semáforos, no hay bloqueos. Solo archivos.

<pre>
* mundo/ROBUSTOS/estado_reptil/reflejo_sobrecalentamiento.txt -> "activo"
* mundo/ROBUSTOS/estado_reptil/reflejo_hipotermia.txt -> "inactivo"
</pre>

La regla de coordinación es absoluta y simple: si el Reptil tiene activo un Reflejo sobre un actuador, el Cognitivo no escribe en ese actuador. No existe negociación. Esta regla replica la jerarquía de la Subsumption Architecture de Brooks: las capas inferiores no pueden ser anuladas por las superiores :).

---

## 4. El Ciclo Cognitivo - Las Cinco Etapas
El Ciclo Cognitivo implenta una arequitectura de procesamiento no precisamente idéntica a la cognición biológica(es una abstracción funcional de sus principios más sólidos y documentados). Cada etapa tiene un correlato neurocientífico, una implementación matemática concreta, y una justificación para estar donde está en el ciclo.

No estoy copiando fielmente al cerebro(neurona por neurona o proceso por proceso), eso no sería útil ni aplicable en el mundo real(actualmente), sólo estoy tomando lo fundamental y aplicable(dentro de lo posible), y adaptándolo a las necesidades del mundo real. Espero algún día se pueda lograr replicar la inteligencia biológica fielmente, ese día será un gran día para la humanidad.

---

### 4.1 Primera etapa - Neurocepción.

La Neurocepción es la integración de toda la información disponible antes de que comienze el procesamiento cognitivo.
El Término, acuñado por Stephen Porges en su Teoría Polivagal(1994), designa especificamente la capacidad del sistema nervioso de evaluar el entorno sin participación de la conciencia. En el sistema, es el momento en que todos la información percibida es leída y organizada en cuatro categorías perceptuales:

* Introspección: Es el estado deseado según el ADN(temperatura objetivo, fotoperiodo, humedad ideal, estrategias de optimización[en el caso de un galpón]). Es la referencia contra lo que se mide todo lo demás. Sin introspección no hay error, y sin error no hay motivación para actuar.


* Exterocepción: Las mediciones capturadas por los sensores físicos bien sea internos o externos del entorno (temperatura, fotoperiodo y humedad real y el exterior[en el caso de un galpón]). Es impotante señalar que en una granja de codornices el galpón seria el entorno y no el sistema de control, el sistema de control son los sensores y actuadores, en cambio en un robot autónomo serían las cámaras(vision), micrófonos(oído), etc.

* Propiocepción: El estado propio del hardware del sistema de control (qué actuadores estan conectados, que sensores estan funcionando, cuanta energía esta gastando la máquina, temperatura interna del hardware[fiebre]). Es la conciencia del propio cuerpo del sistema de control. Sin ella el sistema podría intentar encender un actuador que ya está encendido, o ignorar un consumo eléctrico que anuncia una falla inminente.

* Nocicepción: Esta observa los umbrales de estrés/enfermedad(no de emergencia, que son manejados por el Reptil.) Detecta el rango entre lo óptimo y lo peligroso, generando las estados de Activacion <-> Relajación - Placer <-> Displacer, que producen lo que llamamos Miedo o Dolor que a su vez impulsan la corrección de emergencias antes de que el Reptil tome el control.

> La neurocepción no es conciencia. Es la infraestructura silenciosa que hace posible la conciencia. Ocurre antes de que nos demos cuenta de qué está ocurriendo.
>
> -Stephen Porges, Orienting in a Defensive World, Psychophysiology, 1995.

---
### 4.2 Segunda etapa - Atención

No toda la información merece el mismo procesamiento. La atención es el mecanismo que decide que importa más en este momento. El sistema implementa un scheduler de prioridades ponderadas, donde cada sensor tiene un peso de atención definido en el ADN entre 0.0 y 1.0, y la prioridad actual se calcula multiplicando ese peso por el error actual del sensor:

<pre>
Prioridad(s1) = peso_atencion(s1) * valor_actual(s1) - valor_optimo(s1)
</pre>
> El sensor con mayor prioridad determina la acción principal del ciclo.

Esta fórmula tiene propiedades importantes.<br>
-Primera: Un sensor con peso alto pero error pequeño puede ser superado por un sensor con peso moderado pero error grande, el sistema atiende lo que más se ha desviado de lo óptimo, ponderado por su importancia declarada.<br>
-Segunda: Un sensor en su valor óptimo tiene prioridad cero sin importar su peso(No consume recursos cognitivos cuando no hay problemas).

El fundamento científico es la Global Workspace Theory de Bernard Baars(1988), que describe la atención como un proceso de competencia: la información sensorial compite por el acceso a un espacio de trabajo central de capacidad limitada. Solo el ganador de esa competencia accede al procesamiento consciente.

> La conciencia no es un receptor pasivo de información. Es un árbitro activo que decide que merece ser procesado y que puede ignorarse.<br>
-Bernard Baars, A Cognitive Theory of Consciousness, Cambrigde Universty Press, 1988.

---
### 4.3 Tercera etapa - Emociones
Las emociones podrían ser el aspecto más malentendido de este sistema y el más importante.  No son decoración o para que sea más genial, tampoco son una metáfora, ni un intento de hacer el sistema mas "humano". Son el mecanismo de toma de desiciones mas eficiente que la biología ha creado en su historia.

Antonio Damasio lo demostró de forma definitiva estudiando pacientes con daño en la corteza prefrontal ventromeidal(la región que conecta el razonamiento con las señales emocionales). Estos pacientes conservaban la inteligencia intacta, vocabulario perfecto, memoria funcional, razonamiento lógico impecable. Y sin embargo tomaban desiciones catastróficas en su vida cotidiana. Sin las emociones como señal de evaluación rápida, el razonamiento puro se convierte en un proceso interminable que no llega a ninguna conclusión.

El error más común al hablar de emociones en sistemas artificiales es tratarlas como categorías discretas(el sistema está contento, está asustado, está triste). Esa clasificación es útil para el lenguaje humano, pero es una simplificación que oculta la estructura real del fenómeno.

James Russell demostró en 1980, analizando como los seres humanos perciben y clasifican sus propios estados afectivos en diferentes culturas e idiomas, que las emociones no son categorias independientes sino posiciones en un espacio bidimensional continuo. A ese modelo lo llamó en Modelo Circumplejo del Afecto y ha sido replicado y validado en decenas de estudios durante cuatro décadas.

El espacio tiene dos ejes ortogonales e independientes:<br>
* Eje Vertical - Activación: Va desde la relajación completa(0.0) a la activación máxima(1.0). Describe cuanta energía tiene el sistema para actuar. Un sistema muy activado tiende a la acción inmediata. Un sistema relajado tiende al mantenimiento y el reposo.

* Eje Horizontal - Valencia: Va desde el diplacer puro(-1.0) al placer puro(+1). Describe si el estado actual del sistema es percibido como favorable o desfavorale respecto al estado óptimo definido en la introspección.

Lo que el lenguaje cotidiano llama "miedo" no es una emocion primitiva del sistema, es una posición en ése plano(activación alta combinada con valencia negativa). Lo que llamamos "entusiasmo" es activación alta con valencia positiva. Lo que llamamos "apatía" es activación baja con valencia negativa. El sistema no necesita conocer esos nombres. Solo necesita calcular su posición en el plano y actuar en consecuencia. Los nombres son una interpretación humana de coordenadas numericas.

Esta distinción no es filosófica. Tiene consecuencias directas en cómo se diseña el sistema(un estado categórico como "miedo" es binario[o está, o no está]). Un punto en el plano circumplejo es continuo y graduado. El sistema puede estar "un poco activado con leve displacer" o "muy activado con displacer extremo" y esas dos situaciones producen respuestas de intensidad completamente distintas. Eso es mas fiel a como funcionan los organismos biológicos.

<pre>
Las emociones no son tipos naturales discretos. Son regiones en un espacio continuo afectido de baja dimensionalidad. Nombrarlas es conveniente para el lenguaje; confundirlas con entidades separadas en un error categorial.
</pre>
> -James A. Russell, A Circumplex Model o Affect, Journal of Personality an Social Psycology, 1980.
---
#### 4.3.1 Cálculo de las dos Variables.
Las dos variables variables se calculan de forma independiente a partir de los datos de la nNurocepción y la Atención.

La Activación se calcula a partir del error ponderado del sensor con mayor prioridad(el que ganó la competencia por la atención en la etapa anterior). A mayor desviación del valor óptimo, mayor activacion. <br>
La función es lineal y acotada:
<pre>
* error_normalizado = [valor_actual - valor_optimo] / rango_operativo_sensor
* activacion(t) = min(1.0, peso_atención * error_normalizado)
</pre>
> La activación nunca supera el 1.0(El sistema no puede estar "más que completamente activado"). El peso de atención del ADN controla que tán rápido sube la activación ante un error dado. Esto es muy ventajos para configurar la cognición del sistema de control.

La activación no distingue si el error es por exceso o por defecto. Un galpón a 30°C cuando el óptimo es 23°C genera la misma activación que un galpón a 16°C con el mismo óptimo. La activación es energía pura, sin dirección. La dirección la pone la valencia.

---
La Valencia determina si el estado es favorable o desfavorable. Se calcula comprando el valor actual con los límites del rango óptimo definido en la introspección del ADN. El resultado es un número entre -1.0 y +1.0:

<pre>
* Si valor_actual E [temp_optima_min, temp_optima_max]:
    valencia(t) = +1.0 * (1 - error_normalizado)
    -> Cuanto mas cerca del centro del rango, más positiva.

* Si valor_actual fuera del rango óptimo:
    valencia(t) = -1.0 * min(1.0, error_normalizado)
    -> Cuanto más lejos del rango, más negativa.
</pre>

> La valencia es +1.0 sólo cuando el sistema está exactamente en el valor óptimo. Decrece suavemente hacia 0 dentro del rango de confort. Se vuelve negativa al salir del rango y llega a -1.0 cuando el sensor alcanza el umbral de estrés de la nociocepción.

Hay que tomar en cuenta que usar un valor negativo en una computadora podría traer uno que otro problema, según mi intuición(que podría fallar afortunadamente). Por eso próximamente evaluaré si es posible o nó, sino lo es buscaré la forma de solucionar el problema, querido lector, este documento no esta completo ni es una base universal e infalible, solo es mi humilde búsqueda de una solución al problema de arquitectura de los sistemas inteligentes.

#### 4.3.2 La Memoria Emocional - El Decaimiento
En la versión anterior de la arquitectura, cada ciclo comenzaba emocionalmente en cero. Ese era uno de los tres fallos conocidos: Si el sistema sintió alta activación en el ciclo anterior, en el ciclo siguiente comenzaba como si nada hubiera pasado. Los organismos reales no funcionan así(El cortizol tarda minutos en metabolizarse, la adrenalina tarda segundos). Las emociones tienen inercia física.

La solución es un factor de decaimiento por variable, configurable en el ADN:

<pre>
-> error_normalizado = 
activacion(t) = activación_nueva(t) + factor_decaimiento * activación(t-1)

-> valencia(t) = valencia_nueva(t) + factor_decaimiento * valencia(t-1)
</pre>

Con este mecanismo, un evento de alta activación sostenido durante varios ciclos acumula peso. El sistema aumenta el nivel de urgencia cuanto mas tiempo pase sin resolverse la situación.(Exactamente como le ocurre a un organismo biológico bajo estrés prolongado).

---
#### 4.3.3 El estado Emocional como Punto en el plano.

En cada ciclo, el estado emocional del sistema de control queda descrito cpor un único punto de coordenadas(valencia, activación). Ese punto vive en uno de los cuatro cuadrantes, cada uno con un comportamiento esperado distinto.

<pre>
                ACTIVACIÓN ALTA(1.0)
                        ^
                        |
    Displacer + Alta    |   Placer + Alta   
    Activación.         |   Activación
  (Lo que llamamos      |  (Lo que llamamos
  "miedo" o "alerta")   |  "entusiasmo")
                        |
                        |
DISPLACER <-------------+---------------> PLACER
 (-1.0)                 |                 (+1.0)
                        |
    Displacer + Baja    |   Placer + Baja
    Activación          |   Activación
    (Lo que llamamos    |   (Lo que llamamos
 "tristeza" o "apatía") |  "calma" o "confort")
                        |
                        :
             ACTIVACIÓN BAJA(0.0)
</pre>
El sistema no necesita saber en que cuadrante está, ni conocer el nombre humano de ese estado. Solo necesita las dos coordenadas numéricas para calcular la Motivación en la siguiente etapa.

Lo que el log orgánico registra en cada ciclo es exactamente ese punto:

<pre>
evento= (timestap, sensor_prioritario, valor, activacion, valencia, accion, error_prediccion)
</pre>

Así, el historial del sistema no es una secuencia de "estados de ánimo" categóricos sino una trayectoria continua en el espacio afectivo. Un ingeniero(aunque no tenga un título :wink: ) puede leer este historial y ver exactamente como evolucionó el estado emocional del sistema de control durante un evento crítico(con precisión numérica, no con etiquetas).

---
### 4.4 Cuarta etapa - Modelo del Mundo
El Modelo del Mundo es la memoria y la imaginación del sistema de control. Tiene dos componetes que trabajan juntos:
El log de eventos registra lo que realmente pasó, y el predictor estima lo que debería pasar basándose en ese historial.

La base científica es el Principio de Energía Libre de Karl Friston(2010[mi gran amigo que nunca he conocido :smile:]), que postula que el cerebro no es un receptor pasivo de información sino un generador activo de preducciones. En cada momento, el cerebro tiene un modelo del mundo que predice qué debería estar sintiendo. La diferencia entre lo predicho y lo percibido -el error de predicción(como en los PID)- es la señal de aprendizaje más poderosa del sistema nervioso.

El sistema implementa esta predicción mediante promedio móvil exponencial, que pondera más los eventos recientes que los antiguos sin necesitar almacenar todo el historial(¿si ya hace mucho hubo un terremoto, pero ayer no, porqué debería estar prediciendo que ocurrirá uno en este momento?). Bien, eso dependerá de cómo lo hallamos configurado en el ADN(a), pues, siempre se puede ser paranóico en casos específicos, la idea es que el sistema sirva para cualquier sistema de control, sin más que decir por ahora... He aquí la fórmula:

<pre>
predicción(t) = a * valor(t-1) + (1-a) * prediccion(t-1)
</pre>
> a E(0,1) - Valores altos priorizan el presente, valores bajos priorizan el historial.

Si la fórmula te pareció ilegible, no te preocupes, el conocimiento es para compartir, no para esconder... Aquí tienes la misma en el idioma de los humanos(como yo :smile:).

<pre>
prediccion = 0.2 * (lo_que_paso_ayer) + 0.8 * (toda_mi_experienca)
</pre>

> Como puedes ver claramente si le das mas peso a lo que paso ayer que a toda la experiencia, el sistema aprende rápido pero también olvida rápido. Y si haces lo contrario, pues pasa lo opuesto, el sistema es mas estable pero tarda más para detectar cambios reales en el entorno. Capisci?

El error de predicción es la señal que alimenta la Motivación. Un error alto no solo indica que algo inesperado ocurrió, indica que el modelo del mundo era incorrecto y necesita actualizarse. Eso es Aprendizaje: Cada ciclo, el sistema de control ajusta su modelo para predecir mejor el siguiente.

> Los datos se promedian en ventanas diarias para construir el historial a largo plazo.
---
> El cerebro es una máquina de predicción. Sus sensaciones no son datos crudos del mundo - Son el residuo entre lo que esperaba y lo que encontró.<br><br>
-Karl Friston, The free-energy principle: a unified brain theory, Nature Reviews Neurosciense, 2010.

El log de eventos almacena tuplas estructuradas que permiten consultas durante el estado de Displacer:

<pre>
evento = (timestap, sensor, valor, emoción, acción_tomada, error_prediccion)
</pre>

Los valores afectivos(activación y valencia) permiten al sistema consultar su historial, no solo por valor de sensor sino por el estado emocional. Durante el Displacer prolongado, el Modelo del Mundo puede buscar en el log momentos anteriores con valencia negativa similar y comprarar que acciones fueron efectivas entonces. Esa es la base del aprendizaje por experiencia emocional: No es sólo recordar qué paso, sino recordar como se "sentía" el sistema cuando pasó y que funcionó para salir de ese estado.

---


### 4.5 Quinta etapa - Motivación
La Motivación es la etapa que convierte el estado emocional en acción. Recibe las dos coordenadas del plano circumplejo y produce dos outputs: La "Intensidad" de la acción y la "Dirección" de la acción.

La "Intensidad" la determina la Activación. Un sistema muy activado actua con mucha energía. Un sistema relajado actúa con energía mínima o no actúa. La activación es el acelerador.

La "Dirección" la determina la valencia. Valencia positiva produce comportamiento de aproximacón (el sistema refuerza y mantiene lo que está haciendo, porque el estado es faborable). Valencia negativa produce comportamiento de evitación (el sistema busca cambiar el estado actual porque es desfavorable).

La fórmula de motivación integra ambas variables con el error de predicción del Modelo del Mundo y los pesos del ADN:
<pre>
* Intensidad_motivación = peso_motivación * activacion(t) * [1 + (error_predicción)]

* Direccion_motivación = signo(valencia(t))
    -> +1 aproximación(reforzar estado actual)
    -> -1 evitación(cambiar estado actual)

* Motivación = intensidad_motivación * dirección_motivación
</pre>

>*Motivación E[-1.0, +1.0]<br>
-Valores positivos -> el sistema actúa para mantener o acercarse al estado actual<br>
-Valores negativos -> el sistema actúa para alejarse del estado actual.<br>
La magnitud determina cuánta energía aplica a esa acción.

El error de predicción amplifica la motivación: Si el Modelo del Mundo predijo que la temperatura estaría a 23°C y en realidad está a 29°C, el error es alto y la motivación se amplifica proporcionalmente. El sistema actúa con más urgencia cuanto más inesperado fué el estado(exactamente como lo describe la señal dopaminérgica se Schultz, Dayan y Montague(1997)): La neurona no responde a la magnitud del evento sino a la diferencia entre lo esperado y lo ocurrido.

La combinación de estos cuatro cuadrantes del plano circumplejo produce cuatro patrones de contucta naturales del sistema:

| Posición en el plano | ___ | Conducta |
|---|---|---|
|Alta activación + Valencia positiva|->|Acción de mantenimiento nergético. El sistema está "bien" y pone energía en seguir así|
|Alta activación + Valencia negativa|->| Acción de corrección urgente. El sistema está "mal" y actúa con toda su energía para cambiar|
|Baja activación + Valencia positiva|->|Reposo activo. El sistema está "bien" y reduce su actividad al mínimo|
|Baja activación + Valencia negativa|->|Exploración de alternativas. El sistema esta "mal" pero sin urgencias. Consulta el historial buscando que funcionó en situaciones similares.|

Éste último cuadrante(Baja activación con valencia negativa) es el más interesante desde el punto de vista del aprendizaje. Es el estado en el que el sistema tiene tiempo y razón para revisar su historia, actualizar su modelo del mundo, y ajustar su estrategia sin la presión de una emergencia activa. En biología, ese estado corresponde aproximadamente al procesamiento de memoria durante el sueño ligero: El organismo no está en peligro, pero tampoco está en su mejor estado, y usa esa tensión suave para consolidar lo aprendido.

> La dopamina no codifica el placer. Codifica la predicción del placer. Y cuando la predicción falla -en cualquier dirección- codifica el aprendizaje.<br>
-Wolfram Schultz, Peter Dayan, P. Read Montague, A neural Substrate of Prediction and Reward, Science, 1997.

#### Porqué este modelo de emociones no tiene precedente directo
Los sistemas de control industrial no tienen emociones. Los sistemas de IA que sí modelan estados afectivos -como los agentes de reinforcement learning con funciones de recompensa- operan sobre escalares unidimensionales: La recompensa es un número, más alto es mejor. No tienen unplano bidimensional con activación y valencia independientes.

Los modelos computacionales del afecto que sí usan el espacio bidimensional de Russell existen en psicología computacional y en síntesis de comportamiento de prsonajes virtuales para videojuegos y simulaciones. Pero ninguno de esos sistemas está conectado a hardware físico real, ni usa las emociones como mecanismo de control de actuadores, ni las configura desde un ADN externo que puede cambiar sin tocar el código.

Lo que este sistema hace -usar el modelo circumplejo como mecanismo de control de un organismo hecho con hardware físico real, configurable desde datos- no está documentado en ningún sistema de control conocido. Y esa conexión específica, hasta donde se puede verificar, no existe implementada en ningún otro lugar(Ni aún en este sistema se ha testeado...).

## 5. Los tres fallos conocidos en esta arquitectura
> En desarrollo... :smile:

