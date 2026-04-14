# Calc_dosador_concreto

#  Calculadora de Traço de Concreto -  Método ABCP

Aplicativo desktop desenvolvido em Python (Tkinter) que calcula o traço de concreto conforme o método da Associação Brasileira de Cimento Portland (ABCP).

##  Funcionalidades
- Entrada de Fck (MPa) e abatimento (slider com classificação dinâmica)
- Escolha do tipo de cimento (CP II, CP III, CP IV, CP V-ARI)
- Escolha da brita (0, 1 ou 2) e tipo de areia (fina, média, grossa)
- Cálculo automático do consumo de materiais por m³
- Traço prático para 1 saco de cimento (50 kg), com equivalência em baldes
- Interface intuitiva e botões de ajuda explicativos

##  Como executar
1. Clone o repositório
2. Execute `python dosador_concreto.py` (requer Python 3.6+ com Tkinter)

## Fundamentação teórica
Baseado nas tabelas e curvas do método ABCP, NBR 12655 e curvas de Abrams, com ajustes para diferentes agregados.

