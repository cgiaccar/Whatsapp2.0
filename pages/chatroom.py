# Gestione della chatroom:
#   se l'utente è loggato avremo nome e flag_admin nel session_state
#   displaying del log dei messaggi
#   campo di scrittura di un nuovo messaggio
#   pulsante di invio messaggio
#   pulsante di uscita/logout
#   ban dei messaggi se l'utente è admin

# TODO non aggiorna la tabella automaticamente all'invio del messaggio


import streamlit as st
import pandas as pd
import csv
import datetime as dt
# import pickle as pkl
# import os.path

# setting della pagina con icona
st.set_page_config(page_title="Chatroom", page_icon="🎤")

if 'nomeUtente' not in st.session_state:
    st.session_state['nomeUtente'] = 'Anonimo'
if 'role' not in st.session_state:
    st.session_state['role'] = False

st.title("Benvenuto!")
st.subheader("Questa è la chatroom di Whatsapp2.0")

# displaying del log dei messaggi
fileMessaggi = "logChat.csv"
try:
    df = pd.read_csv(fileMessaggi)
except FileNotFoundError:
    import os
    exit('File ' + fileMessaggi + ' non trovato in ' + os.getcwd())

table = st.dataframe(df, use_container_width=True)

# campo di scrittura di un nuovo messaggio
messaggio = st.text_input("Scrivi un messaggio!")
# pulsante di invio messaggio
invia = st.button("Invia")
if invia:
    file = open(fileMessaggi, 'a')
    writer = csv.writer(file)
    #timey serve come variabile String da mettere in row per far funzionare table.add_rows(row)
    timey = str(dt.datetime.now())
    row = pd.DataFrame(data={'Mittente':[st.session_state['nomeUtente']], 
                             'Messaggio':[messaggio], 'Orario':[timey]})
    writer.writerow([st.session_state['nomeUtente'],
                    messaggio, dt.datetime.now()])
    file.close()
    table.add_rows(row)

# if True:#st.session_state['role'] == True:
#     selected_indices = st.multiselect('Select messages to ban:', df.index)
#     selected_rows = df.loc[selected_indices]
#     st.write('### Selected Messages', selected_rows)
#     banhammer = st.button("Ban Messages")
#     if banhammer:
#         #file = open(fileMessaggi, 'w')
#         for x in selected_rows.index:
#             df.drop(x)
#         #file.close()


# logout = st.button("Logout")
# if logout:
#     pkl.load(open('login.py', 'rb'))

# # if os.path.isfile("login.py"):
# #    pkl.load(open("login.py"))
