import numpy as np #Utilizada para manipular os vetores
import matplotlib.pyplot as plt #Utilizada para manipular os gráficos
from scipy.integrate import odeint #Utilizada para resolver a EDO
from scipy.optimize import leastsq #Utilizada para ajustar os parâmetros
from math import log #Utilizada para construir os modelos
import time #Utilizada para calcular o tempo de execução

'''
Esse algoritmo foi desenvolvido para ser utilizado em conjunto com um arquivo no formato (.TXT) com a seguinte estrutura

t_i P(t_i)

Ex:
1900 15000000
1902 16000000
1910 20750662

--------------------------------------------------------------
Matheus Santana dos Santos
Aracaju-SE, junho/2019
Modelagem Matemática - Turma: 01
Departamento de Matemática - Universidade Federal de Sergipe
'''

def gompertz(p,t,P,h):
    dp = h * p * ( log(P)-log(p) )
    return dp

def verhulst(p,t,P,r):
    dp = r*(1-(p/P))*p
    return dp

def residual(p):
    p = tuple(p)
    if escolhaModelo == 1:
        sim_P = odeint(gompertz,p0,dados_anos_censo,args=p).flatten()
    elif escolhaModelo == 2:
        sim_P = odeint(verhulst,p0,dados_anos_censo,args=p).flatten()
    res = sim_P - dados_populacao_Brasil
    return res

#Manipula um arquivo externo (de forma simples)
def arquivo(arquivo):
        #Abre o arquivo em modo de leitura
        arq = open(arquivo, 'r')
        txt = arq.read()
        #Separa os valores por '\n'
        txt = txt.split('\n')
        data = []
        for i in range(len(txt)):
                #Separa os valores que contém espaço
                aux = txt[i].split(' ')
                #Inclui os dados na lista
                data.append(int(aux[0])) #Anos | 1º coluna
                data.append(float(aux[1])) #População | 2º coluna
        #Fecha o arquivo
        arq.close()
        return data


#----------INICIO DO PROGRAMA----------
print("[1] - Modelo de Gompertz")
print("[2] - Modelo de Verhulst")
escolhaModelo = int(input("Escolha: "))
''
if escolhaModelo == 1:
    nomeModelo = "Gompertz"
elif escolhaModelo == 2:
    nomeModelo = "Verhulst"
else:
    print("Opção inválida, aplicação encerrada!")
    exit()

T_1 = time.time() #inicia um contador de tempo de execução
dados = arquivo("dados.txt")

# Pega a primeira coluna dos dados que estão no arquivo
dados_anos_censo = dados[0::2]

# Pega a segunda coluna dos dados que estão no arquivo
dados_populacao_Brasil = dados[1::2]

#Valor inicial
p0 = dados_populacao_Brasil[0]

T_manipula = time.time() - T_1 #Tempo para fazer a manipulação dos dados

# Parâmetros p/ Gompertz e Verhulst
_pInfinito= 300000000
_lambda= 0.06
#Parâmetro adcional para Smith
_a = 0.5

#Escolhendo os chutes iniciais para ajustar o modelo
chutes = [_pInfinito, _lambda]

T_2 = time.time() #Tempo para encontrar o ajuste

#Ajusta os parâmetros
parametrosAjustados = leastsq(residual, chutes) # a saida desta função é do tipo [[x,y],z]
T_ajuste = time.time() - T_2  #Tempo para fazer o ajuste dos dados

#Parâmetros Ajustados
pInfinitoAjustado = parametrosAjustados[0][0]
lambdaAjustado = parametrosAjustados[0][1]

print("\nParâmetros Ajustados")
print("P∞: {0:,}".format(pInfinitoAjustado).replace(',','*').replace('.',',').replace('*','.'))
print("λ: {0:,}".format(lambdaAjustado).replace(',','*').replace('.',',').replace('*','.'))


#Aplicando o modelo com os parâmetros ajustados
if escolhaModelo == 1:
    T_3 = time.time() #Tempo para resolver o modelo ajustado
    estimativa = odeint(gompertz,p0,dados_anos_censo,args=(pInfinitoAjustado,lambdaAjustado,)) #Resolve o modelo com os parâmetros ajustados
    T_solucao = time.time() - T_3 #Tempo para resolver
elif escolhaModelo == 2:
    T_3 = time.time() #Tempo para resolver o modelo ajustado
    estimativa = odeint(verhulst,p0,dados_anos_censo,args=(pInfinitoAjustado,lambdaAjustado,)) #Resolve o modelo com os parâmetros ajustados
    T_solucao = time.time() - T_3 #Tempo para resolver

#Parte gráfica
plt.plot(dados_anos_censo,dados_populacao_Brasil,'bo',label="Dados Experimentais") # Gráfico dos valores coletados
plt.plot(dados_anos_censo,estimativa,'g-',label="Curva COM ajuste:\nλ: {0:,}".format(lambdaAjustado).replace(',','*').replace('.',',').replace('*','.') + ", P∞: {0:,}".format(pInfinitoAjustado).replace(',','*').replace('.',',').replace('*','.')) # Modelo Ajustado

#Calcula o erro absoluto
erroAbsoluto = abs(dados_populacao_Brasil - estimativa.T[0]) / dados_populacao_Brasil

print("\nMaior erro: {:.3}".format(max(erroAbsoluto)).replace(',','*').replace('.',',').replace('*','.'))
print("\nAcumulo de erro(soma dos erros absolutos): {:.3}".format(sum(erroAbsoluto)).replace(',','*').replace('.',',').replace('*','.'))
print("\nTempo de execução: {:.3}s".format(T_manipula+T_ajuste+T_solucao))

#Inserir legenda
plt.xlabel("Tempo (anos)\nTempo de execução: {:.3}s".format(T_manipula+T_ajuste+T_solucao))
plt.ylabel("População")
plt.title("Demografia do Brasil ("+nomeModelo+")\n ("+str(dados_anos_censo[0])+"-"+str(dados_anos_censo[len(dados_anos_censo)-1])+")"+"\nFonte: IBGE")
plt.legend()

#Exibir a interface
plt.show()
