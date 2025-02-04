import streamlit as st
from utils.db import get_connection, init_db
import time


conn = get_connection()
c = init_db()

def buyer_interface():
    st.title("Espace Acheteur")
    cursor = conn.cursor()
    # Création d'une enchère
    with st.form("new_auction"):
        title = st.text_input("Titre de l'enchère")
        initial_price = st.number_input("Prix initial (€)", min_value=0.0)
        duration = st.number_input("Durée (minutes)", min_value=1)
        
        if st.form_submit_button("Démarrer l'enchère"):
            auction_id = int(time.time())
            end_time = time.time() + duration * 60
            cursor.execute('INSERT INTO auctions VALUES (?, ?, ?, ?, ?)',
                     (auction_id, title, initial_price, end_time, True))
            conn.commit()
            st.success(f"Enchère #{auction_id} lancée !")
    
    # Affichage des enchères en cours
    st.subheader("Enchères Actives")
    cursor.execute('SELECT * FROM auctions WHERE is_active=1')
    active_auctions = cursor.fetchall()
    for auction in active_auctions:
        auction_id = auction[0]
        remaining_time = auction[3] - time.time()
        if remaining_time <= 0:
            cursor.execute('UPDATE auctions SET is_active=0 WHERE id=?', (auction_id,))
            conn.commit()
            continue
        
        st.write(f"**{auction[1]}** (ID: {auction_id})")
        st.write(f"Temps restant: {int(remaining_time // 60)}:{int(remaining_time % 60):02d}")
        
        # Affichage des offres
        cursor.execute('SELECT * FROM bids WHERE auction_id=? ORDER BY amount ASC', (auction_id,))
        bids = cursor.fetchall()
        if bids:
            st.write("Offres soumises :")
            for bid in bids:
                st.write(f"- {bid[2]} € par {bid[1]}")
