import pandas as pd
from operator import getitem
from datetime import date
from calendar import monthrange
import sqlite3

#importar a função para criar as bases de dados
from bases import cria_bases
cria_bases()

class Clinica:
    def __init__(self):
        self.nome_paciente = ''
        self.identidade = ''
        self.profissao = ''
        self.nome_medico = ''
        self.nome_plano = ''
        self.crm = ''
        self.num_credencial = ''
        self.especialidade = ''
        self.fone = ''
        self.telefone = ''
        self.email = ''
        self.endereco = ''
        self.data_nascimento = ''
        self.convenio = ''
        self.outros = ''
        self.plano = ''
        self.data = ''
        self.hora = ''
        #aqui embaixo temos as estrutura de dados
        self.prontuario = {}
        self.base_medicos = {}
        self.nomes_pacientes = {}
        self.nomes_medicos = {}
        self.nomes_planos = ['SUS', 'UNIMED', 'CAUZZO']
        #aqui embaixo valores para os agendamentos
        self.agenda = {}
        self.dias_agendamento = ['SEGUNDA', 'QUARTA', 'SEXTA']
        self.horarios = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
        self.valor_consulta = 250
        self.num_consultas = 0
        self.receitas_consultas = 0
        self.rel_agendamento = []
        self.hist_receita_consultas = {}
        
        #ler dados na base de dados
        conexao1 = None
        conexao2 = None
        try:
            conexao1 = sqlite3.connect('base_pacientes.db')
            cursor_base = conexao1.cursor()
            for paciente in cursor_base.execute("SELECT nome_paciente FROM pacientes"):
                self.prontuario.update({
                    paciente[0]: {
                        'Nome: ': paciente[0],
                        'Data de Nascimento: ': paciente[5],
                        'Telefone para contato: ': paciente[2],
                        'Endereco residencial: ': paciente[4],
                        'Observações: ': paciente[7],
                        'Número de Consultas: ': ''}
                })
            conexao1.commit()

            conexao2 = sqlite3.connect('base_medicos.db')
            cursor_base = conexao2.cursor()
            for medico in cursor_base.execute("SELECT nome_medico FROM medicos"):
                for nome in medico[0::]:
                    self.nomes_medicos.append(nome)
            for medico in cursor_base.execute('SELECT * FROM medicos'):
                self.base_medicos.update({
                    medico[0]:medico[2]})
              
            conexao2.commit()

        except Exception as e:
            print("Ocorreu um erro:", e)
        finally:
            if conexao1:
                conexao1.close()
            if conexao2:
                conexao2.close()
    
    def cadastra_paciente(self):
        self.nome_paciente = input('Digite o nome do paciente: ').upper()
        if self.nome_paciente in self.nomes_pacientes:
            print('Paciente já cadastrado, deseja alterar o cadastro?')
            print('1 - Sim')
            print('2 - Não')
            
            opcao = int(input('Opção: '))
            match opcao:
                case 1:
                    print(f'{self.nome_paciente}')
                    self.identidade = input('Digite a identidade do paciente: ').upper()
                    self.data_nascimento = input('Digite a data de nascimento do paciente: ').upper()
                    self.fone = input('Digite o telefone do paciente: ').upper()
                    self.email = input('Digite o email do paciente: ').upper()
                    self.endereco = input('Digite o endereço do paciente: ').upper()
                    self.profissao = input('Digite a profissão do paciente: ').upper()
                    self.outros = input('Digite as observações do paciente: ').upper()
                    conexao = sqlite3.connect('base_pacientes.db')
                    cursor_base = conexao.cursor()
                    cursor_base.execute("REPLACE INTO pacientes (nome_paciente, identidade, telefone, email, endereco, profissao, outros) VALUES (?, ?, ?, ?, ?, ?, ?)",{
                        'nome_paciente': self.nome_paciente,
                        'identidade':self.identidade,
                        'telefone':self.fone,
                        'email':self.email,
                        'endereco':self.endereco,
                        'profissao':self.profissao,
                        'outros':self.outros})
                    conexao.commit()
                    conexao.close()
                    print('Paciente cadastrado com sucesso! \n')
            
                 
           