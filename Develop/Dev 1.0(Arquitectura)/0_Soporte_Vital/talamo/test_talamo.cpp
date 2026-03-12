#include "Talamo.hpp"
#include <iostream>
#include <cassert>

using namespace Nucleo;

int main() {

   Talamo mi_talamo;

   PulsoSensorial mi_pulso;

   mi_pulso.valor = 25.5f;
   mi_pulso.activo = true;

   std::cout << "Pulso: " << mi_pulso.valor << "Activo?: " 
   << mi_pulso.activo
   << std::endl;

    EstadoSenial informe = mi_talamo.clasificarSenial(mi_pulso);

    if(informe == EstadoSenial::NOMINAL) {
        std::cout << "El Tálamo dice que la señal es NOMINAL, así que todo esta BIEN :)" <<
        std::endl;
    }

    return 0;
}