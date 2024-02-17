import streamlit as st
import pandas as pd
import os

# Chemin vers le fichier CSV pour stocker les messages et les liens vidéo
CSV_FILE = 'messages.csv'

# Fonction pour charger ou initialiser le fichier CSV
def load_or_initialize_csv(csv_file):
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame(columns=['Message', 'VideoLink'])

# Charger ou initialiser le DataFrame
df = load_or_initialize_csv(CSV_FILE)

# Interface utilisateur pour ajouter un nouveau message
st.title("Forum avec Streamlit")
message = st.text_area("Laissez votre message ici:")
video_link = st.text_input("Lien vidéo (optionnel):")
if st.button("Poster"):
    # Ajouter le nouveau message et le lien vidéo au DataFrame
    new_data = {'Message': message, 'VideoLink': video_link}
    df = df.append(new_data, ignore_index=True)
    # Sauvegarder le DataFrame mis à jour dans le fichier CSV
    df.to_csv(CSV_FILE, index=False)
    st.success("Message posté avec succès!")

# Afficher les messages existants
st.write("Messages:")
for index, row in df.iterrows():
    st.write(f"Message {index + 1}: {row['Message']}")
    if row['VideoLink']:
        st.video(row['VideoLink'])
