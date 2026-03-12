/**
 * @file Talamo.cpp
 * @brief Implementación del filtro sensorial (Tálamo) del organismo.
 * * Este componente actúa como la primera frontera de procesamiento, 
 * clasificando las señales antes de que lleguen a los centros de decisión.
 */

#include "Talamo.hpp"

namespace Nucleo {

/**
 * @brief Constructor por defecto.
 */
Talamo::Talamo() {
    // Inicialización de componentes internos si fuera necesario en el futuro.
}

/**
 * @brief Clasifica un pulso sensorial según su integridad y valor.
 * * Jerarquía de filtrado:
 * 1. Estado del Hardware (Sordera)
 * 2. Límites de Realidad Física (Ruido)
 * 3. Umbrales de Seguridad Biológica (Urgencia)
 * 4. Estado Saludable (Nominal)
 */
EstadoSenial Talamo::clasificarSenial(const PulsoSensorial& pulso) {
    
    // --- REGLA 1: ESTADO DEL HARDWARE ---
    // Si el sensor reporta estar inactivo, ignoramos cualquier valor.
    if (!pulso.activo) {
        return EstadoSenial::SORDERA;
    }

    // --- REGLA 2: FILTRO DE RUIDO ---
    // Valores fuera del rango biológico posible (0°C a 100°C).
    // Se procesa ANTES que la urgencia para evitar falsas alarmas por sensores locos.
    if (pulso.valor < 0.0f || pulso.valor > 100.0f) {
        return EstadoSenial::RUIDO;
    }

    // --- REGLA 3: UMBRAL CRÍTICO (URGENCIA) ---
    // Si la temperatura supera los 38°C, el sistema debe reaccionar de inmediato.
    if (pulso.valor > 38.0f) {
        return EstadoSenial::URGENTE;
    }

    // --- ESTADO FINAL: NOMINAL ---
    // Si pasó todos los filtros anteriores, el dato es confiable y seguro.
    return EstadoSenial::NOMINAL;
}

/**
 * @brief Detecta si un sensor ha dejado de enviar datos (Sordera temporal).
 * @param ultimo_update Marca de tiempo del último pulso recibido.
 * @param tiempo_actual Tiempo actual del sistema.
 * @return true si el silencio supera el UMBRAL_SORDERA_MICRO.
 */
bool Talamo::detectarSordera(uint64_t ultimo_update, uint64_t tiempo_actual) {
    // Calculamos la brecha de silencio
    uint64_t tiempo_sin_noticias = tiempo_actual - ultimo_update;

    // Comparamos con el umbral definido en el archivo de cabecera (.hpp)
    return (tiempo_sin_noticias > UMBRAL_SORDERA_MICRO);
}

} // namespace Nucleo