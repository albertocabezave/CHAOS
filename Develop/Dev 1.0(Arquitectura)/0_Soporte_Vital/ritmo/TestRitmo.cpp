#include "Ritmo.hpp"
#include <iostream>
#include <vector>
#include <numeric>
#include <thread>
#include <iomanip>

int main() {
    const double frecuencia_objetivo = 60.0; // 60 latidos por segundo.
    const double delta_ideal = 1.0 / frecuencia_objetivo;
    const int total_ciclos = 600; // 10 segundos de prueba.

    Nucleo::Ritmo corazon(frecuencia_objetivo);
    std::vector<double> deltas;

    std::cout << "======================================================\n";
    std::cout << "INICIANDO PRUEBA DE ESTABILIDAD DE RITMO (60Hz)  \n";
    std::cout << "======================================================\n";
    std::cout << "Tiempo total micro al despertar: " << corazon.obtenerTiempoTotalMicro() <<
    "us\n\n";

    for (int i = 0;  i < total_ciclos; ++i) {
        // --- SIMULACIÓN DE CARGA DE TRABAJO ---
        // Simulamos que el sistema procesa sensores (tarda un poco)
        std::this_thread::sleep_for(std::chrono::milliseconds(5));

        // El corazón debe compensar esos 5ms para que el latido sea exacto.
        corazon.esperarSiguienteLatido();

        double dt = corazon.obtenerDeltaTiempo();
        deltas.push_back(dt);

        if (i % 60 == 0) {
            std::cout << "Latido [" << std::setw(3) << i << "] -> Delta: " << std::fixed <<
            std::setprecision(6) << dt << " s (objetivo: " << delta_ideal << ")\n";
        }
    }

    // Análisis de resultados
    double suma = std::accumulate(deltas.begin(), deltas.end(), 0.0);
    double promedio = suma / deltas.size();
    uint64_t tiempo_final = corazon.obtenerTiempoTotalMicro();

    std::cout << "\n===================================================\n";
    std::cout << " RESULTADOS DEL ANÁLISIS                 \n";
    std::cout << "====================================================\n";
    std::cout << "Ciclos totales: " << corazon.obtenerContadorCiclos() << "\n";
    std::cout << "Tiempo total:  " << (double)tiempo_final / 1000000.0 << " s\n";

    // Si el promedio se desvía por mas de un 1%, el sistema no es robusto.
    if(std::abs(promedio -delta_ideal) < 0.001) {
        std::cout << "ESTADO: [SISTEMA ESTABLE Y SINCRONIZADO] \n";
    } else {
        std::cout << "ESTADO: [DERIVA TEMPORAL DETECTADA]\n";
    }
    std::cout << "=====================================================\n";

    return 0;
}