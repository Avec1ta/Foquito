import streamlit as st
import requests
import os

dify_secret = os.environ['DIFY_API_KEY']

st.image("foquito_logo.png", use_container_width=False, width=200)
st.write("**Idea contenido en un ratito**")

st.markdown("""
¡Hola! Soy un asistente que te ayudará generando ideas de contenido creativas para tus redes sociales, adaptadas a las necesidades de tu negocio y a tu público objetivo.

Cuéntame: 
- ¿A qué rubro perteneces?
- ¿Qué productos o servicios ofreces? (si es un negocio) o ¿Sobre qué temas hablas? (si eres creador de contenido) 
- ¿Cuál es la personalidad de tu marca? (formal, juvenil, alegre, etc.)
- ¿Quiénes son tus clientes o público objetivo?
- ¿Cuántas ideas necesitas? (máximo 20 por ahora 🙈)
- ¿Para qué mes las necesitas?
- ¿Hay fechas especiales que quieras considerar?
""")

prompt = st.text_area("¡Aquí te leo!👇:")

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
assistant_response = ""

if st.button("Enviar"):
    if prompt:
        # Enviar el prompt al workflow en Dify
        response = requests.post(full_url, headers=headers, json=data)
        response_json = response.json()

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Extraer la respuesta del asistente del campo "Propuestas"
            assistant_response = response_json.get("data", {}).get("outputs", {}).get("Propuestas","No se pudo obtener la respuesta.")
            
        else:
            assistant_response = f"Error: {response.status_code} - {response.text}"
    else:
        st.write("Por favor, ingresa un prompt.")


# Mostrar la respuesta del asistente
if assistant_response:
    st.markdown(f"**Respuesta de Foquito 💡:**\n\n{assistant_response}")
    st.image("recuerda_foquito.png", caption="", width=550)