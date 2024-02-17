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

def save_messages(messages):
    messages.to_csv(FILE_PATH, index=False)

def save_message(user, message, video_link):
    messages = load_messages()
    # Assurez-vous que video_link est une chaîne vide si None est fourni
    video_link = video_link if video_link is not None else ""
    new_message = pd.DataFrame([[datetime.datetime.now(), user, message, video_link]],
                               columns=['date', 'user', 'message', 'video_link'])
    messages = pd.concat([messages, new_message], ignore_index=True)
    save_messages(messages)

def delete_message(index):
    messages = load_messages()
    messages = messages.drop(index).reset_index(drop=True)
    save_messages(messages)

# Afficher les messages existants
st.title('Forum de Discussion')
messages = load_messages()
if not messages.empty:
    for idx, row in messages.iterrows():
        st.write(f"{row['date']} - {row['user']}: {row['message']}")
        # Vérifiez si un lien vidéo est présent et non vide avant de l'afficher
        if pd.notnull(row['video_link']) and row['video_link'].strip():
            try:
                st.video(row['video_link'])
            except Exception as e:
                st.error("Erreur lors de l'affichage de la vidéo. Veuillez vérifier le lien.")

# Interface utilisateur pour ajouter un nouveau message
user = st.text_input('Votre nom')
message = st.text_area('Votre message')
video_link = st.text_input('Lien vidéo (optionnel)')

if st.button('Poster'):
    if user and message:  # Vérifiez que l'utilisateur et le message ne sont pas vides
        save_message(user, message, video_link)
        st.success("Message posté avec succès!")
        st.experimental_rerun()
    else:
        st.error("Veuillez remplir à la fois votre nom et votre message.")

# Option pour supprimer un message
if not messages.empty:
    options = ["Sélectionnez un message"] + [f"Message {i+1}" for i in range(len(messages))]
    message_to_delete = st.selectbox('Sélectionnez un message à supprimer:', options, index=0)
    if message_to_delete != "Sélectionnez un message":
        if st.button('Supprimer le message'):
            # Convertir le choix en index et ajuster pour l'indexation à base zéro
            delete_message(int(message_to_delete.split(" ")[-1]) - 1)
            st.experimental_rerun()
