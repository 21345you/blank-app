import streamlit as st
from pages import login, acheteur, fournisseur

st.set_page_config(page_title="Enchères Inversées", page_icon="📊", layout="wide")

# Initialiser st.session_state.user si nécessaire
if 'user' not in st.session_state:
    st.session_state.user = None

# Gestion de la navigation
if st.session_state.user is None:
    login.login()
else:
    # Vérification renforcée de la structure utilisateur
    if not isinstance(st.session_state.user, dict) or 'role' not in st.session_state.user:
        st.error("Configuration utilisateur invalide")
        st.session_state.user = None
        st.rerun()

    # Logique de routing basée sur le rôle
    match st.session_state.user['role']:
        case "Acheteur":
            acheteur.buyer_interface()
        case "Fournisseur":
            fournisseur.supplier_interface()
        case _:
            st.error("Rôle utilisateur non reconnu")
            st.session_state.user = None
            st.rerun()