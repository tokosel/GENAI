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
    """Extraire le texte de toutes les pages du PDF"""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def get_gemini_response(job_description, cv_text, analysis_type):
    """Analyse du CV avec perspective de recrutement"""
    analysis_prompts = {
        "Matching Général": f"""Agis en chargé de recrutement expert. 
        Analyse ce CV par rapport à ce poste :
        Descriptif du poste : {job_description}
        CV analysé : {cv_text}

        Évalue précisément :
        - Correspondance globale du profil
        - Compétences clés
        - Adéquation formation/expérience
        - Potentiel pour le poste

        Format :
        🎯 Taux de Matching : X%
        🔑 Compétences Clés Alignées : [liste]
        🚨 Points à Améliorer : [liste]
        💡 Recommandations : [conseils]""",

        "Filtrage Technique": f"""Analyse technique du CV :
        Poste : {job_description}
        CV : {cv_text}

        Filtres :
        - Technologies requises
        - Niveau technique
        - Certifications
        - Expériences techniques précises

        Rapport :
        ✅ Technologies Maîtrisées : [liste]
        ❌ Technologies Manquantes : [liste]
        📊 Score Technique : X/10""",

        "Profil Psychologique": f"""Analyse comportementale du candidat :
        Contexte : {job_description}
        CV : {cv_text}

        Évaluation :
        - Soft skills
        - Adaptabilité
        - Potentiel de développement
        - Alignement culturel

        Insights :
        🧠 Profil Psychologique : [description]
        🤝 Compatibilité Culturelle : X%
        🚀 Potentiel de Croissance : [évaluation]"""
    }

    prompt = analysis_prompts.get(analysis_type, analysis_prompts["Matching Général"])

    model = genai.GenerativeModel("gemini-1.5-flash-8b-exp-0827")
    response = model.generate_content(prompt)
    return response.text

# Configuration Streamlit
st.set_page_config(page_title="Analyse de CV Pro", page_icon="🔍")
st.header("🔍 Abdoulaye's CV Matcher 🚀")

# Options de personnalisation
col1, col2 = st.columns(2)
with col1:
    job_description = st.text_area("Description du Poste", 
                                   placeholder="Détails précis du poste...", 
                                   key="job_input")

with col2:
    analysis_type = st.selectbox("Type d'Analyse", [
        "Matching Général",
        "Filtrage Technique", 
        "Profil Psychologique"
    ])

# Téléchargement du CV
uploaded_cv = st.file_uploader("Télécharger CV (PDF)", type=["pdf"], accept_multiple_files=True)

# Bouton d'analyse
if st.button("Analyser") and uploaded_cv and job_description:
    for cv_file in uploaded_cv:
        # Extraction du texte du CV
        cv_text = pdf_to_text(cv_file)
        
        # Analyse avec Gemini
        with st.spinner(f'Analyse de {cv_file.name} en cours...'):
            analysis = get_gemini_response(job_description, cv_text, analysis_type)
        
        # Affichage des résultats
        st.subheader(f"📄 Résultat d'analyse de {cv_file.name}")
        st.write(analysis)
        st.divider()