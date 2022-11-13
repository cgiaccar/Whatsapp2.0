# Gestione della chatroom:
#   se l'utente è loggato avremo nome e flag_admin nel session_state
#   displaying del log dei messaggi
#   campo di scrittura di un nuovo messaggio
#   pulsante di invio messaggio
#   pulsante di uscita/logout
#   ban dei messaggi se l'utente è admin


import streamlit as st
import pandas as pd
import csv
import datetime as dt
import os

st.set_page_config(page_title="Chatroom", page_icon="🎤")

st.subheader("Questa è la chatroom di Whatsapp2.0")

if 'nomeUtente' not in st.session_state:
    st.session_state['nomeUtente'] = 'Anonimo'
else:
    st.text('Ciao ' + st.session_state['nomeUtente'] +'!')
    
if 'flag_admin' not in st.session_state:
    st.session_state['flag_admin'] = False

fileMessaggi = os.path.dirname(os.path.dirname(__file__)) + "/csv/logChat.csv"

try:
    dfMessaggi = pd.read_csv(fileMessaggi)
except FileNotFoundError:
    import os
    exit('File ' + fileMessaggi + ' non trovato.')

table = st.dataframe(dfMessaggi, use_container_width=True)

messaggio = st.text_input("Scrivi un messaggio!")
invia = st.button("Invia")
if invia:
    file = open(fileMessaggi, 'a')
    writer = csv.writer(file)
    # necessario trasformare in string per far funzionare table.add_rows(row)
    orario = str(dt.datetime.now())
    row = pd.DataFrame(data={'Mittente': [st.session_state['nomeUtente']],
                             'Messaggio': [messaggio], 'Orario': [orario]})
    writer.writerow([st.session_state['nomeUtente'],
                    messaggio, dt.datetime.now()])
    file.close()
    table.add_rows(row)

if st.session_state['flag_admin'] == True:
    selected_indices = st.multiselect(
        'Seleziona i messaggi da bannare:', dfMessaggi.index)
    selected_rows = dfMessaggi.loc[selected_indices]
    st.write('Messaggi selezionati', selected_rows)
    banhammer = st.button("Banna messaggi")
    if banhammer:
        # per non andare out of bounds nel drop
        ordered_rows = selected_rows.sort_index(ascending=False)
        for x in ordered_rows.index:
            dfMessaggi.drop(dfMessaggi.index[x], inplace=True)
            dfMessaggi.to_csv(fileMessaggi, index=False)
            st.text('Il messaggio ' + str(x) + ' è stato cancellato.')

if st.button("Logout"):
    st.session_state['nomeUtente'] = 'Anonimo'
    st.session_state['flag_admin'] = False
    st.experimental_rerun()