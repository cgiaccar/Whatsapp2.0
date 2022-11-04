# Pagina di login e registrazione
# Codice preso dal file "visualizzaMessaggi"
# Dovrà inserire nel session_state il nome dell'utente
#   attualmente loggato e se è o no un admin (serve a chatroom)


import streamlit as st
import pandas as pd

# settaggio della pagina principale con icona
st.set_page_config(
    page_title="Login",
    page_icon="👋",
)

utente = st.text_input('Nome utente')
password = st.text_input('Password', type="password")

col1, col2 = st.columns(2)

richiestoAccesso = False
richiestaRegistrazione = False
st.session_state['nomeUtente'] = 'Anonimo'


with col1:
    if st.button('Accedi'):
        richiestoAccesso = True

with col2:
    if st.button('Registrati'):
        richiestaRegistrazione = True

nomeFileUtenti = "utenti.csv"
listaUtenti = pd.read_csv(nomeFileUtenti)

if ('accessoEseguito' in st.session_state
        or (richiestoAccesso and utente in listaUtenti['Amici'].unique())):

    if 'accessoEseguito' not in st.session_state:
        st.session_state['accessoEseguito'] = [True]
        st.session_state['nomeUtente'] = utente
        st.text("\n Ciao " + utente + "!")
        st.text("Entra pure nella chatroom :)")

else:
    if utente != '' and utente not in listaUtenti['Amici'].unique():
        st.warning('Utente non censito in archivio', icon="⚠️")

if richiestaRegistrazione:
    if utente in listaUtenti['Amici'].unique():
        st.warning('Utente già censito in archivio', icon="⚠️")
    else:
        if password == '':
            st.warning('Utente/Password obbligatori', icon="⚠️")
        else:
            f = open(nomeFileUtenti, 'a')
            f.write('\n'+utente)
            f.close()
            st.warning('Utente inserito in archivio')

# TODO manca la gestione delle password
