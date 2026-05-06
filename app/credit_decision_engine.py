import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.express as px

# =============================================================================
# 1. CONFIGURACIÓN Y CSS 
# =============================================================================
st.set_page_config(
    page_title="Credit Scoring | Risk Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    :root {
        --bg-main: #0b141a;
        --bg-card: #15202b;
        --border-color: #2b3d4a;
        --text-primary: #ffffff;
        --text-secondary: #8d9aa5;
        --accent-red: #E0462D;
        --status-green: #27AE60;
        --status-yellow: #F2994A;
        --status-red: #EB5757;
    }

    .tech-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 24px;
        margin-bottom: 16px;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .metric-value {
        color: var(--text-primary);
        font-size: 56px;
        font-weight: 400;
        line-height: 1;
        margin: 0 0 12px 0;
    }
    
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-aprobado { background-color: rgba(39, 174, 96, 0.1); color: var(--status-green); border: 1px solid rgba(39, 174, 96, 0.3); }
    .badge-manual { background-color: rgba(242, 153, 74, 0.1); color: var(--status-yellow); border: 1px solid rgba(242, 153, 74, 0.3); }
    .badge-rechazado { background-color: rgba(235, 87, 87, 0.1); color: var(--status-red); border: 1px solid rgba(235, 87, 87, 0.3); }
    
    .tech-divider {
        height: 1px;
        background-color: var(--border-color);
        margin: 24px 0;
    }
    .factor-item {
        margin-bottom: 16px;
    }
    .factor-name {
        color: var(--text-primary);
        font-size: 14px;
        font-weight: 500;
    }
    .factor-value {
        color: var(--text-secondary);
        font-size: 13px;
        margin-top: 4px;
    }
    .highlight-pos { color: var(--status-green); font-weight: 600; }
    .highlight-neg { color: var(--status-red); font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. CARGA DE MODELO
# =============================================================================
@st.cache_resource
def load_model_assets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pkl_path = os.path.join(current_dir, '..', 'models', 'modelo_scorecard.pkl')
    
    if not os.path.exists(pkl_path):
        st.error(f"Error: Modelo no encontrado en ruta {pkl_path}")
        st.stop()
        
    with open(pkl_path, 'rb') as f:
        return pickle.load(f)

assets = load_model_assets()
modelo, tabla_puntos, base_score = assets['modelo'], assets['tabla_puntos'], assets['base_score']

# =============================================================================
# 3. PANEL DE CONTROL (SIDEBAR)
# =============================================================================
with st.sidebar:
    st.markdown("<div style='font-size: 12px; color: #8d9aa5; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 20px;'>Input Parameters</div>", unsafe_allow_html=True)

def get_user_inputs():
    with st.sidebar.expander("Comportamiento Crediticio", expanded=True):
        utilizacion = st.slider("Uso de Línea Revolvente", 0.0, 1.0, 0.35)
        mora = st.number_input("Eventos de Mora Históricos", min_value=0, step=1, value=0)
        
    with st.sidebar.expander("Perfil Demográfico", expanded=True):
        edad = st.slider("Edad Solicitante", 18, 95, 35)
        carga = st.number_input("Carga Familiar", min_value=0, step=1, value=1)
        
    with st.sidebar.expander("Situación Financiera", expanded=True):
        ingreso = st.number_input("Ingreso Mensual Bruto", min_value=0, value=4500)
        endeudamiento = st.number_input("Ratio de Endeudamiento", min_value=0.0, value=0.3)
        hipotecas = st.number_input("Hipotecas Activas", min_value=0, step=1, value=0)
        instrumentos = st.number_input("Otros Créditos", min_value=0, step=1, value=2)

    data = {
        'utilizacion_limite_revolvente': utilizacion, 'edad_solicitante': edad,
        'indice_endeudamiento': endeudamiento, 'ingreso_mensual_bruto': ingreso,
        'conteo_instrumentos_credito': instrumentos, 'conteo_hipotecas': hipotecas,
        'carga_familiar': carga, 'total_eventos_mora': mora
    }
    return pd.DataFrame(data, index=[0])

df_input = get_user_inputs()

# =============================================================================
# 4. MOTOR DE CÁLCULO
# =============================================================================
puntos_detalle = df_input.melt(var_name='Variable', value_name='Valor_Original')
puntos_detalle = puntos_detalle.merge(tabla_puntos, on='Variable')
puntos_detalle['Puntos_Generados'] = puntos_detalle['Valor_Original'] * puntos_detalle['Puntos_por_Unidad']

score_final = base_score + puntos_detalle['Puntos_Generados'].sum()
CUTOFF_RECHAZO, CUTOFF_APROBACION = 400, 500

# =============================================================================
# 5. VISTA PRINCIPAL (WORKSPACE)
# =============================================================================
st.markdown("<h2 style='font-weight: 400; margin-bottom: 0;'>Credit Decision Engine</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #8d9aa5; font-size: 14px;'>Risk Analysis Workspace</p>", unsafe_allow_html=True)
st.markdown("<div class='tech-divider'></div>", unsafe_allow_html=True)

col_score, col_grafico = st.columns([1, 2.5])

with col_score:
    if score_final >= CUTOFF_APROBACION:
        badge_class, dictamen = "badge-aprobado", "Approved"
    elif score_final >= CUTOFF_RECHAZO:
        badge_class, dictamen = "badge-manual", "Manual Review"
    else:
        badge_class, dictamen = "badge-rechazado", "Rejected"

    st.markdown(f"""
        <div class="tech-card">
            <div class="metric-label">Calculated Score</div>
            <div class="metric-value">{score_final:.0f}</div>
            <div class="status-badge {badge_class}">{dictamen}</div>
            <div style="margin-top: 20px; font-size: 12px; color: #8d9aa5;">
                Base Score: {base_score:.1f}<br>
                Variance: {(score_final - base_score):+.1f}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_grafico:
    st.markdown("<div class='metric-label' style='margin-bottom: 16px;'>Model Explainability (Reason Codes)</div>", unsafe_allow_html=True)
    
    puntos_detalle_graf = puntos_detalle.copy()
    puntos_detalle_graf['Variable'] = puntos_detalle_graf['Variable'].str.replace('_', ' ').str.title()
    
    color_scale = [[0.0, '#EB5757'], [0.5, '#2b3d4a'], [1.0, '#27AE60']]
    
    fig = px.bar(
        puntos_detalle_graf.sort_values(by='Puntos_Generados'), 
        x='Puntos_Generados', y='Variable', orientation='h',
        color='Puntos_Generados',
        color_continuous_scale=color_scale,
        text_auto='.1f'
    )
    
    fig.update_traces(
        textfont_size=11, 
        textfont_color='white', 
        textangle=0, 
        textposition="outside", 
        cliponaxis=False
    )
    
    fig.update_layout(
        showlegend=False, 
        coloraxis_showscale=False,
        height=280, 
        margin=dict(l=0, r=40, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#8d9aa5', size=11),
        xaxis=dict(showgrid=True, gridcolor='#2b3d4a', zeroline=True, zerolinecolor='#8d9aa5', title=""),
        yaxis=dict(title="")
    )
    st.plotly_chart(fig, config={'displayModeBar': False})

# =============================================================================
# 6. ANÁLISIS DE FACTORES
# =============================================================================
st.markdown("<div class='tech-divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='metric-label'>Driver Analysis</div>", unsafe_allow_html=True)

fortalezas = puntos_detalle.nlargest(2, 'Puntos_Generados')
debilidades = puntos_detalle.nsmallest(2, 'Puntos_Generados')

col_fort, col_deb = st.columns(2)

html_fort = "<div class='tech-card'>"
html_fort += "<div style='color: #ffffff; font-size: 14px; font-weight: 500; margin-bottom: 16px; border-bottom: 1px solid #2b3d4a; padding-bottom: 8px;'>Positive Drivers</div>"
for _, row in fortalezas.iterrows():
    nombre = row['Variable'].replace('_', ' ').title()
    html_fort += f"<div class='factor-item'><div class='factor-name'>{nombre}</div><div class='factor-value'>Impact: <span class='highlight-pos'>+{row['Puntos_Generados']:.1f} pts</span></div></div>"
html_fort += "</div>"

with col_fort:
    st.markdown(html_fort, unsafe_allow_html=True)

html_deb = "<div class='tech-card'>"
html_deb += "<div style='color: #ffffff; font-size: 14px; font-weight: 500; margin-bottom: 16px; border-bottom: 1px solid #2b3d4a; padding-bottom: 8px;'>Risk Factors (Top Offenders)</div>"
for _, row in debilidades.iterrows():
    nombre = row['Variable'].replace('_', ' ').title()
    html_deb += f"<div class='factor-item'><div class='factor-name'>{nombre}</div><div class='factor-value'>Impact: <span class='highlight-neg'>{row['Puntos_Generados']:.1f} pts</span></div></div>"
html_deb += "</div>"

with col_deb:
    st.markdown(html_deb, unsafe_allow_html=True)

# Auditoría técnica
with st.expander("Model Validation Log"):
    st.dataframe(
        puntos_detalle[['Variable', 'Valor_Original', 'Puntos_Generados']].style.format({
            'Valor_Original': '{:.2f}',
            'Puntos_Generados': '{:+.2f}'
        }),
        use_container_width=True
    )