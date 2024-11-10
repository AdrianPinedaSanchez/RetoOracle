import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import numpy as np

# Cargar el modelo entrenado
best_rf_model = joblib.load('best_rf_model.pkl')  # Asegúrate de tener el modelo guardado como .pkl

# Configurar estilo general
st.set_page_config(
    page_title="Predicción de Enfermedades Cardíacas",
    page_icon="💓",
    layout="centered"
)

# Estilo del mockup móvil con diseño responsivo
st.markdown(
    """
    <style>
        /* Estilos generales */
        .stApp {
            background: #F5F5F5;
            border-radius: 30px;
            box-shadow: 0px 15px 45px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: auto;
            overflow-y: auto;
            max-width: 540px; /* Tamaño máximo para pantallas grandes */
        }
        @media (max-width: 768px) {
            .stApp {
                max-width: 100%; /* Para pantallas más pequeñas */
                border-radius: 0;
                box-shadow: none;
                padding: 10px;
            }
        }
        .app-content {
            width: 100%;
            height: 100%;
            text-align: center;
            font-family: 'Arial', sans-serif;
            color: #333;
        }
        h1, h2, h3 {
            color: #FF5722;
        }
        .stButton button {
            background-color: #FF5722;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            width: 100%;
            padding: 10px;
        }
        .stButton button:hover {
            background-color: #FF3D00;
        }
        .st-radio > label {
            font-weight: bold;
        }
        /* Estilo del botón de menú */
        .menu-button {
            background-color: #FF5722;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            width: 100%;
        }
        /* Ocultar el título del expander */
        .streamlit-expanderHeader {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True
)

# Estado de la aplicación
if 'menu_expanded' not in st.session_state:
    st.session_state['menu_expanded'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'Inicio'

# Función para cambiar de página
def change_page(page_name):
    st.session_state['page'] = page_name
    st.session_state['menu_expanded'] = False

# Botón de menú y menú desplegable
with st.container():
    cols = st.columns([1, 9])
    with cols[0]:
        if st.button("☰"):
            st.session_state['menu_expanded'] = not st.session_state['menu_expanded']
    with cols[1]:
        st.write("")  # Espacio en blanco

if st.session_state['menu_expanded']:
    with st.expander("", expanded=True):
        if st.button("Inicio"):
            change_page('Inicio')
        if st.button("Predicción"):
            change_page('Predicción')
        if st.button("Visualización"):
            change_page('Visualización')

# Página actual
page = st.session_state['page']

# Página de inicio
if page == "Inicio":
    st.title("💓 Predicción de Enfermedades Cardíacas")
    st.write("Bienvenido a la aplicación de predicción de enfermedades cardíacas. Navega por las secciones para realizar una predicción o visualizar resultados.")

# Página de predicción
elif page == "Predicción":
    st.title("📊 Predicción")
    st.header("Responde las siguientes preguntas:")

    # Formulario de entrada
    age = st.number_input("¿Cuál es tu edad?", min_value=18, max_value=100, step=1)
    sex = st.radio("¿Cuál es tu sexo?", options=["Hombre", "Mujer"])
    sex = 1 if sex == "Hombre" else 0

    cp = st.radio(
        "Tipo de dolor en el pecho:",
        ["Angina típica", "Angina atípica", "Dolor no anginal", "Asintomático"]
    )
    opciones_map = {
        "Angina típica": 0,
        "Angina atípica": 1,
        "Dolor no anginal": 2,
        "Asintomático": 3
    }
    cp = opciones_map[cp]

    trestbps = st.number_input("Presión arterial en reposo (mm Hg):", min_value=80, max_value=200, step=1)
    chol = st.number_input("Nivel de colesterol en suero (mg/dl):", min_value=100, max_value=600, step=1)
    fbs = st.radio("¿Azúcar en sangre en ayunas > 120 mg/dl?", ["Sí", "No"])
    fbs = 1 if fbs == "Sí" else 0

    restecg = st.radio(
        "Resultados del electrocardiograma:",
        ["Normal", "Anomalía leve", "Hipertrofia ventricular"]
    )
    restecg = ["Normal", "Anomalía leve", "Hipertrofia ventricular"].index(restecg)

    thalach = st.number_input("Frecuencia cardíaca máxima (lpm):", min_value=60, max_value=220, step=1)
    exang = st.radio("¿Angina durante el ejercicio?", ["Sí", "No"])
    exang = 1 if exang == "Sí" else 0
    oldpeak = st.number_input("Depresión del segmento ST:", min_value=0.0, max_value=5.0, step=0.1)

    slope = st.radio(
        "Pendiente del ST durante ejercicio:",
        ["Ascendente", "Plana", "Descendente"]
    )
    slope = ["Ascendente", "Plana", "Descendente"].index(slope)

    ca = st.radio("Vasos coloreados por fluoroscopía:", ["0", "1", "2", "3"])
    ca = int(ca)

    thal = st.radio("Condición de talasemia:", ["Normal", "Defecto fijo", "Defecto reversible"])
    thal = ["Normal", "Defecto fijo", "Defecto reversible"].index(thal) + 1

    input_data = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
                              columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'])

    if st.button("Predecir"):
        prediccion = best_rf_model.predict(input_data)[0]
        probabilidad = best_rf_model.predict_proba(input_data)[:, 1][0]

        st.session_state["probabilidad"] = probabilidad
        st.subheader("Resultados:")
        st.write(f"**Predicción:** {'Enfermedad cardíaca' if prediccion == 1 else 'Sin enfermedad'}")
        st.write(f"**Riesgo calculado:** {probabilidad:.2%}")

# Página de visualización
elif page == "Visualización":
    st.title("📈 Visualización")

    if "probabilidad" in st.session_state:
        probabilidad = st.session_state["probabilidad"]
    else:
        st.warning("Por favor, realiza una predicción primero.")
        st.stop()

    fig, ax = plt.subplots()
    ax.pie([probabilidad, 1 - probabilidad], labels=["Riesgo", "Sin Riesgo"],
           colors=["#FF5722", "#D3D3D3"], startangle=90,
           autopct="%1.1f%%", wedgeprops=dict(width=0.3))
    st.pyplot(fig)
