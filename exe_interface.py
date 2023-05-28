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
    with st.form(key='cadastro_paciente'):
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
cursor_base = conexao.cursor(conexao)
cursor_base.execute("REPLACE INTO pacientes (nome_paciente, identidade, fone, email, endereco, data_nascimento, profissao, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    {'nome_pac': sistema.nome_paciente,
                     'identidade': sistema.identidade,
                     'fone': sistema.fone,
                     'email': sistema.email,
                     'endereco': sistema.endereco,
                     'data_nasc': sistema.data_nasc,
                     'profissao': sistema.profissao,
                     'observacoes': sistema.outros})

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
    with st.form(key='cadastro_medico'):
            st.title('Cadastro de Médico')
            nome = st.text_input('Digite o nome completo do médico: ').upper()
            crm = st.text_input('Digite o número do CRM: ')
            especialidade = st.text_input('Digite a especialidade: ').upper()
            botao_enviar = st.form_submit_button('Enviar')
    if botao_enviar:
        sistema.nome_med = nome
        sistema.crm = crm
        sistema.especialidade = especialidade

    conexao = sqlite3.connect('base_medicos.db')
    cursor_base = conexao.cursor()
    cursor_base.execute("INSERT INTO medicos (nome_med, crm, especialidade) VALUES (?, ?, ?)", {
    'nome_med': sistema.nome_med,
    'crm': sistema.crm,
    'especialidade': sistema.especialidade
    })
    conexao.commit()
    conexao.close()

    sistema.nomes_medicos.append(sistema.nome_med)
    sistema.base_medicos.update({f'{sistema.especialidade}'})

    st.text('Cadastro Realizado com sucesso!')

elif menu == 'Agendar Consulta':
    with st.form(key = 'escolha_paciente'):
        st.write('Agendamento de Consultas')
        nome_pac = st.text_input('Digite o nome do paciente: ').upper()
        botao_verificar1 = st.form_submit_button(label = 'Verificar')
        if botao_verificar1:
            if nome_pac in sistema.nomes_pacientes:
                st.write('Paciente já cadastrado')
            else:
                st.write('Paciente não cadastrado')
                st.write('Por favor, cadastre o paciente para continuar o agendamento.')
    with st.form(key = 'escolha_medico')
        nome_med = st.text_input('Digite o nome do médico: ').upper()
        botao_verificar2 = st.form_submit_button(label = 'Verificar')
        if botao_verificar2:
            if nome_med in sistema.nomes_medicos:
                st.write('Médico já cadastrado')
            else:
                st.write('Médico não cadastrado')
                st.write('Por favor, cadastre o médico para continuar o agendamento.')    
    with st.form(key = 'escolha_plano')
        nome_plano = st.radio('Escolha um plano de saúde', ('Unimed', 'SUS', 'CAUZZO'))
        if nome_plano == 'SUS':
            sistema.valor_consulta = 0
            st.write('Aplicado o desconto de 100%')
        if nome_plano == 'CAUZZO':
            sistema.valor_consulta = sistema.valor_consulta - sistema.valor_consulta * 0.40
            st.write('Aplicado o desconto de 40%')
        if nome_plano == 'UNIMED':
            sistema.valor_consulta = sistema.valor_consulta - sistema.valor_consulta * 0.50
            st.write('Aplicado o desconto de 50%')
        botao_verificar3 = st.form_submit_button('Escolher')
    with st.form(key = 'escolhe_dia'):
        dia_consulta_ = st.date_input('Escolha o dia da consulta: ', datetime.date.today())
        dia_consulta = dia_consulta_.day
        botao_verificar4 = st.form_submit_button('Definir')
        st.write(f'Dia: {dia_consulta}')
    with st.form(key = 'escolhe_hora'):
        hora_consulta = st.slider('Escolha um horário: ',
                                  min_value = 8,
                                  max_value = 18,
                                  step = 1)
        botao_verificar5 = st.form_submit_button('Definir')
        st.write(f'Hora: {hora_consulta} horas')
    with st.form(key = 'conclui_agendamento'):
        if ((botao_verificar1 == True)
            and (botao_verificar2 == True)
            and (botao_verificar3 == True)
            and (botao_verificar4 == True)
            and (botao_verificar5 == True)):
            st.write('Agendamento realizado com sucesso!')
        botao_concluir = st.form_submit_button('Finalizar Agendamento')
            