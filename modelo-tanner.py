import numpy as np #Utilizada para manipular os vetores
import matplotlib.pyplot as plt #Utilizada para manipular os graficos
from scipy.integrate import odeint #Utilizada para resolver a EDO
from scipy.optimize import leastsq #Utilizada para ajustar os parametros

def arquivo(arquivo,num_cols):
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
            for j in range(num_cols):
                data.append(float(aux[j]))
    #Fecha o arquivo
    arq.close()
    return data

def modelo_Tanner(vetor_condicao_inicial, t, gamma, u, m, d, s, h):
    #x -> numero de presas
    #y -> numero de predadores

    y = vetor_condicao_inicial[0]
    x = vetor_condicao_inicial[1]

    y_ponto = (s*y*(1-((h*y)/x)))
    x_ponto = ((gamma*x*(1-(x/u))) - ((m*x*y)/(d+x)))   

    taxa = np.array([y_ponto,x_ponto])
    return taxa

def residual(p):
    p = tuple(p)
    g = odeint(modelo_Tanner, condicao_inicial, tempo, args=p).flatten()
    res_predador = g[0::2] - dados_predador
    res_presas = g[1::2] - dados_presas

    res = np.zeros(2*len(res_predador))
    res[0::2] = res_predador  # SAIDA DO COMANDO res[predador,0,predador,0,....]
    res[1::2] = res_presas # SAIDA DO COMANDO res[predador,presa,predador,presa,....]

    return res

arquivo_colunas = 3
dados = arquivo("dados-unidade-2-1.txt",arquivo_colunas)

# Pega a primeira coluna dos dados que estao no arquivo
tempo = dados[0::arquivo_colunas]
dados_tempo = np.linspace(min(tempo), max(tempo),  1000) #Para criar uma suavidade na hora do plot

# Pega a segunda coluna dos dados que estao no arquivo
dados_predador = dados[1::arquivo_colunas]

# Pega a terceira coluna dos dados que estao no arquivo
dados_presas = dados[2::arquivo_colunas]

#Condicoes Iniciais
condicao_inicial = [dados_predador[0], dados_presas[0]]

#Parametros sem ajuste

param_gamma = 0.5
param_u = 0.2
param_m = 0.8
param_d = 0.4
param_s = 0.02
param_h = 0.8

chutes = [param_gamma, param_u, param_m, param_d, param_s, param_h]

parametros_ajustados = leastsq(residual, chutes)

#Parametros ajustados
_param_gamma = parametros_ajustados[0][0]
_param_u = parametros_ajustados[0][1]
_param_m = parametros_ajustados[0][2]
_param_d = parametros_ajustados[0][3]
_param_s = parametros_ajustados[0][4]
_param_h = parametros_ajustados[0][5]

print(f'Parametros ajustados\n >gamma: {_param_gamma:.3f}\n >u: {_param_u:.3f}\n >m: {_param_m:.3f}\n >d: {_param_d:.3f}\n >s: {_param_s:.3f}\n >h: {_param_h:.3f}')

resultado = odeint(modelo_Tanner, condicao_inicial, dados_tempo, args=(_param_gamma, _param_u, _param_m, _param_d, _param_s, _param_h))

predadores, presas = resultado[:,0], resultado[:,1]

#PLOT

fig, axes = plt.subplots(2, 2, figsize=(8,8))
ax = axes.flatten()

ax[0].set_title("Dados coletados", fontsize=12)
ax[0].plot(tempo, dados_predador, 'ro-', label = "Lince (Predador)")
ax[0].plot(tempo, dados_presas, 'bo-', label = "Coelhos (Presa)")
ax[0].set_xlabel('Tempo (anos)')
ax[0].set_ylabel('População (x1000)')
ax[0].legend(loc='best')
ax[0].grid()

ax[1].set_title("Evolução da poluação de presas", fontsize=12)
ax[1].plot(tempo, dados_presas, 'bo-', label = "Dados coletados")
ax[1].plot(dados_tempo, presas, 'g', label = "Curva ajustada")
ax[1].set_xlabel('Tempo (anos)')
ax[1].set_ylabel('População (x1000)')
ax[1].legend(loc='best')
ax[1].grid()

ax[2].set_title("Evolução da poluação de predadores", fontsize=12)
ax[2].plot(tempo, dados_predador, 'ro-', label = "Dados coletados")
ax[2].plot(dados_tempo, predadores, 'y', label = "Curva ajustada")
ax[2].set_xlabel('Tempo (anos)')
ax[2].set_ylabel('População (x1000)')
ax[2].legend(loc='best')
ax[2].grid()

ax[3].set_title("Curvas ajustadas", fontsize=12)
ax[3].plot(dados_tempo, predadores, 'r', label = "Lince (Predador)")
ax[3].plot(dados_tempo, presas, 'b', label = "Coelho (Presa)")
ax[3].set_xlabel('Tempo (anos)')
ax[3].set_ylabel('População (x1000)')
ax[3].legend(loc='best')
ax[3].grid()

plt.suptitle('Modelo de Tanner', fontsize=16)
plt.subplots_adjust(hspace = 0.4, top = 0.8, bottom = 0.07)
plt.show()