import streamlit as st
import pandas as pd
import datetime

# Chemin vers le fichier CSV où les messages seront stockés
FILE_PATH = 'messages.csv'

# Fonction pour charger les messages depuis le fichier CSV
def load_messages():
    try:
        messages = pd.read_csv(FILE_PATH)
    except FileNotFoundError:
        # Si le fichier n'existe pas, on crée un DataFrame vide
        messages = pd.DataFrame(columns=['date', 'user', 'message'])
    return messages

# Fonction pour sauvegarder un nouveau message dans le fichier CSV
def save_message(user, message):
    messages = load_messages()
    new_message = pd.DataFrame([[datetime.datetime.now(), user, message]],
                               columns=['date', 'user', 'message'])
    messages = pd.concat([messages, new_message], ignore_index=True)
    messages.to_csv(FILE_PATH, index=False)

# Interface utilisateur
st.title('Forum de Discussion')

user = st.text_input('Votre nom')
message = st.text_area('Votre message')

if st.button('Poster'):
    save_message(user, message)

# Afficher les messages
messages = load_messages()
if not messages.empty:
    for idx, row in messages.iterrows():
        st.write(f"{row['date']} - {row['user']}: {row['message']}")
