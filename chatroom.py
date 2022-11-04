#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:55:54 2022

@author: Camilla
"""

# Gestione della chatroom:
#   l'utente arriva qui dalla pagina di login
#   displaying del log dei messaggi
#   campo di scrittura di un nuovo messaggio
#   pulsante di invio messaggio
#   pulsante di uscita/logout che riporta alla pagina di login


import streamlit as st
import pandas as pd
import csv
import datetime as dt
# import pickle as pkl
# import os.path


st.title("Benvenuto!")
st.subheader("Questa è la chatroom di Whatsapp2.0")

# displaying del log dei messaggi
fileMessaggi = "logChat.csv"
df = pd.read_csv(fileMessaggi)
st.table(df)

# campo di scrittura di un nuovo messaggio
messaggio = st.text_input("Scrivi un messaggio!")
# pulsante di invio messaggio
invia = st.button("Invia")
if invia:
    file = open(fileMessaggi, 'a')
    writer = csv.writer(file)
    writer.writerow([" ", messaggio, dt.datetime.now()])
    file.close()

# logout = st.button("Logout")
# if logout:
#     pkl.load(open('login.py', 'rb'))

# # if os.path.isfile("login.py"):
# #    pkl.load(open("login.py"))
