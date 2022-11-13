# Gestione della chatroom:
#   se l'utente Ã¨ loggato avremo nome e flag_admin nel session_state
#   displaying del log dei messaggi
#   campo di scrittura di un nuovo messaggio
#   pulsante di invio messaggio
#   pulsante di uscita/logout
#   ban dei messaggi se l'utente Ã¨ admin


import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Chatroom", page_icon="ð¤")

st.subheader("Questa è la pagina di gestione utenti di Whatsapp2.0")

if 'flag_admin' not in st.session_state:
  st.warning('Utente non registrato tramite login', icon="⚠️")
  st.stop()
else:
  if st.session_state['flag_admin'] != True:
      st.warning('Accesso consentito solo ad utenti admin', icon="⚠️")
      st.stop()

fileUtenti = os.path.dirname(os.path.dirname(__file__)) + "/csv/utenti.csv"

try:
    dfUtenti = pd.read_csv(fileUtenti)
except FileNotFoundError:
    import os
    exit('File ' + fileUtenti + ' non trovato.')

table = st.dataframe(dfUtenti.iloc[:, [0, 2]], use_container_width=True)

def numeroUtentiAdmin(ordered_rows):
    numUtentiAdmin=0
    for x in ordered_rows.index:
        if dfUtenti.iloc[x,2]==True:
            numUtentiAdmin=numUtentiAdmin+1
    return numUtentiAdmin


if st.session_state['flag_admin'] == True:
    selected_indices = st.multiselect(
        'Seleziona gli utenti da bannare:', dfUtenti.index)
    selected_rows = dfUtenti.loc[selected_indices]
    st.write('Utenti selezionati', selected_rows.iloc[:, [0, 2]])
    col1, col2 = st.columns(2)
    with col1:
        banhammer = st.button("Banna utenti")
        if banhammer:
            # per non andare out of bounds nel drop
            ordered_rows = selected_rows.sort_index(ascending=False)
            if numeroUtentiAdmin(ordered_rows)==0:
                for x in ordered_rows.index:
                    utenteCancellato=dfUtenti.iloc[x,0]
                    dfUtenti.drop(dfUtenti.index[x], inplace=True)
                    dfUtenti.to_csv(fileUtenti, index=False)
                    st.text("L'utente " + utenteCancellato + ' è stato cancellato.') 
            else:
                st.warning('Gli utenti admin non possono essere bannati. Modificare la selezione.', icon="⚠️")
                st.stop()
    with col2:
        st.button("Aggiorna lista utenti")
        
logout = st.button("Logout")
if logout:
    st.session_state['nomeUtente'] = 'Anonimo'
    st.session_state['flag_admin'] = False
    st.text('Logout effettuato! Ora sei Anonimo')
