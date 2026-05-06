# Proyecto de Credit Scoring: Predicción de Incumplimiento

## I. Contexto Estratégico y Descripción del Proyecto
Este proyecto desarrolla un modelo de **Credit Scoring**, el cual es un instrumento fundamental para la asignación de capital bancario. Un sistema eficiente permite diferenciar perfiles de riesgo, asegurando la rentabilidad institucional y mitigando la morosidad.

El problema de negocio principal radica en las ineficiencias generadas por modelos con baja capacidad discriminatoria:
*   **Pérdida Directa:** Aprobación de créditos a perfiles de alto riesgo.
*   **Costo de Oportunidad:** Rechazo a clientes solventes, lo que limita el crecimiento de la cartera.

El objetivo central es predecir la probabilidad de que un prestatario caiga en mora severa (evento de default) en un horizonte temporal de 2 años, maximizando la métrica **ROC-AUC** y optimizando el estadístico **KS (Kolmogorov-Smirnov)** para el poder de discriminación.

---

## II. Estructura del Directorio
El repositorio del proyecto sigue una arquitectura estándar para proyectos de ciencia de datos:

*   `app/`: Código fuente de la aplicación o API para el despliegue del modelo en producción.
*   `data/`: Almacenamiento de datos, subdividido en:
    *   `raw/`: Datos originales sin procesar (ej. `cs-training.csv`).
    *   `processed/`: Datos limpios e imputados (ej. `cs-training-clean.csv`, `log_exclusiones_edad.csv`).
*   `models/`: Modelos serializados y entrenados.
*   `notebooks/`: Cuadernos de Jupyter para exploración, análisis y preparación.
*   `retail_scoring_env/`: Entorno virtual de Python para aislamiento de dependencias.
*   `README.md`: Documento explicativo del proyecto.
*   `requirements.txt`: Dependencias y librerías necesarias.

---

## III. Metodología (CRISP-DM)
El proyecto se rige por la metodología CRISP-DM. Se han desarrollado las siguientes fases:

### Fase 1: Comprensión del Negocio y Taxonomía de Variables
Se trabajó sobre una muestra de **150,000 registros** con nomenclatura técnica bancaria.

*   **Variable Objetivo (Target):**
    *   `indicador_default`: Mora $\ge$ 90 días en los últimos 24 meses.
*   **Variables Predictoras Estandarizadas:**
    *   `utilizacion_limite_revolvente`, `edad_solicitante`, `frecuencia_mora_30_59d`, `indice_endeudamiento`, `ingreso_mensual_bruto`, `conteo_instrumentos_credito`, `frecuencia_mora_90d`, `conteo_hipotecas`, `frecuencia_mora_60_89d`, `carga_familiar`.

### Fase 2: Comprensión de los Datos
Se identificaron problemas de calidad estructural:
*   **Valores Nulos:** Déficit del 19.82% en `ingreso_mensual_bruto` y 2.61% en `carga_familiar`.
*   **Outliers y Anomalías:** Edades ilógicas (0 años) y valores absurdos en ratios de endeudamiento.
*   **Códigos de Sistema:** Valores 96 y 98 en historial de mora (errores de sistemas legados).

### Fase 3: Preparación de los Datos
Se generó un dataset limpio (`df_clean`) aplicando:
*   **Tratamiento de Edad:** Eliminación de registros < 18 o > 90 años; registro en `log_exclusiones_edad.csv`.
*   **Clipping (Truncamiento) y Flags:**
    *   **Límite Revolvente/Endeudamiento:** Clipping superior en 2.0.
    *   **Historial de Mora:** Clipping en 20 para mitigar códigos 96/98.
    *   **Hipotecas/Instrumentos:** Clipping en 10 y 30 respectivamente.
*   **Imputación:**
    *   `ingreso_mensual_bruto`: Imputación por la **mediana** con flag de control.
    *   `carga_familiar`: Imputación basada en la **moda**.

---

## IV. Pasos para la Configuración y Ejecución

### 1. Clonar el repositorio
Navegue mediante la consola hacia la raíz del proyecto.

### 2. Activar el entorno virtual
Utilice el entorno proveído o cree uno nuevo según su OS:
```bash
# Linux/Mac
source retail_scoring_env/bin/activate

# Windows
retail_scoring_env\Scripts\activate