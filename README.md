# Proyecto de Credit Scoring: Predicción de Incumplimiento

> 🚀 **¡Prueba la aplicación en vivo!** Ya puedes interactuar con el modelo y realizar predicciones en tiempo real a través de nuestro [Credit Decision Engine en Streamlit](https://creditdecisionengine-byclaudiochavarria.streamlit.app/).

![Captura de la Aplicación](app/app_example.png)
*Vista previa de la interfaz de usuario del motor de decisiones de crédito.*

---

## I. Contexto Estratégico y Descripción del Proyecto

Este proyecto desarrolla un modelo predictivo de **Credit Scoring**, el cual es un instrumento fundamental para la asignación de capital bancario. Un sistema de scoring eficiente permite diferenciar perfiles de riesgo con precisión, asegurando la rentabilidad institucional y mitigando la morosidad estructural.

El problema de negocio principal radica en las ineficiencias financieras generadas por modelos con baja capacidad discriminatoria:
*   **Pérdida Directa:** Aprobación de créditos a perfiles de alto riesgo que terminan en default.
*   **Costo de Oportunidad:** Rechazo de clientes solventes (falsos positivos de riesgo), lo que limita el crecimiento orgánico de la cartera.

**Objetivo Central:** Predecir la probabilidad de que un prestatario caiga en mora severa (evento de default) en un horizonte temporal de 2 años. Se busca maximizar la métrica **ROC-AUC** y optimizar el estadístico **KS (Kolmogorov-Smirnov)** para garantizar el mayor poder de discriminación posible.

* **Origen de los Datos:** Este proyecto utiliza el dataset oficial de la competencia de Kaggle [Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit).

---

## II. Estructura del Directorio

El repositorio del proyecto sigue una arquitectura estándar y escalable para proyectos de ciencia de datos, organizada de la siguiente manera:

*   `app/`: Contiene el código fuente de la aplicación en Streamlit y recursos visuales para el despliegue del modelo predictivo (ej. `app_example.png`).
*   `data/`: Directorio destinado al almacenamiento de los datos.
    *   `raw/`: Datos originales sin procesar descargados de Kaggle (ej. `cs-training.csv`).
    *   `processed/`: Datos limpios, imputados y transformados, listos para el entrenamiento (ej. `cs-training-clean.csv`, `log_exclusiones_edad.csv`).
*   `models/`: Directorio para guardar los modelos serializados y entrenados listos para inferencia.
*   `notebooks/`: Cuadernos de Jupyter (Jupyter Notebooks) utilizados para la exploración, el análisis descriptivo y la ingeniería de características.
*   `retail_scoring_env/`: Entorno virtual de Python configurado específicamente para aislar las dependencias del proyecto.
*   `README.md`: Documento principal de documentación del proyecto.
*   `requirements.txt`: Archivo que detalla las dependencias y librerías de Python necesarias para replicar el entorno.

---

## III. Metodología (CRISP-DM)

El proyecto se rige estrictamente por la metodología estándar de la industria **CRISP-DM** (Cross-Industry Standard Process for Data Mining). A continuación se explican a detalle las fases desarrolladas:

### Fase 1: Comprensión del Negocio y Taxonomía de Variables
Se trabajó sobre una muestra histórica de **150,000 registros**. Como primer paso metodológico, se aplicó una estandarización de nomenclatura técnica orientada a la industria bancaria para facilitar su comprensión e interpretación funcional.

*   **Variable Objetivo (Target):**
    *   `indicador_default`: Representa un evento de mora $\ge$ 90 días en los últimos 24 meses (1 = Default, 0 = No Default).
*   **Variables Predictoras Estandarizadas:**
    *   `utilizacion_limite_revolvente`, `edad_solicitante`, `frecuencia_mora_30_59d`, `indice_endeudamiento`, `ingreso_mensual_bruto`, `conteo_instrumentos_credito`, `frecuencia_mora_90d`, `conteo_hipotecas`, `frecuencia_mora_60_89d`, `carga_familiar`.

### Fase 2: Comprensión de los Datos (EDA)
Mediante el Análisis Exploratorio de Datos se identificaron anomalías estructurales y problemas de calidad que requerían intervención directa:
*   **Valores Nulos:** Se detectó un déficit de información del **19.82%** en la variable `ingreso_mensual_bruto` y del **2.61%** en `carga_familiar`.
*   **Outliers y Anomalías Lógicas:** Presencia de edades ilógicas (ej. solicitantes de 0 años) y valores económicamente absurdos en los ratios de endeudamiento y uso de líneas de crédito revolventes.
*   **Códigos de Sistema Legados:** Presencia atípica de los valores numéricos `96` y `98` en las variables de historial de morosidad. Un análisis profundo reveló que estos números no representan eventos reales de mora, sino códigos de error de lectura de sistemas bancarios antiguos.

### Fase 3: Preparación de los Datos e Ingeniería de Características
Para garantizar la gobernanza del dato, mantener la trazabilidad y evitar el sesgo estadístico (como el overfitting o la distorsión paramétrica), se generó un conjunto de datos robusto (`df_clean`) aplicando las siguientes transformaciones:

1.  **Tratamiento de Edad:** Eliminación de clientes con 0 años o mayores de 90 años. Para mantener la auditoría, los casos anómalos se exportaron al registro `log_exclusiones_edad.csv`.
2.  **Clipping (Truncamiento) y Creación de Flags:** Para mitigar el apalancamiento de valores atípicos en los modelos sin perder la información:
    *   **Límite Revolvente y Endeudamiento:** Clipping superior en 2.0 y creación de banderas (flags) booleanas indicando que el registro era originalmente un outlier.
    *   **Historial de Mora:** Clipping en 20 para anular la distorsión de los códigos de sistema (96 y 98), acompañados de una variable dummy de registro.
    *   **Hipotecas e Instrumentos de Crédito:** Clipping superior en 10 y 30 respectivamente, agrupando la "cola larga" estadística de perfiles financieros ultra-complejos.
3.  **Imputación de Valores Nulos:**
    *   `ingreso_mensual_bruto`: Para evitar sesgos por la alta asimetría salarial, se realizó un clipping previo en 25,000, se imputó utilizando la **mediana** de la población y se añadió una variable flag indicando la imputación artificial.
    *   `carga_familiar`: Se imputaron los valores faltantes utilizando la **moda** estadística poblacional.

El resultado final de esta etapa es el archivo `cs-training-clean.csv`, un dataset altamente representativo y paramétricamente estable para las fases de modelado.

---

## IV. Pasos para la Configuración y Ejecución

Para reproducir el entorno, ejecutar los cuadernos de análisis o levantar la aplicación localmente, siga estos pasos:

### 1. Clonar el repositorio y navegar a la raíz
Abra su consola de preferencia y diríjase a la carpeta del proyecto.

### 2. Activar el entorno virtual
Utilice el entorno preconfigurado en el directorio `retail_scoring_env` o cree uno nuevo en caso de incompatibilidad con su sistema operativo:
```bash
# Para entornos basados en Linux/Mac
source retail_scoring_env/bin/activate

# Para entornos basados en Windows
retail_scoring_env\Scripts\activate