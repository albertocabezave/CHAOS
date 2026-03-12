## Documentación del Schema Maestro ADN CHAOS v1.5

### 1. Introducción

El **Schema Maestro** es la piedra angular de la arquitectura CHAOS. Actúa como la **gramática universal** que define cómo se construye el ADN de cualquier “especie” (sistema de control) que el motor SOMA pueda interpretar y ejecutar. Es un archivo JSON Schema que valida la estructura y los tipos de datos del ADN, garantizando que el motor reciba una configuración coherente y libre de errores básicos.

Este documento describe en detalle cada componente del schema, explica su propósito, las validaciones que impone y cómo se relaciona con los principios de la arquitectura (ciclo dual, emociones, reflejos, etc.). Además, señala aspectos que deben ser considerados en futuras fases del desarrollo para mantener la robustez y evolucionar el sistema.

---

### 2. Visión general del esquema

El schema define un objeto JSON con las siguientes propiedades obligatorias:

- `schema_version`
- `especie`
- `sensores`
- `actuadores`
- `reflejos`
- `ciclos`

Adicionalmente, incluye propiedades opcionales pero recomendadas: `metadata`, `debug`, `logs`. La raíz tiene `"additionalProperties": false`, lo que impide la presencia de campos no definidos, evitando errores por nombres mal escritos.

---

### 3. Descripción detallada de cada propiedad

#### 3.1 `schema_version` (string, obligatorio)

- **Patrón**: `^1\.[0-9]+$` (versión 1.x)
- **Descripción**: Indica la versión del schema que utiliza este ADN. Permite que el motor SOMA mantenga compatibilidad hacia atrás: si en el futuro se crea una versión 2.0, el motor podrá leer ADNs antiguos si reconoce la versión.
- **Ejemplo**: `"1.5"`

#### 3.2 `metadata` (objeto, opcional)

Contiene información descriptiva sobre el ADN. No afecta la ejecución, pero es útil para trazabilidad.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `autor` | string | Creador del ADN. |
| `fecha_creacion` | string (formato date) | Fecha de creación (YYYY-MM-DD). |
| `version` | string | Versión del ADN (ej. "1.0.0"). |
| `comentarios` | string | Notas adicionales. |

**Restricción**: No se permiten otras propiedades dentro de `metadata` (`additionalProperties: false`).

#### 3.3 `debug` (objeto, opcional)

Configura el comportamiento del motor en cuanto a logs y modo de operación.

| Campo | Tipo | Valores | Default | Descripción |
|-------|------|---------|---------|-------------|
| `nivel_log` | string | `"debug"`, `"info"`, `"warn"`, `"error"` | `"info"` | Nivel de detalle de los mensajes de log. |
| `modo_operacion` | string | `"normal"`, `"test"`, `"simulacion"` | `"normal"` | Permite ejecutar el sistema en modo test (sin hardware) o simulación. |
| `traza_eventos` | boolean | `true`/`false` | `false` | Si es `true`, el motor registrará trazas detalladas de cada ciclo (útil para depuración). |

#### 3.4 `especie` (objeto, obligatorio)

Define la identidad del sistema de control. Aunque no interviene directamente en la lógica, ayuda a contextualizar.

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `nombre` | string | Sí | Nombre de la especie (ej. "Codorniz ROBUSTO'S"). |
| `industria` | string | Sí | Sector de aplicación (ej. "avícola", "robótica"). |
| `tipo` | string | Sí | Subtipo o raza (ej. "coturnix"). |
| `descripcion` | string | No | Texto libre explicativo. |

#### 3.5 `sensores` (objeto, obligatorio)

Es un objeto cuyas claves son los **nombres de los sensores** (identificadores únicos). Cada clave debe cumplir el patrón `^[a-zA-Z][a-zA-Z0-9_]*$` (empieza con letra, luego letras, números o guiones bajos). El valor asociado es un objeto con las siguientes propiedades **obligatorias**:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `tipo` | string | Tipo de sensor (libre, ej. `"temperatura"`, `"humedad"`, `"presion"`). |
| `unidad` | string | Unidad de medida (libre, ej. `"celsius"`, `"porcentaje"`). |
| `rango_operativo` | array [número, número] | Rango físico que el sensor puede medir [mín, máx]. |
| `rango_optimo` | array [número, número] | Rango ideal para el organismo [mín, máx]. |
| `umbral_estres` | array [número, número] | Límites a partir de los cuales se considera estrés [mín, máx]. |
| `critico` | boolean | `true` si el sensor debe ser monitoreado por el ciclo reptil (alta frecuencia). |
| `peso_atencion` | número (0.0 a 1.0) | Peso para el cálculo de prioridad en la etapa de atención. |
| `ubicacion` | string (opcional) | Lugar donde está instalado el sensor. |
| `descripcion` | string (opcional) | Descripción adicional. |

**Notas**:
- Los rangos (`rango_operativo`, `rango_optimo`, `umbral_estres`) siempre tienen exactamente dos números.
- El motor deberá verificar que `rango_optimo` esté contenido dentro de `rango_operativo`, y que `umbral_estres` sea exterior o coincidente con los límites del rango óptimo (esto es lógica de negocio, no validación del schema).

#### 3.6 `actuadores` (objeto, obligatorio)

Similar a `sensores`, las claves son nombres de actuadores. Cada actuador tiene:

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `tipo` | string | Sí | Tipo de actuador (libre, ej. `"ventilador"`, `"motor"`). |
| `estado_inicial` | string, number, boolean o null | Sí | Valor que tendrá el actuador al arrancar el sistema. |
| `valores_posibles` | array de (string, number, boolean) | Sí | Conjunto de valores que el actuador puede aceptar. |
| `ubicacion` | string | No | Ubicación física. |
| `descripcion` | string | No | Descripción. |
| `potencia` | número | No | Potencia nominal (para cálculos energéticos futuros). |
| `tiempo_respuesta` | número | No | Tiempo característico de respuesta (ms). |

**Importante**: El motor deberá validar que `estado_inicial` esté incluido en `valores_posibles` (si no es null). Además, las acciones de los reflejos deben ser compatibles con estos valores.

#### 3.7 `reflejos` (array, obligatorio)

Lista de reflejos que ejecutará el ciclo reptil. Cada reflejo es un objeto con:

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `nombre` | string | Sí | Identificador del reflejo. |
| `sensor` | string | Sí | Nombre del sensor que dispara el reflejo (debe existir en `sensores`). |
| `operador` | string | Sí | Operador de comparación: `">"`, `"<"`, `">="`, `"<="`, `"=="`. |
| `umbral` | número | Sí | Valor umbral para la comparación. |
| `actuador` | string | Sí | Nombre del actuador a controlar. |
| `accion` | string, number, boolean | Sí | Valor a escribir en el actuador cuando se cumple la condición. |
| `histeresis` | número (≥0) | Sí | Banda muerta para evitar oscilaciones (en las mismas unidades que el sensor). |
| `tiempo_bloqueo` | número (≥0) | Sí | Tiempo mínimo entre activaciones sucesivas de este reflejo (en milisegundos). |
| `prioridad` | entero (≥1) | Sí | Prioridad del reflejo (menor = más prioritario). En caso de empate, se usa el orden en el array. |
| `descripcion` | string | No | Descripción del reflejo. |

**Validaciones semánticas que debe hacer el motor**:
- El `sensor` debe estar definido en el objeto `sensores` y tener `critico: true` (aunque no es obligatorio en el schema, es lógico).
- El `actuador` debe existir.
- La `accion` debe ser uno de los `valores_posibles` del actuador.
- El `umbral` y la `histeresis` deben ser coherentes con el rango del sensor.

#### 3.8 `ciclos` (objeto, obligatorio)

Configuración de los dos ciclos de procesamiento. Contiene dos subobjetos: `reptil` y `cognitivo`.

##### 3.8.1 `ciclos.reptil`

| Campo | Tipo | Obligatorio | Default | Descripción |
|-------|------|-------------|---------|-------------|
| `frecuencia_hz` | número (1-1000) | Sí | (ninguno) | Frecuencia de ejecución del ciclo reptil en Hz. |
| `prioridad_hilo` | string | No | `"maxima"` | Prioridad del hilo a nivel de sistema operativo. Valores: `"maxima"`, `"alta"`, `"normal"`, `"baja"`. |

##### 3.8.2 `ciclos.cognitivo`

| Campo | Tipo | Obligatorio | Default | Descripción |
|-------|------|-------------|---------|-------------|
| `frecuencia_hz` | número (0.1-60) | Sí | (ninguno) | Frecuencia del ciclo cognitivo. |
| `factor_decaimiento_activacion` | número (0.0-1.0) | No | 0.7 | Inercia del eje de activación emocional entre ciclos. |
| `factor_decaimiento_valencia` | número (0.0-1.0) | No | 0.7 | Inercia del eje de valencia emocional. |
| `umbral_activacion_por_error` | número (0.1-2.0) | No | 1.0 | Sensibilidad del sistema al error (amplifica la activación). |
| `peso_motivacion` | número (0.1-2.0) | No | 1.0 | Peso global de la motivación. |
| `factor_prediccion` | número (0.0-1.0) | No | 0.2 | Factor alfa para el promedio móvil exponencial del modelo del mundo. 0 = solo histórico, 1 = solo último valor. |
| `prioridad_hilo` | string | No | `"normal"` | Prioridad del hilo cognitivo. |

**Nota**: El motor debe respetar estas prioridades en la medida que el sistema operativo lo permita (en Python solo es una sugerencia, pero en C++ con RTOS se puede mapear a prioridades reales).

#### 3.9 `logs` (objeto, opcional)

Configuración del sistema de logs orgánicos (el historial de eventos del sistema).

| Campo | Tipo | Valores | Default | Descripción |
|-------|------|---------|---------|-------------|
| `nivel_detalle` | string | `"minimo"`, `"importante"`, `"completo"` | `"importante"` | Nivel de detalle de los logs almacenados. |
| `formato_timestamp` | string | `"unix"`, `"iso8601"` | `"unix"` | Formato de los timestamps en los logs. |
| `retencion_dias` | entero (≥1) | - | 30 | Días que se conservarán los logs antes de ser purgados. |

---

### 4. Validaciones y restricciones importantes

- **Tipos fuertes**: Cada campo tiene tipos claramente definidos. El motor debería usar una librería de validación JSON Schema (como `jsonschema` en Python) para verificar el ADN al cargarlo.
- **Ausencia de propiedades extra**: Gracias a `"additionalProperties": false` en todos los niveles, se previenen errores por campos mal escritos.
- **Patrones de nombres**: Los nombres de sensores y actuadores siguen una convención (letras, números y guiones bajos), lo que facilita su uso como identificadores en el código.
- **Valores por defecto**: Algunos campos tienen valores por defecto definidos en el schema. El motor debe aplicarlos si el ADN no los proporciona.

---

### 5. Relación con la arquitectura

Cada parte del schema refleja directamente los conceptos de la arquitectura CHAOS:

- **Ciclo reptil**: Los sensores marcados como `critico` y la lista de `reflejos` con histéresis y tiempo de bloqueo materializan la lógica de supervivencia inmediata.
- **Ciclo cognitivo**: Los parámetros como `factor_decaimiento_*`, `peso_motivacion`, `factor_prediccion` permiten ajustar la "personalidad" del sistema (cómo siente, aprende y decide).
- **Emociones**: Aunque el schema no define explícitamente el plano circumplejo, los factores de decaimiento y el peso de atención son los insumos para calcular activación y valencia.
- **Universalidad**: Al dejar libres los tipos de sensores y actuadores, el schema permite modelar cualquier industria (solo se necesita que el motor sepa interpretar esos tipos).
- **Separación ADN/SOMA**: Toda la configuración está en el ADN; el motor no tiene valores hardcodeados.

---

### 6. Consideraciones para futuras fases del desarrollo

#### 6.1 Durante la implementación en Python (Fase 1)

- **Validación**: Usa la librería `jsonschema` para validar el ADN al iniciar el motor. Esto te ahorrará horas de depuración.
- **Manejo de errores**: Si el ADN es inválido, el motor debería detenerse con un mensaje claro indicando qué campo falla.
- **Valores por defecto**: Implementa la lógica para aplicar los defaults definidos en el schema (especialmente en `ciclos` y `logs`).
- **Consistencia interna**: Además de la validación del schema, el motor debe realizar comprobaciones semánticas:
  - Que los sensores referidos en reflejos existan.
  - Que los actuadores referidos existan.
  - Que `accion` esté dentro de `valores_posibles`.
  - Que los rangos sean coherentes (`rango_optimo` ⊆ `rango_operativo`, `umbral_estres` fuera de `rango_optimo` o en los bordes).
  - Que `critico` sea `true` para los sensores usados en reflejos (opcional pero recomendable).
- **Frecuencias realistas**: Aunque el schema permite hasta 1000 Hz en el ciclo reptil, en Python es difícil superar 100 Hz con garantías. Considera añadir una advertencia si se configura una frecuencia muy alta.

#### 6.2 De cara a la migración a C++/RTOS (Fase 3)

- El schema actual es independiente del lenguaje, por lo que no necesitará cambios. Sin embargo, el motor en C++ deberá implementar las mismas validaciones.
- La propiedad `prioridad_hilo` cobrará verdadero significado en un sistema con hilos POSIX. Se debe mapear a valores de prioridad real (ej. `sched_setscheduler`).
- El campo `tiempo_bloqueo` en milisegundos deberá convertirse a ticks o tiempos del RTOS.

#### 6.3 Posibles extensiones futuras

- **Asimetría en atención**: En versiones posteriores, se podría ampliar `peso_atencion` para permitir pesos diferenciados por exceso y defecto.
- **Tipos de actuadores más complejos**: Para robots, las acciones podrían ser trayectorias, no valores simples. Habría que extender `accion` y `valores_posibles` para aceptar objetos estructurados.
- **Múltiples niveles de procesamiento**: Si se introduce un tercer ciclo (ej. límbico), el schema debería ampliarse con una nueva sección en `ciclos`.
- **Aprendizaje de pesos**: Si el motor aprende y ajusta los pesos del ADN, habría que definir cómo se persisten esos cambios (¿sobrescribir el ADN?).

#### 6.4 Aspectos no cubiertos por el schema que debe manejar el motor

- **Comunicación con hardware**: El schema no especifica cómo se conectan los sensores y actuadores. Eso es responsabilidad del motor (lectura/escritura de archivos, bus, etc.).
- **Condiciones de carrera**: El schema no puede prevenir problemas de concurrencia; el motor debe implementar mecanismos como `estado_reptil` y file locking.
- **Watchdog y supervisión**: El schema no incluye configuraciones para la supervisión externa del motor; deberán añadirse en el futuro si se requiere redundancia.

---

### 7. Ejemplo mínimo de un ADN válido

```json
{
  "schema_version": "1.5",
  "especie": {
    "nombre": "Codorniz ROBUSTO'S",
    "industria": "avícola",
    "tipo": "coturnix"
  },
  "sensores": {
    "temp_ambiente": {
      "tipo": "temperatura",
      "unidad": "celsius",
      "rango_operativo": [0, 50],
      "rango_optimo": [18, 24],
      "umbral_estres": [10, 35],
      "critico": true,
      "peso_atencion": 0.8
    },
    "humedad": {
      "tipo": "humedad",
      "unidad": "porcentaje",
      "rango_operativo": [0, 100],
      "rango_optimo": [50, 70],
      "umbral_estres": [30, 85],
      "critico": false,
      "peso_atencion": 0.3
    }
  },
  "actuadores": {
    "ventilador": {
      "tipo": "ventilador",
      "estado_inicial": "OFF",
      "valores_posibles": ["OFF", "ON"]
    },
    "extractor": {
      "tipo": "extractor",
      "estado_inicial": "OFF",
      "valores_posibles": ["OFF", "ON"]
    }
  },
  "reflejos": [
    {
      "nombre": "sobrecalentamiento",
      "sensor": "temp_ambiente",
      "operador": ">=",
      "umbral": 38,
      "actuador": "ventilador",
      "accion": "ON",
      "histeresis": 1.0,
      "tiempo_bloqueo": 60000,
      "prioridad": 1
    }
  ],
  "ciclos": {
    "reptil": {
      "frecuencia_hz": 100
    },
    "cognitivo": {
      "frecuencia_hz": 1,
      "factor_decaimiento_activacion": 0.8,
      "factor_prediccion": 0.15
    }
  },
  "logs": {
    "nivel_detalle": "importante",
    "retencion_dias": 15
  }
}
```

---

### 8. Conclusión

El Schema Maestro v1.5 es una pieza clave que garantiza que el ADN de cualquier sistema de control CHAOS sea válido, comprensible y extensible. Su diseño cuidadoso, con tipos estrictos y propiedades bien definidas, reduce errores y facilita el desarrollo del motor SOMA. Con la documentación aquí proporcionada, tienes un mapa mental completo para transcribirlo, implementarlo y mantenerlo en el futuro.

Recuerda que el schema es solo el contrato; el motor debe respetarlo y complementarlo con validaciones semánticas y lógica de negocio. A medida que el sistema evolucione, este documento servirá como referencia para introducir cambios de forma controlada.