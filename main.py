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
        conexao3 = None
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
            conexao1.close()

            conexao2 = sqlite3.connect('base_medicos.db')
            cursor_base = conexao2.cursor()
            for medico in cursor_base.execute("SELECT nome_medico FROM medicos"):
                for nome in medico[0::]:
                    self.nomes_medicos.append(nome)
            for medico in cursor_base.execute('SELECT * FROM medicos'):
                self.base_medicos.update({
                    medico[0]:medico[2]})
              
            conexao2.commit()
            conexao2.close()
            
            conexao3 = sqlite3.connect('base_agenda.db')
            cursor_base = conexao3.cursor()
            for consulta in cursor_base.execute("SELECT * FROM agenda"):
                self.agenda.update({
                    consulta[0]: {
                        'Id: ': consulta[0],
                        'Nome: ': consulta[1],
                        'Médico(a): ': consulta[2],
                        'Dia: ': consulta[3],
                        'Hora: ': consulta[4],
                        }
                })
            conexao3.commit()
            conexao3.close()
        finally:
            pass
                
            
                
    
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
                #escolher o dia da semana
                self.data = input('Qual dia da semana deseja consultar?').upper()
                while self.data not in self.dias_agendamento:
                    print('Agendamento apenas Segunda, Quarta e Sexta. \n')
                    self.data = input('Qual dia da semana deseja consultar? ').upper()
                self.hora = int(input('Em qual horário?'))
                #escolher o horário da consulta
                while self.hora not in self.horarios:
                    print('Atendimento das 8 às 11h e das 14 às 17h \n')
                    self.hora = int(input('Em qual horário?'))
                    
        #atualizar a agenda base com as informações do agendamento
        self.agenda.update({f'Dia: {self.data}, às {self.hora} ':[f'Paciente: {self.nome_paciente}',f' Dr(a): {self.nome_med}',f'Plano: {self.nome_plano}',f'Consulta: {self.consulta}',f'Valor: R${self.valor_consulta}']})
        
        #atualizar a série de objetos 
        self.num_consultas += 1
        self.receitas_consultas += self.valor_consulta
        
        #gerar relatório de agendamentos de consultas realizadas
        self.dia = date.today().strftime("%d/%m/%Y")
        self.rel_agendamento.append(f'Consulta com {self.nome_med}, {self.data}, no dia {self.dia} às {self.hora} horas')
        
        #exibição das consultas agendadas
        print(f'Consulta agendada para {self.data} às {self.hora} horas com o(a) Dr(a) {self.nome_med} \n')
        print(f'Valor da consulta: R${self.valor_consulta} \n')
        
        #atualizar o prontuário do paciente
        self.prontuario.update({
            self.nome_paciente:{
                'Nome':self.nome_paciente,
                'Data de Nascimento':self.data_nasc,
                'Telefone':self.telefone,
                'Endereço':self.endereco,
                'Observações':self.outros,
                'Número de consultas':self.num_consultas,
                'Prontuário':self.rel_agendamento
            }
        })
        
        #ordenar a relação dos prontuários dos pacientes em ordem alfabética
        #o método sorted itera sobre cada chave Nome de cada item a partir desta chave
        self.prontuario = sorted(self.prontuario.items(),key = lambda x: getitem(x[1],'Nome:'))
        
        #retorna o escopo global da classe com os últimos dados fornecidos para as duas bases
        return self.agenda, self.prontuario, self.receitas_consultas, self.rel_agendamento, self.nomes_pacientes
    
    #função para exibir os prontuários    
    def exibe_prontuario(self):
        print('PRONTUÁRIOS')
        if len(self.prontuario.keys()) == 0:
            print('Não existem registros de prontuários')
            
        for i in self.prontuario.items():
            print(i)
    
    #função para exibir a agenda de consultas
    def exibe_agenda(self):
        print('AGENDA')
        if len(self.agenda.keys()) == 0:
            print('A agenda está vazia \n')
            
        for i in self.agenda.keys():
            print(i)                       
    
    #função para exibir a relação de médicos conveniados
    def exibe_medicos(self):
        print('MÉDICOS CONVENIADOS')
        if len(self.nomes_medicos) == 0:
            print('Não existem médicos cadastrados. \n')
            
        for i in self.base_medicos.items():
            print(i)
            
    #relatório gerencial com informações da clínica
    def relatorio_gerencial(self):
        print(f'Número total de consultas: {self.num_consultas} \n')
        print(f'Receita gerada pelas consultas: R${self.receitas_consultas} \n')
        print('-----------------------------------------------')
        print(f'Número de pacientes cadastrados: {len(self.nomes_pacientes)} \n')
        print(f'Número de médicos conveniados: {len(self.nomes_medicos)} \n')
        print('-----------------------------------------------')
        data_atual = date.today()
        ultimo_dia = data_atual.replace(day = monthrange(data_atual.year, data_atual.month)[1])
        if data_atual == ultimo_dia:
            print(self.receitas_consultas)
            self.receitas_consultas == 0
            self.hist_receita_consultas.update({f'MÊS {data_atual.month}':f'R${self.receitas_consultas}'})
        if data_atual != ultimo_dia:
            print(f'Receita acumulada: R${self.receitas_consultas} \n')
            self.hist_receita_consultas.update({f'MÊS {data_atual.month}':f'R${self.receitas_consultas}'})
            print(self.hist_receita_consultas.items())
            
#função para inicialicar a aplicação e exibir o menu de opções
def main():
    sistema = Clinica()
    while True:
        print('1 - Agendar consulta')
        print('-----------------------------------------------')
        print('2 - Cadastro de Pacientes')
        print('3 - Cadastro de Médicos')
        print('-----------------------------------------------')
        print('4 - Exibir Agenda')
        print('5 - Prontuários de Pacientes')
        print('6 - Relaç˜ao de Médicos Cadastrados')
        print('7 - Relatório Gerencial')
        print('-----------------------------------------------')
        print('9 - Sair \n')
        try:
            opcao = int(input('Digite a opção desejada: '))
            match opcao:
                case 1: 
                    sistema.agenda_consulta()
                case 2: 
                    sistema.cadastra_paciente()
                case 3: 
                    sistema.cadastra_medico()
                case 4: 
                    sistema.exibe_agenda()
                case 5: 
                    sistema.exibe_prontuario()
                case 6: 
                    sistema.relacao_medicos()
                case 7: 
                    sistema.relarotio_geencial()
                case 9: 
                    break
        except: 
            print('Escolha uma opção válida: \n')
            continue
main()