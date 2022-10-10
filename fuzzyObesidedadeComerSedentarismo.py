import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl



#Variaveis de Entrada (Antecedent)
comer = ctrl.Antecedent(np.arange(0, 11, 1), 'comer') #Comer
sedentario = ctrl.Antecedent(np.arange(0, 11, 1), 'sedentario') #Tempo para Ex

#Variaveis de saída (Consequent)
peso = ctrl.Consequent(np.arange(0, 161, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
#comer.automf(names=['pouco','razoavel','muito'])
comer['pouco'] = fuzz.trapmf(comer.universe, [-2,-1,0,6])
comer['razoavel'] = fuzz.trapmf(comer.universe, [0,5,5,10])
comer['muito'] = fuzz.trapmf(comer.universe, [4,10,11,12])

#sedentario.automf(names=['pouco','medio','muito'])
sedentario['pouco'] = fuzz.trapmf(sedentario.universe, [-2,-1,0,6])
sedentario['medio'] = fuzz.trapmf(sedentario.universe, [0,5,5,10])
sedentario['muito'] = fuzz.trapmf(sedentario.universe, [4,10,11,12])

# atribuicao sem o automf
peso['leve'] = fuzz.gaussmf(peso.universe, 0,25)
peso['medio'] = fuzz.gaussmf(peso.universe, 80,25)
peso['pesado'] = fuzz.gaussmf(peso.universe, 160,25)


#Visualizando as variáveis

comer.view()
sedentario.view()
peso.view()

#Criando as regras
regra_1 = ctrl.Rule(comer['pouco'] | (sedentario['medio'] & sedentario['pouco']), peso['leve'])
regra_2 = ctrl.Rule(comer['razoavel'] | (sedentario['medio'] & sedentario['medio']), peso['medio'])
regra_3 = ctrl.Rule(comer['muito'] | (sedentario['medio'] & sedentario['muito']), peso['pesado'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3])


#Simulando
CalculoPeso = ctrl.ControlSystemSimulation(controlador)

#notaComer = x
#notaSedentario= x
notaComer = int(input('Comer: '))
notaSedentario = int(input('Sedentario: '))
CalculoPeso.input['comer'] = notaComer
CalculoPeso.input['sedentario'] = notaSedentario
CalculoPeso.compute()

valorPeso = CalculoPeso.output['peso']

print("\nComer %d \nSedentario: %d\nPeso de %5.2f" %(
        notaComer,
        notaSedentario,
        valorPeso))



comer.view(sim=CalculoPeso)
sedentario.view(sim=CalculoPeso)
peso.view(sim=CalculoPeso)

plt.show()