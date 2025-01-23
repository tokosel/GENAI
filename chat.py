from dotenv import load_dotenv

load_dotenv()  # prendre les variables d'environnement de .env.

import streamlit as st
import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Fonction pour charger le modèle OpenAI et obtenir une réponse

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):

    response = chat.send_message(question, stream=True)
    return response


## initialiser notre application Streamlit

st.set_page_config(page_title="Local AI")

st.header("Gemini Génération de texte")

input = st.text_input("Posez votre question : ", key="input")


submit = st.button("Soumettre")

## Si le bouton « Demander » est cliqué

if submit:

    response = get_gemini_response(input)
    st.subheader("La reponse à votre question : ")
    for chunk in response:
        print(st.write(chunk.text))
        print("_" * 80)

    #st.write(chat.history)
