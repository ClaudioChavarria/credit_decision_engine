# Retail Credit Risk Scoring: Modelo de Probabilidad de Incumplimiento (PD)

## 1. Comprensión del Negocio (Business Understanding)

**Contexto Operativo:**
La gestión eficiente de la cartera de crédito de consumo requiere la mitigación sistemática de la Pérdida Esperada (Expected Loss). El componente fundamental de este cálculo es la Probabilidad de Incumplimiento (Probability of Default - PD), la cual debe ser cuantificada con precisión durante la originación del crédito.

**Objetivo del Modelo:**
Desarrollar y calibrar un modelo predictivo (Application Scorecard) para estimar la PD en solicitantes de crédito retail. El evento de incumplimiento (Target) se define, en alineación con los estándares del Comité de Basilea, como una obligación en mora igual o superior a 90 días dentro de un horizonte de observación de 24 meses.

**Criterios de Aceptación y Cumplimiento Normativo:**
1. **Transparencia e Interpretabilidad:** El modelo excluye metodologías de caja negra (Black-box algorithms). Se empleará transformación matemática Weight of Evidence (WoE) y modelado lineal mediante Regresión Logística para garantizar la trazabilidad de cada variable.
2. **Desempeño Estadístico:** La capacidad de discriminación del modelo será auditada prioritariamente mediante el estadístico de Kolmogorov-Smirnov (KS) y el Índice de Gini.
3. **Gobernanza:** El ciclo de vida del modelo se adhiere a los principios de gestión de riesgo de modelos (e.g., directrices SR 11-7 de la Reserva Federal), requiriendo validación de supuestos empíricos y tratamiento riguroso de la información atípica.