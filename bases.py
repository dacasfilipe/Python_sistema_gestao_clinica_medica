# -*- coding: utf-8 -*-
import sqlite3

# criação das bases de dados
def cria_bases():
    try:
        conexao1 = sqlite3.connect('base_pacientes.db')
        cursor_base = conexao1.cursor()
        cursor_base.execute('''
                            CREATE TABLE pacientes (
                                nome_paciente TEXT,
                                identidade TEXT,
                                fone TEXT, 
                                email TEXT,
                                endereco TEXT,
                                data_nascimento TEXT,
                                profissao TEXT,
                                observacoes TEXT,  
                                PRIMARY KEY (nome_paciente)
                            )
                            ''')
        conexao1.commit()
        
        
        conexao2 = sqlite3.connect('base_medicos.db')
        cursor_base = conexao2.cursor()
        cursor_base.execute('''
                            CREATE TABLE medicos (
                                nome_medico TEXT,
                                crm TEXT,
                                especialidade TEXT, 
                                PRIMARY KEY (nome_medico)
                            )
                            ''')
        conexao2.commit()
        
        conexao3 = sqlite3.connect('base_agenda.db')
        cursor_base = conexao3.cursor()
        cursor_base.execute('''
                            CREATE TABLE agenda (
                                consulta_num integer,
                                nome_pac text,
                                consulta_com text,
                                dia text,
                                hora text 
                                )
                            ''')
        conexao3.commit()
        conexao3.close()
        
        
    except sqlite3.Error as e:
        print(f"Ocorreu um erro: {e}")
        pass
    finally:
        if conexao1:
            conexao1.close()
        if conexao2:
            conexao2.close()
