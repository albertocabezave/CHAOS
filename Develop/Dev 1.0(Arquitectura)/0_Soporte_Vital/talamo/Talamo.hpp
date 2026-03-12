/**
* @file Talamo.hpp
* @brief Contrato del Tálamo - El Conmutador Sensorial.
*/

#ifndef NUCLEO_TALAMO_HPP
#define NUCLEO_TALAMO_HPP

#include "Senial.hpp"
#include <vector>

namespace Nucleo {
    class Talamo {
        public:
        Talamo();

        /**
        * @brief Procesa un pulso entrante y determina su relevancia.
        * @param pulso El dato crudo del nervio.
        * @return EstadoSenial La clasificación del dato.
        */
        EstadoSenial clasificarSenial(const PulsoSensorial& pulso);

        /**
        * @brief Verifica si un nervio se ha quedado "mudo" por demasiado tiempo.
        * @param ultimo_update Tiempo del último pulso recibido.
        * @param tiempo_actual Tiempo actual del ritmo.
        * @return true si el nervio esta en estado de "SORDERA".
        */
        bool detectarSordera(uint64_t ultimo_update, uint64_t tiempo_actual);

        private:
        const uint64_t UMBRAL_SORDERA_MICRO = 2000000; // 2 segundos sin datos.
    };
} // namespace Nucleo

#endif