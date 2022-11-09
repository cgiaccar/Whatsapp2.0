# Pagina principale del progetto
# login e registrazione:
#   campi di inserimento nome e password
#   login (warning se utente non esiste in utenti.csv)
#   registrazione in utenti.csv (warning se utente esiste già)
#   inserisce nel session_state il nome dell'utente
#       attualmente loggato e se è o no un admin


import streamlit as st
import pandas as pd
import csv
import os

st.set_page_config(page_title="Login", page_icon="👋")

st.title('Benvenuto in Whatsapp2.0!')
st.subheader('Entra o registrati qui sotto:')

utente = st.text_input('Nome utente')
password = st.text_input('Password', type="password")

col1, col2 = st.columns(2)

richiestoAccesso = False
richiestaRegistrazione = False

if 'nomeUtente' not in st.session_state:
    st.session_state['nomeUtente'] = 'Anonimo'
if 'flag_admin' not in st.session_state:
    st.session_state['flag_admin'] = False


with col1:
    if st.button('Accedi'):
        richiestoAccesso = True

with col2:
    if st.button('Registrati'):
        richiestaRegistrazione = True

fileUtenti = os.path.dirname(__file__) + "/csv/utenti.csv"

try:
    listaUtenti = pd.read_csv(fileUtenti)
except FileNotFoundError:
    exit('File ' + fileUtenti + ' non trovato.')

if ('accessoEseguito' in st.session_state
        or (richiestoAccesso and (((listaUtenti['Utente'] == utente)
                                   & (listaUtenti['Password'] == password)).any())
            )):

    if 'accessoEseguito' not in st.session_state:
        st.session_state['accessoEseguito'] = [True]
        st.session_state['nomeUtente'] = utente
        # TODOOOOOOO bisogna recuperare il ruolo dalla riga di utente
        st.session_state['flag_admin'] = False  # TODOOOOOOOOOOO
        # TODOOOOOOO
        st.text("\n Ciao " + utente + "!")
        st.text("Entra pure nella chatroom :)")

else:
    if utente != '' and utente not in listaUtenti['Utente'].unique():
        st.warning('Utente non censito in archivio', icon="⚠️")
    elif (password != '' and (((listaUtenti['Utente'] == utente)
                              & (listaUtenti['Password'] != password)).any())):
        st.warning('Password errata!', icon="⚠️")

if richiestaRegistrazione:
    if utente in listaUtenti['Utente'].unique():
        st.warning('Utente già censito in archivio', icon="⚠️")
    else:
        if password == '':
            st.warning('Utente/Password obbligatori', icon="⚠️")
        else:
            f = open(fileUtenti, 'a')
            writer = csv.writer(f)
            writer.writerow([utente, password, 'False'])
            f.close()
            st.warning('Utente inserito in archivio')
