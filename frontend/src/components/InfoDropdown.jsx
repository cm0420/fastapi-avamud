import React, { useState } from 'react';
import { Users, Store, TrendingUp, ChevronLeft, Info } from "lucide-react";
import { Button } from "./ui/button";

export function InfoDropdown() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="flex justify-end">
      <div className="relative">
        {/* Toggle Button */}
        <Button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2"
          variant={isOpen ? "default" : "outline"}
        >
          <Info className="w-4 h-4" />
          {isOpen ? "Ocultar Informações" : "Saiba Mais Sobre Nós"}
          <ChevronLeft className={`w-4 h-4 transition-transform ${isOpen ? "rotate-90" : ""}`} />
        </Button>

        {/* Dropdown Content - Opens to the Left */}
        <div
          className={`absolute right-0 bottom-full mb-4 w-[600px] max-w-[90vw] transition-all duration-300 origin-bottom-right ${
            isOpen
              ? "opacity-100 scale-100 translate-y-0"
              : "opacity-0 scale-95 translate-y-4 pointer-events-none"
          }`}
        >
          <div className="bg-white rounded-lg shadow-xl border border-gray-200 p-6 space-y-4">
            {/* Features */}
            <div className="space-y-4">
              <div className="flex gap-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Users className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
                <div>
                  <h3 className="text-gray-900 mb-1">Organização e Representação</h3>
                  <p className="text-sm text-gray-600">
                    Representamos os interesses dos vendedores ambulantes junto aos órgãos públicos e a comunidade.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 bg-green-50 rounded-lg border border-green-100">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <Store className="w-6 h-6 text-green-600" />
                  </div>
                </div>
                <div>
                  <h3 className="text-gray-900 mb-1">Apoio aos Associados</h3>
                  <p className="text-sm text-gray-600">
                    Oferecemos suporte, orientação e recursos para que nossos associados possam desenvolver suas atividades.
                  </p>
                </div>
              </div>

              <div className="flex gap-4 p-4 bg-purple-50 rounded-lg border border-purple-100">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
                <div>
                  <h3 className="text-gray-900 mb-1">Desenvolvimento Econômico</h3>
                  <p className="text-sm text-gray-600">
                    Promovemos o crescimento econômico e a profissionalização do comércio ambulante em Diamantina.
                  </p>
                </div>
              </div>
            </div>

            {/* Mission */}
            <div className="bg-gradient-to-r from-blue-600 to-green-600 text-white p-6 rounded-lg">
              <h3 className="mb-2">Nossa Missão</h3>
              <p className="text-sm text-blue-50">
                Fortalecer o comércio ambulante em Diamantina, promovendo desenvolvimento sustentável, 
                organização e dignidade para todos os nossos associados.
              </p>
            </div>
          </div>

          {/* Arrow pointing down to button */}
          <div className="flex justify-end pr-8">
            <div className="w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-white"></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default InfoDropdown;
