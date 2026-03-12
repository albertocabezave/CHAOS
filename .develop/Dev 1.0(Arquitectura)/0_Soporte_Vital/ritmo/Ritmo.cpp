/**
* @file Ritmo.cpp
* @brief Implmentación del Tallo Cerebral - Gestión de precisión temporal.
* @author Alberto Cabeza (Arquitecto de Sistemas)
*/

#include "Ritmo.hpp"
#include <thread> // Para std::this_thread::sleep_for

namespace Nucleo {
    Ritmo::Ritmo(double hercios)
    : m_delta_tiempo(0.0),
    m_contador_ciclos(0)
    {
        // Calculamos la duración de un latido en segundos (1/Hz)
        m_duracion_objetivo = std::chrono::duration<double>(1.0 / hercios);

        // Inicializamos los cronómetros al tiempo actual
        m_punto_inicio_sistema = std::chrono::steady_clock::now();
        m_punto_ultimo_latido = m_punto_inicio_sistema;
    }

    bool Ritmo::esperarSiguienteLatido() {
        auto ahora = std::chrono::steady_clock::now();

        // Calculamos cuanto tiempo ha pasado dedsde el inicio del ultimo ciclo
        auto tiempo_consumido = ahora - m_punto_ultimo_latido;

        // Si terminamos el trabajo antes del tiempo ojetivo, entramos en estado de reposo.
        if (tiempo_consumido < m_duracion_objetivo) {
            std::this_thread::sleep_for(m_duracion_objetivo - tiempo_consumido);
        }

        // Actualizamos el punto de tiempo oficial del latido actual
        auto punto_final_latido = std::chrono::steady_clock::now();

        // Calculamos el Delta Tiempo real(debe ser muy cercano a 1/Hz)
        std::chrono::duration<double> delta = punto_final_latido - m_punto_ultimo_latido;
        m_delta_tiempo = delta.count();

        // Actualizamos contenedores de estado
        m_punto_ultimo_latido = punto_final_latido;
        m_contador_ciclos++;
        
        return true;
    }

    double Ritmo::obtenerDeltaTiempo() const {
        return m_delta_tiempo;
    }

    uint64_t Ritmo::obtenerTiempoTotalMicro() const {
        auto ahora = std::chrono::steady_clock::now();

        // Calculamos la diferencia total desde que el sistema "despertó".
        return std::chrono::duration_cast<std::chrono::microseconds>
        (ahora - m_punto_inicio_sistema).count();
    }

    uint64_t Ritmo::obtenerContadorCiclos() const {
        return m_contador_ciclos;
    }
} // namespace Nucleo