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

elif menu == 'Cadastrar Paciente':
    with st.form(key = 'cadastro_paciente'):
        st.title('Cadastro de Pacientes')
        nome = st.text_input('Digite o nome completo do paciente: ').upper()
        identidade = st.text_input('Digite o número da identidade: ')
        data_nasc = st.text_input('Digite a data de nascimento: ')
        fone = st.text_input('Digite o telefone: ')
        email = st.text_input('Digite o email:').upper()
        endereco = st.text_input('Digite o endereço: ').upper()
        profissao = st.text_input('Digite a atividade profissional: ').upper()
        outros = st.text_input('Digite outras informações: ').upper()
        botao_enviar = st.form_submit_button('Enviar')
    
