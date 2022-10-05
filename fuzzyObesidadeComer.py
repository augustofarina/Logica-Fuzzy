import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 11, 1), 'comer') #Comer
#servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico') #Tempo para Ex

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 161, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
comer.automf(names=['pouco','razoavel','muito'])
#servico.automf(names=['ruim','medio','bom'])

# atribuicao sem o automf
#peso['minima'] = fuzz.gaussmf(gorjeta.universe, 0,.1)
peso['leve'] = fuzz.trapmf(peso.universe, [-1,0,40,60])
peso['medio'] = fuzz.trapmf(peso.universe, [40,60,80,100])
peso['pesado'] = fuzz.trapmf(peso.universe, [80,100,150,160])


#Visualizando as variáveis
comer.view()
#servico.view()
peso.view()



#Criando as regras
regra_1 = ctrl.Rule(comer['pouco'], peso['leve'])
regra_2 = ctrl.Rule(comer['razoavel'], peso['medio'])
regra_3 = ctrl.Rule(comer['muito'], peso['pesado'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3])


#Simulando
CalculoGorjeta = ctrl.ControlSystemSimulation(controlador)

notaQualidade = int(input('Comer: '))
#notaServico = int(input('Servico: '))
CalculoGorjeta.input['comer'] = notaQualidade
#CalculoGorjeta.input['servico'] = notaServico
CalculoGorjeta.compute()

valorGorjeta = CalculoGorjeta.output['peso']

print("\nComer %d \nPeso de %5.2f" %(
        notaQualidade,
        valorGorjeta))


comer.view(sim=CalculoGorjeta)
#servico.view(sim=CalculoGorjeta)
peso.view(sim=CalculoGorjeta)

plt.show()
