import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sondage Chantier", layout="wide")

# Initialisation du stockage local
if "evaluations" not in st.session_state:
    st.session_state["evaluations"] = []

if "comments" not in st.session_state:
    st.session_state["comments"] = []

if "last_satisfaction" not in st.session_state:
    st.session_state["last_satisfaction"] = None


# ----------------------------
#       TITRE
# ----------------------------
st.title("🏗️ Sondage : État Général d’un Chantier")
st.write("Merci de participer au sondage. Veuillez évaluer les aspects suivants du chantier.")


# ----------------------------
#    INFORMATIONS GÉNÉRALES
# ----------------------------
st.subheader("👤 Informations")

nom_eval = st.text_input("Votre nom")
nom_chantier = st.text_input("Nom du chantier évalué")
commentaire = st.text_area("Votre commentaire sur l’état général du chantier")


# ----------------------------
#       SLIDERS
# ----------------------------
st.subheader("📊 Critères d’Évaluation (0 = très mauvais, 100 = excellent)")

avancement = st.slider("Avancement des travaux", 0, 100, 50)
securite = st.slider("Sécurité du chantier", 0, 100, 50)
qualite = st.slider("Qualité du travail réalisé", 0, 100, 50)
materiaux = st.slider("Gestion des matériaux", 0, 100, 50)
proprete = st.slider("Propreté et organisation du chantier", 0, 100, 50)


# ----------------------------
#   VERIFICATION DES CHAMPS
# ----------------------------
def all_filled():
    return (
        nom_eval.strip() != "" and
        nom_chantier.strip() != "" and
        commentaire.strip() != ""
    )


# ----------------------------
#   ENREGISTREMENT
# ----------------------------
if st.button("📩 Soumettre l'évaluation"):
    if not all_filled():
        st.error("⚠️ Vous devez remplir tous les champs, y compris le commentaire.")
    else:

        # moyenne
        satisfaction = (avancement + securite + qualite + materiaux + proprete) / 5
        st.session_state["last_satisfaction"] = satisfaction

        # Sauvegarde
        st.session_state["evaluations"].append({
            "Nom": nom_eval,
            "NomChantier": nom_chantier,
            "Avancement": avancement,
            "Sécurité": securite,
            "Qualité": qualite,
            "Matériaux": materiaux,
            "Propreté": proprete,
            "Satisfaction": satisfaction
        })

        st.session_state["comments"].append({
            "Nom": nom_eval,
            "Commentaire": commentaire
        })

        st.success("✔ Évaluation enregistrée avec succès !")


# ----------------------------
#   DIAGRAMME CIRCULAIRE GLOBAL
# ----------------------------
st.subheader("📈 Niveau général de satisfaction")

if len(st.session_state["evaluations"]) > 0:

    satisfactions = [d["Satisfaction"] for d in st.session_state["evaluations"]]
    satisfaction_globale = sum(satisfactions) / len(satisfactions)

    fig, ax = plt.subplots(figsize=(3, 3))  # <-- DIAGRAMME PLUS PETIT

    labels = ["Satisfaction Globale", "Reste"]
    values = [satisfaction_globale, 100 - satisfaction_globale]

    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Satisfaction Globale", fontsize=12)

    st.pyplot(fig)

else:
    st.info("Aucune donnée disponible pour le moment.")


# ----------------------------
#   TABLEAU DES SATISFACTIONS
# ----------------------------
st.subheader("📋 Niveaux de satisfaction des utilisateurs")

if len(st.session_state["evaluations"]) > 0:
    df_satisfaction = pd.DataFrame([
        {"Nom": d["Nom"], "Satisfaction": d["Satisfaction"]}
        for d in st.session_state["evaluations"]
    ])
    st.table(df_satisfaction)
else:
    st.info("Aucune évaluation enregistrée.")


# ----------------------------
#    TABLEAU DES COMMENTAIRES
# ----------------------------
st.subheader("💬 Commentaires des utilisateurs")

if len(st.session_state["comments"]) > 0:
    df_comments = pd.DataFrame(st.session_state["comments"])
    st.table(df_comments)
else:
    st.info("Aucun commentaire enregistré pour le moment.")