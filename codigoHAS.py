#Aqui estou importando uma biblioteca para poder manipular planilhas de excel

import pandas as pd

# Vetor de risco.
# Aqui estou definindo todos os vetores de risco em um dicionário, dando o nome (keys) do que é cada um desses valores.

vetor_risco = {'IDADE': 0.104619551, 'TOXICÔNOMO': 0.244612108,
               'SOBREPESO/OBESIDADE': 0.118891867,'HÁBITOS ALIMENTARES': 0.095654227,
               'SEDENTARISMO': 0.126109516, 'ÁLCOOL': 0.10986779,
               'FATORES SÓCIOS ECONÔMICOS': 0.079178861, 'MEDICAÇÕES': 0.091405364,
               'APNÉIA SONO': 0.030135857,'GENÉTICA': 0.010811172}

# Funções de normalização
# Aqui estou criando funções de normalização

# Nessa normalização, eu recebo a idade do paciente, e divido por 65, retornando pra ele esse resultado.

def normalize_age(idade):
    norm = idade/65
    return norm

# Nessa normalização, eu pego o valor x e divido pela idade do paciente, retornando um valor entre 0 e 1.

def normalize(x, idade):
    norm = x/idade
    return min(norm, 1)

# Nessa normalização, eu pego o valor x que se refere ao sobrepeso/obesidade e divido por 30, e retorno o resultado.

def normalizeIMC(x):
    norm = x/30
    return min(norm, 1)

# Aqui eu verifico o x, que seria a soma de todos os dados normalizados  após multiplicar pelo vetor de risco, e retorno a quantidade de risco que há.

def alerta(x):
  if x >= 0 and x <= 0.33 : return "baixo risco"
  elif x > 0.33 and x <= 0.66 : return "médio risco"
  else : return "alto risco"

# Lendo os dados

# Para ler os dados, eu preciso primeiro colocar o caminho para chegar até ele, então será lido e depois crio uma cópia.

df = pd.read_excel('/content/Pacientes.xlsx')
df_copy = df.copy()

# Normalizando os dados

# Aqui estou aplicando todas as normalizações, adicionando o dado normalizado no lugar do antigo dado, faço isso em looping para todos os pacientes.

for key in vetor_risco.keys():
    if key == 'IDADE':
        df[key] = df['IDADE'].apply(normalize_age)
    elif key == 'TOXICÔNOMO':
        df[key] = df.apply(lambda row: normalize(row[key], df_copy.loc[row.name, 'IDADE']), axis=1)
    elif key == 'SOBREPESO/OBESIDADE':
        df[key] = df[key].apply(normalizeIMC)
    elif key == 'HÁBITOS ALIMENTARES' or key == 'SEDENTARISMO' or key == 'ÁLCOOL':
        df[key] = df.apply(lambda row: normalize(row[key], df_copy.loc[row.name, 'IDADE']), axis=1)
    elif key == 'FATORES SÓCIOS ECONÔMICOS':
        df[key] = df[key]
    elif key == 'MEDICAÇÕES':
        df[key] = df.apply(lambda row: normalize(row[key], df_copy.loc[row.name, 'IDADE']), axis=1)
    elif key == 'APNÉIA SONO':
        df[key] = df.apply(lambda row: normalize(row[key], df_copy.loc[row.name, 'IDADE']), axis=1)

# Calculando o resultado

# Aqui estou fazendo a multipicação de cada valor pelo seu vetor de risco, e somando tudo para criar um resultado.

df['resultado'] = sum(df[key] * vetor_risco[key] for key in vetor_risco.keys())

# Gerando o alerta
# Aqui eu crio o alerta usando o resultado, para saber se é baixo, médio ou alto risco.

df['alerta'] = df['resultado'].apply(alerta)

# Salvando os resultados
# Então aqui criamos um excel com os dados normalizados

df.to_excel('/content/saida_normalizada.xlsx')

# Multiplicando o DataFrame pelas ponderações
# E aqui criamos um excel com todos os dados ponderados, que seria com todos os dados multiplicados pelo seu vetor de risco.

df.loc[:, vetor_risco.keys()] = df.loc[:, vetor_risco. keys()].multiply(list(vetor_risco.values()), axis=1)

# Salvando o resultado da ponderação
# Por fim criamos o excel com os dados ponderados.

df.to_excel('/content/saida_ponderada.xlsx')
