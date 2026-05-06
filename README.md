# Proyecto de Credit Scoring: Predicción de Incumplimiento

> **¡Prueba la aplicación!** Puedes interactuar con el modelo y realizar predicciones en tiempo real a través de  [Credit Decision Engine en Streamlit](https://creditdecisionengine-byclaudiochavarria.streamlit.app/).

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
*   `README.md`: Documento principal de documentación del proyecto.
*   `requirements.txt`: Archivo que detalla las dependencias y librerías de Python necesarias para replicar el entorno.

---

## III. Metodología (CRISP-DM)

El proyecto se rige estrictamente por la metodología estándar de la industria **CRISP-DM** (Cross-Industry Standard Process for Data Mining). A continuación se explican a detalle las fases desarrolladas:
# Metodología del Proyecto (CRISP-DM)


## IV. Pasos para la Configuración y Ejecución

Para reproducir el entorno, ejecutar los cuadernos de análisis o levantar la aplicación localmente, siga estos pasos:

### 1. Clonar el repositorio y navegar a la raíz
Abra su consola de preferencia y diríjase a la carpeta del proyecto.

### 2. Activar el entorno virtual
cree un entorno y utilice requirements.txt :

```bash
# Para entornos basados en Linux/Mac
source retail_scoring_env/bin/activate

# Para entornos basados en Windows
retail_scoring_env\Scripts\activate