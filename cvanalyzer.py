import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz  # PyMuPDF
from PIL import Image

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'API Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def pdf_to_text(pdf_file):
    """Extraire le texte de la première page du PDF"""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def get_gemini_response(job_description, cv_text):
    """Analyse du CV avec perspective de recrutement"""
    prompt = f"""Agis en tant que chargé de recrutement expérimenté. 
    Analyse ce CV par rapport à ce poste :

    Descriptif du poste : {job_description}

    CV analysé : {cv_text}

    Instructions pour ton analyse :
    - Évalue précisément la correspondance du profil
    - Identifie les points forts et points à améliorer
    - Calcule un pourcentage de matching
    - Sois objectif et pragmatique
    - Donne des conseils de candidature
    
    Format de réponse :
    🎯 Taux de Matching : X%
    
    Forces du candidat :
    - [Liste des points positifs]

    Points à améliorer :
    - [Liste des points faibles]

    Recommandations :
    - [Conseils pour améliorer la candidature]"""

    model = genai.GenerativeModel("gemini-1.5-flash-8b-exp-0827")
    response = model.generate_content(prompt)
    return response.text

# Configuration de l'application Streamlit
st.set_page_config(page_title="Analyse de CV")
st.header("🔍 Analyse de CV - Abdoulaye's CV Matcher")

# Saisie de la description du poste
job_description = st.text_area("Description du poste visé :", 
                                placeholder="Ex: Développeur Python junior, 0-2 ans d'expérience, maîtrise de Django...", 
                                key="job_input")

# Téléchargement du CV
uploaded_cv = st.file_uploader("Télécharger le CV (PDF)", type=["pdf"])

# Bouton d'analyse
if st.button("Analyser le CV") and uploaded_cv is not None and job_description:
    # Extraction du texte du CV
    cv_text = pdf_to_text(uploaded_cv)
    
    # Analyse avec Gemini
    with st.spinner('Analyse en cours...'):
        analysis = get_gemini_response(job_description, cv_text)
    
    # Affichage des résultats
    st.subheader("📋 Résultat de l'analyse")
    st.write(analysis)