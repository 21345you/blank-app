import streamlit as st
from utils.db import init_db
import time
import sqlite3

conn = sqlite3.connect('data/auctions.db', check_same_thread=False)
c = init_db()

def supplier_interface():
    st.title(f"Espace {st.session_state.user['name']}")
    auction_id = st.number_input("ID de l'enchère", min_value=1)

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM auctions WHERE id=? AND is_active=1', (auction_id,))
    auction = cursor.fetchone()
    if not auction:
        st.error("Enchère introuvable ou terminée.")
        return
    
    if auction:
        st.subheader(auction[1])
        remaining_time = auction[3] - time.time()
        st.write(f"Temps restant: {int(remaining_time // 60)}:{int(remaining_time % 60):02d}")
    else:
        st.warning("y'a aucun enchère active") 

    # Affichage du meilleur prix
    cursor.execute('SELECT MIN(amount) FROM bids WHERE auction_id=?', (auction_id,))
    best_bid_result = cursor.fetchone()
    best_bid = best_bid_result[0] if best_bid_result and best_bid_result[0] is not None else (auction[2] if auction and len(auction) > 2 else "N/A")
    st.metric("Meilleure offre actuelle", f"{best_bid} €")
    
    # Soumission d'offre
    with st.form("submit_bid"):
        new_bid = st.number_input("Votre offre (€)", min_value=0.0, step=0.01)
        if st.form_submit_button("Soumettre"):
            if new_bid >= best_bid:
                st.error("Votre offre doit être inférieure au prix actuel !")
            else:
                cursor.execute('INSERT INTO bids VALUES (?, ?, ?, ?)',
                         (auction_id, st.session_state.user['name'], new_bid, time.time()))
                conn.commit()
                st.success("Offre soumise !")
                st.rerun()