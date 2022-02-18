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

def modelo_Gause(vetor_condicao_inicial, t, r,k,a,s,l,b):
    #x -> numero de presas
    #y -> numero de predadores

    y = vetor_condicao_inicial[0]
    x = vetor_condicao_inicial[1]

    y_ponto = ((s*y*(1-(y/l))) - (a*x*y))
    x_ponto = ((r*x*(1-(x-k))) - (b*x*y))

    taxa = np.array([y_ponto,x_ponto])
    return taxa

def residual(p):
    p = tuple(p)
    g = odeint(modelo_Gause, condicao_inicial, tempo, args=p).flatten()
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
param_r = 0.5 #Crescimento da presa
param_k = 100 #capacidade suporte
param_a = 0.02

param_s = 0.8 #Crescimento do predador
param_l = 100 #capacidade suporte
param_b = 0.02



chutes = [param_r, param_k, param_a, param_s, param_l, param_b]

parametros_ajustados = leastsq(residual, chutes)

#Parametros ajustados
_param_r = parametros_ajustados[0][0] #r
_param_k = parametros_ajustados[0][1] #s
_param_a = parametros_ajustados[0][2] #alpha
_param_s = parametros_ajustados[0][3] #beta
_param_l = parametros_ajustados[0][4] #k
_param_b = parametros_ajustados[0][5] #l

print(f'Parametros ajustados\n >a: {_param_r:.3f}\n >b: {_param_k:.3f}\n >c: {_param_a:.3f}\n >d: {_param_s:.3f}\n >e: {_param_l:.3f}\n >f: {_param_b:.3f}')

resultado = odeint(modelo_Gause, condicao_inicial, dados_tempo, args=(_param_r, _param_k, _param_a, _param_s, _param_l, _param_b))

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

equacaoString = r'$\dfrac{dx}{dt}=x(a-by)$' + '\t' + r'$\dfrac{dy}{dt}= y(-c+dx)$'
plt.suptitle('Modelo de Gause', fontsize=16)
plt.subplots_adjust(hspace = 0.4, bottom = 0.07)
plt.show()