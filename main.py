import streamlit as st
import pandas as pd
import datetime
import os

# Chemin vers le fichier CSV où les messages et les liens vidéo seront stockés
FILE_PATH = 'messages.csv'

def load_messages():
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        messages = pd.read_csv(FILE_PATH)
    else:
        messages = pd.DataFrame(columns=['date', 'user', 'message', 'video_link'])
    return messages

def save_message(user, message, video_link):
    messages = load_messages()
    new_message = pd.DataFrame([[datetime.datetime.now(), user, message, video_link]],
                               columns=['date', 'user', 'message', 'video_link'])
    messages = pd.concat([messages, new_message], ignore_index=True)
    messages.to_csv(FILE_PATH, index=False)

# Interface utilisateur
st.title('Forum de Discussion')

user = st.text_input('Votre nom')
message = st.text_area('Votre message')
video_link = st.text_input('Lien vidéo (optionnel)')

if st.button('Poster'):
    save_message(user, message, video_link)
    st.success("Message posté avec succès!")

# Afficher les messages et les vidéos
messages = load_messages()
if not messages.empty:
    for idx, row in messages.iterrows():
        st.write(f"{row['date']} - {row['user']}: {row['message']}")
        if row['video_link']:  # Vérifie si un lien vidéo est présent
            st.video(row['video_link'])  # Affiche la vidéo
