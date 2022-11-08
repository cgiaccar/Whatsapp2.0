from st_aggrid import GridUpdateMode, DataReturnMode
import streamlit as st
import pandas as pd

###############################################################################
# ATTENZIONE INSTALLARE IL COMPONENTE streamlit-aggrid CON IL SOTTOSTANTE COMANDO
# pip install streamlit-aggrid
###############################################################################

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
# from st_aggrid.shared import JsCode


def _max_width_():
    max_width_str = "max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_icon=":smile:", page_title="Whatsapp2.0")
st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/balloon_1f388.png", width=100)
st.title("Whatsapp2.0 - Visualizza messaggi")

utente = st.text_input('Nome utente')
password = st.text_input('Password', type="password")

col1, col2 = st.columns(2)

richiestoAccesso = False
richiestaRegistrazione = False


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

    gb = GridOptionsBuilder.from_dataframe(listaUtenti)
    # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
    gb.configure_default_column(
        enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
    gridOptions = gb.build()

    response = AgGrid(
        listaUtenti,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
    )

    if len(response['selected_rows']) > 0:
        destinatarioMessaggio = response['selected_rows'][0].get('Amici')

        nomeFileMessaggi = "messaggi.csv"
        listaMessaggi = pd.read_csv(nomeFileMessaggi)

        # for col in listaMessaggi.columns:
        #     st.text(col)
        nomeColDestinatario = listaMessaggi.columns[0]
        nomeColMittente = listaMessaggi.columns[1]
        listaMessaggiFiltrata = listaMessaggi.loc[listaMessaggi[nomeColDestinatario]
                                                  == destinatarioMessaggio]
        st.subheader("La chat selezionata apparirà qui sotto 👇 ")
        st.table(listaMessaggiFiltrata[listaMessaggi.columns])
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
