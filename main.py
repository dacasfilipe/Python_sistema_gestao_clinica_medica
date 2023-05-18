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
        #verifica se o paciente já existe na base de dados
        if self.nome_paciente in self.nomes_pacientes:
            print('Paciente já cadastrado, deseja alterar o cadastro?')
            print('1 - Sim')
            print('2 - Não')
            
            opcao = int(input('Opção: '))
            match opcao:
                case 1:
                    #lógica do paciente já cadastrado/ alterar dados
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
                    
                case 2:
                    pass
        #cadastra o paciente na base de dados caso não exista
        if self.nome_paciente not in self.nomes_pacientes:
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
            cursor_base = cursor_base.execute("INSERT INTO pacientes (nome_paciente, identidade, telefone, email, endereco, profissao, outros) VALUES (?, ?, ?, ?, ?, ?, ?)",{
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
            
        #adiciona o paciente na lista de pacientes cadastrados    
        self.nomes_pacientes.append(self.nome_paciente)

        #adiciona o paciente na relação de prontuários de pacientes
        self.prontuario.update({
            self.nome_paciente: {
                'Nome: ': self.nome_paciente,
                'Data de Nascimento: ': self.data_nascimento,
                'Endereço Residencial: ': self.endereco,
                'Observações: ': self.outros,
                'Número de Consultas: ': self.num_consultas,
                'Prontuario: ': self.rel_agendamento}
        })
        
        #retorna o último estado para a instância base da classe
        return self.nomes_pacientes
        #fim dos métodos de cadastro pacientes
    def cadastra_medico(self):
        self.nome_med = input('Digite o nome completo do médico: ').upper()
        if self.nome_med in self.nomes_medicos:
            print('Médico já cadastrado, deseja alterar o cadastro?')
            print('1 - Sim')
            print('2 - Não')
            opcao = int(input('Opção: '))
            match opcao:
                case 1:
                    print(f'Dr(a){self.nome_med}')
                    self.crm = input('Digite o CRM do médico: ').upper()
                    self.especialidade = input('Digite a especialidade do médico: ').upper()
                    
                    conexao = sqlite3.connect('base_medicos.db')
                    cursor_base = conexao.cursor()
                    cursor_base.execute("REPLACE INTO medicos (nome_medico, crm, especialidade) VALUES (?, ?, ?)",{
                        'nome_medico': self.nome_med,
                        'crm':self.crm,
                        'especialidade':self.especialidade
                    })
                    conexao.commit()
                    conexao.close()
                    print('Cadastro alterado com sucesso! \n')
                case 2:
                    pass
        #cadastra o médico na base de dados caso não exista
        if self.nome_med not in self.nomes_medicos:
            print(f'Dr(a){self.nome_med}')
            self.crm = input('Digite o CRM do médico: ').upper()
            self.especialidade = input('Digite a especialidade do médico: ').upper()
            
            conexao = sqlite3.connect('base_medicos.db')
            cursor_base = conexao.cursor()
            cursor_base.execute("INSERT INTO medicos (nome_medico, crm, especialidade) VALUES (?, ?, ?)",{
                'nome_medico': self.nome_med,
                'crm':self.crm,
                'especialidade':self.especialidade
            })
            conexao.commit()
            conexao.close()
            print('Médico cadastrado com sucesso! \n')
            self.nomes_medicos.append(self.nome_med)
            self.base_medicos.update({f'{self.nome_med}':f'{self.especialidade}'})
            #retorna o escopo global da classe com os últimos dados fornecidos para as duas bases
            return self.nomes_medicos,self.base_medicos                    
    
    #função para o agendamento de consultas
    def agenda_consultas(self):
        self.nome_paciente = input('Digite o nome completo do paciente: ').upper()
        if self.nome_paciente not in self.nomes_pacientes:
            print('Paciente não cadastrado, deseja cadastrar?\n')
            self.cadastra_paciente()
            print('Retomando o Agendamento... \n')
            #Aqui o paciente já está cadastrado, perguntamos então qual o médico que gostaria de consultar
            self.nome_med = input('Qual o nome do médico(a) que gostaria de consultar?').upper()
            if self.nome_med not in self.nomes_medicos:
                print('Médico não cadastrado, deseja cadastrar?\n')
                self.cadastra_medico()
                print(f'Retomando com o Agendamento para o Dr. {self.nome_med} \n')
                #verificação do plano de saúde
                print('SUS / UNIMED / CAUZZO')
                self.nome_plano = input('Qual o plano de saúde? Digite o nome caso houver.').upper()
                if self.nome_plano in self.nomes_planos:
                    match self.nome_plano:
                        case 'SUS':
                            self.valor_consulta = 0
                            print('Aplicado desconto de 100% \n')
                            print(f'Valor da consulta: R${self.valor_consulta}')
                        case 'UNIMED':
                            self.valor_consulta = self.valor_consulta / 2
                            print('Aplicado desconto de 50% \n')
                            print(f'Valor da consulta: R${self.valor_consulta}')
                        case 'CAUZZO':
                            self.valor_consulta = self.valor_consulta - self.valor_consulta * 0.40
                            print('Aplicado desconto de 40% \n')
                            print(f'Valor da consulta: R${self.valor_consulta}')
                            