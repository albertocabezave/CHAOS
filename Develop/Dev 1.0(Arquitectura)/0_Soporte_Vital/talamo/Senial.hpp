/**
* @file Senial.hpp
* @brief Definición de la estructura de datos sensoriales.
*/

#ifndef NUCLEO_SENIAL_HPP
#define NUCLEO_SENIAL_HPP

#include <cstdint>

namespace Nucleo {
    /**
    * @enum EstadoSenial
    * @brief Define la calidad del dato recibido.
    */

    enum class EstadoSenial : uint8_t {
        NOMINAL, // Dato Confiable
        URGENTE, // Dato fuera de rango (Peligro)
        RUIDO, // Dato incoherente
        SORDERA // No hay señal del sensor
    };

    /**
    * @struct PulsoSensorial
    * @brief El paquete de información que viaja por los nervios.
    */
    struct PulsoSensorial {
        uint32_t id_nervio; // Identificador del sensor
        float valor; // Valor físico (Temp, etc.)
        uint64_t marca_tiempo_micro; // Marca el tiempo del ritmo.
        bool activo; // Estado del hardware
    };
} // namespace Nucleo

#endif