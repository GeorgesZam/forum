import streamlit as st
import pandas as pd
import datetime
import os
import uuid

# Chemin vers le dossier où les fichiers seront stockés
FILE_PATH = 'messages.csv'
UPLOAD_FOLDER = 'uploaded_files/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_messages():
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        messages = pd.read_csv(FILE_PATH)
    else:
        messages = pd.DataFrame(columns=['date', 'user', 'message', 'image_path'])
    return messages

def save_message(user, message, image_file=None):
    messages = load_messages()
    image_path = ""
    if image_file is not None:
        # Générer un nom de fichier unique
        filename = f"{uuid.uuid4()}{os.path.splitext(image_file.name)[1]}"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())
    new_message = pd.DataFrame([[datetime.datetime.now(), user, message, image_path]],
                               columns=['date', 'user', 'message', 'image_path'])
    messages = pd.concat([messages, new_message], ignore_index=True)
    messages.to_csv(FILE_PATH, index=False)

st.title('Forum de Discussion')

user = st.text_input('Votre nom')
message = st.text_area('Votre message')
image_file = st.file_uploader("Téléchargez une image", type=['jpg', 'png'])

if st.button('Poster'):
    save_message(user, message, image_file)

messages = load_messages()
if not messages.empty:
    for idx, row in messages.iterrows():
        st.write(f"{row['user']}: {row['message']}")
        if row['image_path']:
            st.image(row['image_path'])
