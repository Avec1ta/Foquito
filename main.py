import os

#import pyperclip
import requests
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Foquito", page_icon="💡", layout="wide")

st.markdown(
    """
    <style>
    .centered-title {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 50px;
    }
    .custom-label {
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    .right-column {
        margin-left: 50px; 
    }
    .copy-button {
        margin-left: 50px; 
    }
    .footer {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 50px;
        font-size: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar el título centrado en la parte superior
st.markdown('<div class="centered-title">Foquito💡</div>', unsafe_allow_html=True)

dify_secret = os.environ['DIFY_API_KEY']

col1, col2 = st.columns([4, 5])

with col1:
  st.markdown('<div class="custom-label">Cuéntame de tu negocio aquí 👇</div>', unsafe_allow_html=True)
  prompt = st.text_area(label="", \
placeholder="Mi negocio es...", \
height=150)

  base_url = "https://api.dify.ai/v1"
  path = "/workflows/run"
  full_url = base_url + path

  headers = {
          "Authorization": f"Bearer {dify_secret}",
          "Content-Type": "application/json"
      }

  data = {
          "inputs": {
          "query": prompt
        },
        "response_mode": "blocking",
        "user": "Emprendedor"
    }

    # Variable para almacenar la respuesta del asistente
  if 'assistant_response' not in st.session_state:
        st.session_state.assistant_response = ""

# Botón de enviar justo debajo de la caja de texto
  if st.button("Enviar"):
    if prompt:
        # Mostrar mensaje de cargando
        with st.spinner("Cargando..."):
            # Hacer la solicitud a la API de Dify
            response = requests.post(full_url, headers=headers, json=data)
            response_json = response.json()

            if response.status_code == 200:
                # Extraer la respuesta del asistente del campo "Propuestas"
                st.session_state.assistant_response = response_json.get("data", {}).get("outputs", {}).get("Propuestas", "No se pudo obtener la respuesta.")
            else:
                st.session_state.assistant_response = f"Error: {response.status_code} - {response.text}"
    else:
        st.warning("Por favor, escribe una solicitud.")


with col2:
    if not st.session_state.assistant_response:
        st.markdown('''
        <div class="right-column">
            <h3>Instrucciones</h3>
            <p>Escribe en la caja de texto de la izquierda: el rubro de tu 
            negocio, los productos o servicios que vendes, quiénes son tus 
            clientes, cuál es la identidad de tu marca, cuántas ideas necesitas (máximo 
            20 ideas por ahora)
            y para qué mes las necesitas. Luego presiona 'Enviar' para obtener 
            ideas de contenido para tus redes sociales. 
            Un ejemplo de buen prompt sería:</p>
            <pre>
            Tengo un vivero, vendo plantas de interior y exterior, suculentas, 
            macetas, abonos, fertilizantes, insecticidas orgánicos, etc. 
            Mi marca se llama "Verdileza" y somos una marca ecológica, que ama 
            la naturaleza y busca propagar este amor por las plantas y el 
            equilibrio natural a todas las personas. Mis clientes suelen ser 
            jóvenes, mayormente mujeres que les gusta la belleza que las 
            plantas aportan a sus espacios. Deseo 7 ideas para setiembre.
            </pre>
        </div>
        ''', 
        unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="right-column">
            <h4>Respuesta:</h4>
            <p>{}</p>
        </div>
        '''.format(st.session_state.assistant_response), unsafe_allow_html=True)
        if len(st.session_state.assistant_response) > 450:
            st.image("recuerda_que_foquito.png", caption="", width=550)
        #st.markdown('<div class="copy-button">', unsafe_allow_html=True)
        #if st.button("Copiar respuesta"):
            # Use Streamlit's built-in clipboard functionality
            #pyperclip.copy(st.session_state.assistant_response)
            #st.success("Respuesta copiada al portapapeles")
        #st.markdown('</div>', unsafe_allow_html=True)

# Mensaje de texto con hipervínculo al final de la pantalla
st.markdown('''
<div class="footer">
    <p>¿Tienes feedback? Envíalo por correo <a href="mailto:ana.vict.esp@gmail.com">aquí</a>.</p>
</div>
''', unsafe_allow_html=True)
