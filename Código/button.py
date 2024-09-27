import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import csv
from datetime import datetime, timedelta
import requests


leitorRFid = SimpleMFRC522()
usuarios = {837196207282: "Fulano", 701577035323: "Beltrano", 634156810886: "Ciclano"}
professores = {837196207282: "Fulano"} 
acesso_diario = {}
tempo_entrada = {}
alunos_saindo = {}
inicio_aula = None
fim_aula = None

led_verde = 5
led_vermelho = 3
buzzer = 37
entrada = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_verde, GPIO.OUT)
GPIO.setup(led_vermelho, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)


def send_post_request(mensagem):
    data = {'data': mensagem}
    try:
        response = requests.post('http://localhost:5000', json=data)
        if response.status_code == 201:
            print("Mensagem enviada com sucesso!")
        else:
            print(f"Erro ao enviar mensagem: {response.status_code}")
    except Exception as e:
        print(f"Erro na conexão: {e}")


def calcular_presenca(tempo_na_sala, aluno_tag):
    
    periodo_completo = timedelta(hours=1)

    
    total_presenca = 4
    
    
    if aluno_tag in alunos_saindo:
        tempo_saida = alunos_saindo[aluno_tag]
        if tempo_saida < fim_aula:
    
            presenca_proporcional = tempo_na_sala // periodo_completo
            return min(presenca_proporcional, total_presenca)
    
    return total_presenca



def verificar_tag(tag):
    global entrada, inicio_aula, fim_aula, alunos_saindo

    if tag in professores: 
        if inicio_aula is None:  
            inicio_aula = datetime.now()
            print(f"Início da aula registrado pelo professor {usuarios[tag]}. Horário: {inicio_aula}")
            novo_log(tag, usuarios[tag], "Início da Aula", None)
            send_post_request(f"Início da aula registrado pelo professor {usuarios[tag]}. Horário: {inicio_aula}")
        else:  
            fim_aula = datetime.now()
            duracao_aula = fim_aula - inicio_aula
            print(f"Término da aula registrado pelo professor {usuarios[tag]}. Horário: {fim_aula}")
            novo_log(tag, usuarios[tag], "Término da Aula", duracao_aula)
            send_post_request(f"Término da aula registrado pelo professor {usuarios[tag]}. Horário: {fim_aula}")

            
            for aluno_tag, tempo_inicial in tempo_entrada.items():
                tempo_na_sala = fim_aula - tempo_inicial
                if aluno_tag in alunos_saindo:
                    tempo_saida = alunos_saindo[aluno_tag]
                    if tempo_saida < fim_aula:  
                        presenca = calcular_presenca(tempo_na_sala, aluno_tag)
                        print(f"Aluno {usuarios[aluno_tag]} saiu antes do término da aula. Presença proporcional: {presenca}/4 períodos.")
                        novo_log(aluno_tag, usuarios[aluno_tag], f"Presença proporcional: {presenca}/4", None)
                        send_post_request(f"{usuarios[aluno_tag]} Presença: {presenca}/4")
                else:  
                    presenca = calcular_presenca(tempo_na_sala, aluno_tag)
                    print(f"Aluno {usuarios[aluno_tag]} esteve presente por {tempo_na_sala}. Presença: {presenca}/4 períodos.")
                    novo_log(aluno_tag, usuarios[aluno_tag], f"Presença: {presenca}/4", None)
                    send_post_request(f"{usuarios[aluno_tag]} Presença: {presenca}/4")
                

            inicio_aula = None  
            fim_aula = None
            tempo_entrada.clear()  
            alunos_saindo.clear()  
            acesso_diario.clear()

    elif tag in usuarios:  
        if tag not in acesso_diario:
            print(f"Bem vindo {usuarios[tag]}!")
            acesso_diario[tag] = usuarios
            entrada = True
            ligar_leds("verde")
            novo_log(tag, usuarios[tag], "Entrada", None)
            tempo_entrada[tag] = datetime.now()
            send_post_request(f"Entrada de {usuarios[tag]} registrada. Horário: {datetime.now()}")
        elif entrada:
            print(f"Volte Sempre {usuarios[tag]}!")
            tempo_inicial = tempo_entrada[tag]
            tempo_atual = datetime.now() 

            
            if inicio_aula is not None and tempo_inicial < inicio_aula:
                tempo_inicial = inicio_aula  

            
            alunos_saindo[tag] = tempo_atual 
            tempo_na_sala = tempo_atual - tempo_inicial
            entrada = False
            novo_log(tag, usuarios[tag], "Saída", tempo_na_sala)
            send_post_request(f"Saída de {usuarios[tag]} registrada. Horário: {tempo_atual}")
            entrada = False 
    
    else:
        print(f"Identificação não encontrada!")
        ligar_leds("vermelho")


def ligar_leds(led):
    if led == "verde":
        GPIO.output(led_verde, GPIO.HIGH)
        print("ligar Led verde")
        time.sleep(1)
        print("desligar Led verde")
        GPIO.output(led_verde, GPIO.LOW)
    elif led == "vermelho":
        for i in range(5):
            GPIO.output(led_vermelho, GPIO.HIGH)
            GPIO.output(buzzer, GPIO.HIGH)
            print("ligar Led vermelho")
            time.sleep(0.5)
            GPIO.output(led_vermelho, GPIO.LOW)
            GPIO.output(buzzer, GPIO.LOW)
            print("desligar Led vermelho")
            time.sleep(0.5)


def novo_log(log, usuario, entrada_saida, tempo):
    with open('logs.csv', mode='a', newline='', encoding='utf-8') as arquivo_csv:
        dados = csv.writer(arquivo_csv)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dados.writerow([data_hora, log, usuario, entrada_saida, tempo])


try:
    while True:
        GPIO.output(led_verde, GPIO.LOW)
        GPIO.output(led_vermelho, GPIO.LOW)
        
        print("Aguardando leitura da tag...")
        #tag = int(input("Digite o ID do usuário: "))  
        time.sleep(2)
        tag, text = leitorRFid.read()
        print(tag)
        verificar_tag(tag)

except KeyboardInterrupt:
    print("Programa interrompido")
finally:
    #GPIO.cleanup()
    print("Fim do programa")
