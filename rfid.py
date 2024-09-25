import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep, time
import signal
import sys
import csv
import requests
import mysql.connector
import os

# Configuração da conexão com o banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='atitus_bd',  # Substitua pelo nome do seu banco de dados
    user='Pedro Sena',      # Substitua pelo seu usuário
    password='Luciane20.'   # Substitua pela sua senha
)

cursor = conexao.cursor()

# Configurações de hardware
GPIO.setmode(GPIO.BOARD)
LED_VERDE = 8
LED_VERMELHO = 10
BUZZER = 38

GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# Iniciando o leitor RFID
leitorRfid = SimpleMFRC522()

# Controle de acessos
tempo_entrada = {}

# Função para buscar a tag no banco de dados
def verificar_autorizacao(tag):
    try:
        cursor.execute("SELECT nome_aluno FROM alunos_acessos WHERE id_tag = %s", (tag,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]  # Retorna o nome do aluno autorizado
        else:
            return None
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {e}")
        return None

# Funções para o buzzer
def tocar_buzzer(frequencia, duracao):
    p = GPIO.PWM(BUZZER, frequencia)
    p.start(50)  # Duty cycle de 50%
    sleep(duracao)
    p.stop()

def buzzer_entrada_autorizada():
    tocar_buzzer(1000, 0.2)  # Som curto de entrada autorizada

def selecionar_itens(nome):
    itens_retirados = []
    print(f"\n{nome}, você está retirando os seguintes itens? Responda com 'sim' ou 'não':")

    for item in itens_disponiveis:
        limpar_tela()

        while True:
            resposta = input(f"{item}: ").strip().lower()
            if resposta in ['sim', 's']:
                itens_retirados.append(item)
                break
            elif resposta in ['não', 'n', 'nao']:
                break
            else:
                print("Resposta inválida. Por favor, responda apenas com 'sim' ou 'não'.")
                sleep(2)
                limpar_tela()

    salvar_itens_retirados(nome, itens_retirados)
    print(f"Obrigado {nome}, os itens selecionados foram registrados.")
    print(itens_retirados)

# Função para limpar a tela
def limpar_tela():
    os.system('clear')

def finalizar_programa(signal, frame):
    print("\nFinalizando o programa.")
    GPIO.cleanup()
    sys.exit(0)

# Captura o sinal de interrupção (CTRL+C)
signal.signal(signal.SIGINT, finalizar_programa)

try:
    while True:
        print("Aguardando leitura da tag...")

        tag, _ = leitorRfid.read()

        print(f"ID do cartão: {tag}")

        nome = verificar_autorizacao(tag)  # Verifica a autorização no banco de dados

        if nome:
            if tag not in tempo_entrada:
                tempo_entrada[tag] = time()
                print(f"Acesso autorizado, Bem-vindo(a) {nome}!")

                GPIO.output(LED_VERDE, GPIO.HIGH)
                buzzer_entrada_autorizada()
                sleep(3)
                GPIO.output(LED_VERDE, GPIO.LOW)

                selecionar_itens(nome)
            else:
                print(f"{nome}, você já está com a entrada registrada.")
        else:
            print("Acesso negado. Tag não autorizada.")
            GPIO.output(LED_VERMELHO, GPIO.HIGH)
            sleep(3)
            GPIO.output(LED_VERMELHO, GPIO.LOW)

finally:
    GPIO.cleanup()
    conexao.close()
    cursor.close()
