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

if 'nomeUtente' not in st.session_state:
    st.session_state['nomeUtente'] = 'Anonimo'
if 'flag_admin' not in st.session_state:
    st.session_state['flag_admin'] = False

st.subheader("Questa è la chatroom di Whatsapp2.0")

fileMessaggi = os.path.dirname(os.path.dirname(__file__)) + "/csv/logChat.csv"

try:
    df = pd.read_csv(fileMessaggi)
except FileNotFoundError:
    import os
    exit('File ' + fileMessaggi + ' non trovato.')

table = st.dataframe(df, use_container_width=True)

messaggio = st.text_input("Scrivi un messaggio!")
invia = st.button("Invia")
if invia:
    file = open(fileMessaggi, 'a')
    writer = csv.writer(file)
    # � necessario trasformare in string per far funzionare table.add_rows(row)
    orario = str(dt.datetime.now())
    row = pd.DataFrame(data={'Mittente': [st.session_state['nomeUtente']],
                             'Messaggio': [messaggio], 'Orario': [orario]})
    writer.writerow([st.session_state['nomeUtente'],
                    messaggio, dt.datetime.now()])
    file.close()
    table.add_rows(row)

# if True:#st.session_state['flag_admin'] == True:
#     selected_indices = st.multiselect('Select messages to ban:', df.index)
#     selected_rows = df.loc[selected_indices]
#     st.write('### Selected Messages', selected_rows)
#     banhammer = st.button("Ban Messages")
#     if banhammer:
#         #file = open(fileMessaggi, 'w')
#         for x in selected_rows.index:
#             df.drop(x)
#         #file.close()

logout = st.button("Logout")
if logout:
    st.session_state['nomeUtente'] = 'Anonimo'
    st.text('Logout effettuato! Ora sei Anonimo')
