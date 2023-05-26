import pandas as pd
import sqlite3
from calendar import monthrange
from datetime import date
from operator import getitem
import streamlit as st 
import datetime

from app import Clinica

sistema = Clinica()

st.sidebar.title('Menu Principal')

menu = st.sidebar.selectbox('Selecione uma opção', ['Página Principal',
                                                    'Agendar Consulta',
                                                    'Cadastrar Paciente',
                                                    'Cadastrar Médico',
                                                    'Exibir Prontuários'])

if menu == 'Página Principal':
    st.title('Sistema Clínica')
    st.text('Agenda')
    st.write(sistema.agenda)
