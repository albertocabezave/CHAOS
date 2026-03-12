/**
* @file Ritmo.hpp
* @brief Contrato del Tallo Cerebral -Gestión de Paso Fijo (Fixed Timestap).
* * Este componente es el metrónomo del sistema. Garantiza que el ciclo de
* procesamiento se ejecute a una frecuencia constante, permitiendo que las simulaciones
* físicas y los filtros sensoriales sean deterministas.
* @author Alberto Cabeza (Arquitecto de Sistemas)
* @copyright 2026 - Organismo Digital
*/

#ifndef NUCLEO_RITMO_HPP
#define NUCLEO_RITMO_HPP

#include <cstdint> // Tipos de ancho fijo: uint64_t.
#include <chrono> // Precisión temporal de alta resolución.
#include <cmath>

/**
* @namespace Nucleo
* @brief Espacio de nombres para los componentes del sistema Vital.
*/
namespace Nucleo {
   /**
   * @class Ritmo
   * @brief Controlador del tiempo de ejecución para sistemas de tiempo real.
   */
    class Ritmo {
        public:
        /**
        * @brief Inicializa el metrónomo con una frecuencia específica.
        * @param hercios Número de ciclos por segundo(ej. 60.0).
        */
        explicit Ritmo(double hercios);

        /**
        * @brief Bloque el hilo actual hasta que se cumpla el periodo del ciclo.
        * @return true Si el latido fue exitoso y el sistema esta en sincronía.
        */
        bool esperarSiguienteLatido();

        /**
        * @brief Obtiene el tiempo transcurrido entre los últimos dos latidos.
        * @return Delta tiempo en segundos (ej. 0.01666 para 60Hz).
        */
        double obtenerDeltaTiempo() const;

        /**
        * @brief Devuelve el número total de el número total de microsegundos desde el
        * inicio del sistema.
        * @return uint64_t con el tiempo acumulado(evita desbordamiento por siglos).
        */
        uint64_t obtenerTiempoTotalMicro() const;

        /**
        * @brief Obtiene el conteo total de ciclos (latidos) realizados.
        * @return uint64_t con el número de pasos ejecutados.
        */
        uint64_t obtenerContadorCiclos() const;

        private:
        // Puntos de tiempo usando el reloj estable (steady_clock)
        std::chrono::time_point<std::chrono::steady_clock>
        m_punto_inicio_sistema;
        std::chrono::time_point<std::chrono::steady_clock>
        m_punto_ultimo_latido;

        //Configuración y estadísticas
        std::chrono::duration<double> m_duracion_objetivo;
        double m_delta_tiempo;
        uint64_t m_contador_ciclos;
    };

} // namespace Nucleo

#endif // NUCLEO_RITMO_HPP

// 1. #ifndef NUCLEO_RITMO_HPP: El nombre del guard incluye el namespace, eliminando
// cualquier posibilidad de conflicto con otras librerias que usen la clase llamada "Ritmo".

// 2. explici: Evitamos convenciones accidentales. El compilador obliga a ser claro al crear
// objetos.

// 3. uint64_t: Esto garantiza que el software pueda correr durante milenios sin que el
// contador de tiempo falle.

// 4. steady_clock: Es el único reloj que garantiza que el tiempo siempre avance, ignorando
// cambios de hora del sistema o ajustes por NTP.