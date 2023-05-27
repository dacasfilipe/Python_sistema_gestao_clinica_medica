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
    if botao_enviar:
        sistema.nome_paciente = nome
        sistema.identidade = identidade
        sistema.data_nasc = data_nasc
        sistema.fone = fone
        sistema.email = email
        sistema.endereco = endereco
        sistema.profissao = profissao
        sistema.outros = outros
    
conexao = sqlite3.connect('base_pacientes.db')
cursor_base = conexao_cursor(conexao)
cursor_base.execute("REPLACE INTO pacientes (nome_paciente, identidade, fone, email, endereco, data_nascimento, profissao, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    {'nome_pac' : sistema.nome_paciente,
                     'identidade' : sistema.identidade,
                     'fone' : sistema.fone,
                     'email': sistema.email,
                     'endereco' : sistema.endereco,
                     'data_nasc' : sistema.data_nasc,
                     'profissao' : sistema.profissao,
                     'observacoes' : sistema.outros})

sistema.nomes_pacientes.append(sistema.nome_paciente)

sistema.prontuario.update({
        sistema.nome_paciente: {
            'Nome': sistema.nome_paciente,
            'Data de Nascimento: ': sistema.data_nasc,
            'Telefone para contato: ': sistema.fone,
            'Endereço Residencial: ': sistema.endereco,
            'Observações: ': sistema.outros,
            'Número de Consultas: ': sistema.num_consultas,
            'Prontuário: ': sistema.rel_agendamento}
    })
st.text('Cadastro Realizado / alterado com sucesso!')

elif menu == 'Cadastrar Médico':
    with st.form(key = 'cadastro_medico'):
        st.title('Cadastro de Médico')
        nome = st.text_input('Digite o nome completo do médico: ').upper()
        crm = st.text_input('Digite o número do CRM: ')
        especialidade = st.text_input('Digite a especialidade: ').upper()
        botao_enviar = st.form_submit_button('Enviar')
    