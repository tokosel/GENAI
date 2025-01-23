from dotenv import load_dotenv

load_dotenv()  # prendre les variables d'environnement de .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Fonction pour charger le modèle OpenAI et obtenir une réponse


def get_gemini_response(input, image):
    model = genai.GenerativeModel("gemini-1.5-flash-8b-exp-0827")
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text


## initialiser notre application Streamlit

st.set_page_config(page_title="Local AI")

st.header("Gemini Vision par ordinateur")
input = st.text_input("Saisissez votre demande : ", key="input")
uploaded_file = st.file_uploader("Choisir une image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Charger l'mage.", use_column_width=True)


submit = st.button("Soumettre")

## Si le bouton « Demander » est cliqué

if submit:

    response = get_gemini_response(input, image)
    st.subheader("Voici la description:")
    st.write(response)
