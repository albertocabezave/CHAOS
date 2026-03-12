#include "Talamo.hpp"
#include <iostream>
#include <vector>

using namespace Nucleo;

/**
* Funcion auxiliar para imprimir el resultado de forma bonita
*/
void reportarResultado(const std::string& prueba, EstadoSenial resultado) {
    std::cout << "Prueba: " << prueba << " -> ";
    switch(resultado) {
        case EstadoSenial::NOMINAL: std::cout << "[NOMINAL]";
        break;
        case EstadoSenial::URGENTE: std::cout << "[URGENTE]";
        break;
        case EstadoSenial::RUIDO: std::cout << "[RUIDO - BASURA]";
        break;
        case EstadoSenial::SORDERA: std::cout << "[SORDERA - HARDWARE]";
        break;
    }
    std::cout << std::endl;
}
int main() {
    Talamo mi_talamo;
    PulsoSensorial mi_pulso;
    mi_pulso.id_nervio = 1;
    mi_pulso.marca_tiempo_micro = 0;

    std::cout << "=== INICIANDO TEST DE ESTRÉS DEL TÁLAMO ===" << std::endl;

    // --- PRUEBA 1: EL LÍMITE DE LA NORMALIDAD ---
    mi_pulso.valor = 37.9f; // Casi FIEBRE
    mi_pulso.activo = true;
    reportarResultado("37.9 grados(Límite nominal)",
    mi_talamo.clasificarSenial(mi_pulso));

    // --- PRUEBA 2: EL SALTO A LA URGENCIA ---
    mi_pulso.valor = 38.1f; // FIEBRE
    reportarResultado("38.1 grados (Entrada a Urgencia)",
    mi_talamo.clasificarSenial(mi_pulso));

    // --- PRUEBA 3: RUIDO POR EXCESO ---
    mi_pulso.valor = 100.1f; // Imposible para una codorniz.
    reportarResultado("100.1 grados (Ruido superior)",
    mi_talamo.clasificarSenial(mi_pulso));

    // --- PRUEBA 4: RUIDO POR DEFECTO ---
    mi_pulso.valor = -1.0f; // Congelación imposible.
    reportarResultado("-1.0 grados (Ruido inferior)",
    mi_talamo.clasificarSenial(mi_pulso));

    // --- PRUEBA 5: FALLO DE HARDWARE ---
    mi_pulso.valor = 25.0f; // Valor normal.
    mi_pulso.activo = false; // ...pero el sensor se desconectó.
    reportarResultado("Sensor desconectado: ",
    mi_talamo.clasificarSenial(mi_pulso));

    // --- PRUEBA 6: TEST DE SORDERA (TIEMPO) ----
    uint64_t ahora = 5000000; // 5 segundos después
    uint64_t ultimo =2000000; //El sesor habló hace 3 segundos
    bool sordo = mi_talamo.detectarSordera(ultimo, ahora);

    std::cout << "Prueba: Silencio de 3 segundos -> " <<
    (sordo ? "[SORDERA DETECTADA]":"[TODO BIEN]") <<
     std::endl;

     std::cout << "============================================" << std::endl;
     return 0;
}