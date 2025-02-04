import streamlit as st
from utils.auth import hash_password, verify_password
from utils.db import get_connection

def login():
    st.subheader("Connexion")
    role = st.selectbox("Rôle", ["Acheteur", "Fournisseur 1", "Fournisseur 2", "Fournisseur 3", "Fournisseur 4"])
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        try:
            # Vérification des identifiants avec hashage
            if role == "Acheteur":
                stored_hash = st.secrets["acheteur"]["password_hash"]
                if verify_password(password, stored_hash):
                    st.session_state.user = {"role": "Acheteur", "name": "Acheteur Public"}
                    st.success("Connecté avec succès !")
                    st.rerun()
                
            elif role.startswith("Fournisseur"):
                num = role.split()[-1]
                secret_key = f"fournisseur{num}"
                stored_hash = st.secrets[secret_key]["password_hash"]
                
                if verify_password(password, stored_hash):
                    st.session_state.user = {
                        "role": "Fournisseur",
                        "name": f"Fournisseur {num}"
                    }
                    st.success(f"Connecté en tant que Fournisseur {num} !")
                    st.rerun()

            # Si aucune correspondance trouvée
            st.error("Identifiants incorrects")

        except KeyError:
            st.error("Erreur de configuration : compte non trouvé")
        except Exception as e:
            st.error(f"Erreur technique : {str(e)}")