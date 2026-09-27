import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

st.set_page_config(page_title="MyCar", page_icon="🚗", layout="wide")
DATA_FILE = Path("dataset.csv")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "car" not in st.session_state:
    st.session_state.car = {}
if "appointments" not in st.session_state:
    st.session_state.appointments = []
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE) if DATA_FILE.exists() else pd.DataFrame()

df = load_data()

# =========================
# CONNEXION / INSCRIPTION
# =========================
if not st.session_state.logged_in:
    st.title("🚗 MyCar")
    st.subheader("Votre assistant automobile")
    login, signup = st.tabs(["🔐 Connexion", "📝 Créer un compte"])

    with login:
        u = st.text_input("Nom d'utilisateur", key="login_u")
        pw = st.text_input("Mot de passe", type="password", key="login_pw")
        if st.button("Se connecter", type="primary"):
            if u and pw:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.session_state.role = "Conducteur"
                st.rerun()
            else:
                st.error("Remplissez les champs.")

    with signup:
        name = st.text_input("Nom complet")
        u2 = st.text_input("Nom d'utilisateur", key="signup_u")
        email = st.text_input("Email")
        pw2 = st.text_input("Mot de passe", type="password", key="signup_pw")
        role = st.selectbox("Votre métier / profil",
                            ["Conducteur", "Technicien", "Expert automobile"])
        if st.button("Créer mon compte", type="primary"):
            if name and u2 and email and pw2:
                st.session_state.logged_in = True
                st.session_state.username = u2
                st.session_state.role = role
                st.success("Compte créé.")
                st.rerun()
            else:
                st.error("Tous les champs sont obligatoires.")
    st.stop()

# =========================
# MENU
# =========================
st.sidebar.title("🚗 MyCar")
st.sidebar.write(f"👤 {st.session_state.username}")
st.sidebar.write(f"Profil : **{st.session_state.role}**")
if st.sidebar.button("🚪 Déconnexion"):
    st.session_state.logged_in = False
    st.rerun()

page = st.sidebar.radio("Navigation", [
    "🏠 Accueil", "🚘 Ma voiture", "🛠️ Conseils & diagnostic",
    "📅 Entretien & rappels", "👨‍🔧 Techniciens", "💬 Discussion",
    "🎥 Vidéos", "👤 Mon profil"
])

# =========================
# ACCUEIL
# =========================
if page == "🏠 Accueil":
    st.title("🚗 Bienvenue sur MyCar")
    st.write("Une plateforme pour suivre votre voiture et contacter des professionnels.")
    a,b,c,d = st.columns(4)
    a.metric("🚘 Véhicule", "1" if st.session_state.car else "0")
    b.metric("📅 Rappels", len(st.session_state.appointments))
    c.metric("💬 Messages", len(st.session_state.messages))
    d.metric("👤 Profil", st.session_state.role)

# =========================
# VOITURE
# =========================
elif page == "🚘 Ma voiture":
    st.header("🚘 Ma voiture")
    with st.form("car"):
        brand = st.text_input("Marque", st.session_state.car.get("brand",""))
        model = st.text_input("Modèle", st.session_state.car.get("model",""))
        year = st.number_input("Année", 1950, 2030,
                               int(st.session_state.car.get("year",2020)))
        fuel = st.selectbox("Carburant", ["Essence","Diesel","Hybride","Électrique"])
        km = st.number_input("Kilométrage (km)", 0, 1000000,
                             int(st.session_state.car.get("km",0)))
        if st.form_submit_button("💾 Enregistrer"):
            st.session_state.car = {"brand":brand,"model":model,
                                    "year":year,"fuel":fuel,"km":km}
            st.success("Véhicule enregistré.")
    if st.session_state.car:
        st.json(st.session_state.car)

# =========================
# CONSEILS
# =========================
elif page == "🛠️ Conseils & diagnostic":
    st.header("🛠️ Conseils & diagnostic")
    problem = st.selectbox("Problème", [
        "Voyant moteur","Batterie","Surchauffe","Bruit inhabituel",
        "Freins","Pneus","Climatisation","Consommation élevée","Autre"
    ])
    advice = {
        "Voyant moteur":"Un diagnostic OBD peut aider à identifier la cause. Consultez un professionnel si le problème persiste.",
        "Batterie":"Faites contrôler la batterie et le système de charge.",
        "Surchauffe":"Arrêtez-vous dans un endroit sûr et laissez refroidir le moteur. Ne touchez pas au circuit chaud.",
        "Bruit inhabituel":"Notez le moment et les conditions d'apparition puis demandez un contrôle.",
        "Freins":"Une perte d'efficacité ou un bruit inhabituel nécessite un contrôle professionnel.",
        "Pneus":"Contrôlez pression, usure et dommages visibles.",
        "Climatisation":"Contrôlez les réglages et faites diagnostiquer le circuit si nécessaire.",
        "Consommation élevée":"Contrôlez pneus, entretien et système moteur.",
        "Autre":"Décrivez précisément le symptôme à un technicien."
    }
    st.info(advice[problem])
    desc = st.text_area("Décrivez votre problème")
    if st.button("📨 Envoyer au technicien"):
        if desc:
            st.session_state.messages.append({"user":st.session_state.username,"message":desc})
            st.success("Demande enregistrée.")
        else:
            st.warning("Décrivez le problème.")

# =========================
# RAPPELS
# =========================
elif page == "📅 Entretien & rappels":
    st.header("📅 Entretien & rappels")
    with st.form("reminder"):
        service = st.selectbox("Service", ["Vidange","Révision","Freins","Pneus",
                                           "Batterie","Contrôle technique","Visite mécanicien","Autre"])
        dt = st.date_input("Date", date.today())
        note = st.text_area("Notes")
        if st.form_submit_button("📅 Ajouter"):
            st.session_state.appointments.append(
                {"service":service,"date":str(dt),"notes":note})
            st.success("Rappel ajouté.")
    if st.session_state.appointments:
        st.dataframe(pd.DataFrame(st.session_state.appointments), use_container_width=True)

# =========================
# TECHNICIENS
# =========================
elif page == "👨‍🔧 Techniciens":
    st.header("👨‍🔧 Techniciens")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun technicien dans le dataset.")

# =========================
# DISCUSSION
# =========================
elif page == "💬 Discussion":
    st.header("💬 Discussion avec experts / techniciens")
    for m in st.session_state.messages:
        st.write(f"**{m['user']} :** {m['message']}")
    msg = st.chat_input("Votre message...")
    if msg:
        st.session_state.messages.append({"user":st.session_state.username,"message":msg})
        st.rerun()
    st.info("Dans cette version MVP, les messages sont conservés pendant la session.")

# =========================
# VIDEOS
# =========================
elif page == "🎥 Vidéos":
    st.header("🎥 Tutoriels")
    st.write("Ajoute ici les liens YouTube de tes tutoriels automobiles.")
    url = st.text_input("Lien vidéo YouTube")
    if url:
        st.video(url)

# =========================
# PROFIL
# =========================
elif page == "👤 Mon profil":
    st.header("👤 Mon profil")
    st.write(f"**Utilisateur :** {st.session_state.username}")
    st.write(f"**Profil :** {st.session_state.role}")
    if st.session_state.car:
        st.subheader("🚘 Ma voiture")
        st.json(st.session_state.car)
