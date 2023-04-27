import pandas as pd
from teqniqly.lahman_datasets import LahmanDatasets
import seaborn as sns

ld = LahmanDatasets()
ld.load()

df_names = ld.dataframe_names

bateo_DF = ld["Batting"]
jugadores_DF = ld["People"]
salarios_DF = pd.read_csv("..\\salarios.csv")

bateo_hr = bateo_DF[["playerID", "HR"]]
# Se seleccionan sólamente los jugadores y los homeruns que han hecho
salarios_hr = salarios_DF[["playerID", "salary"]]
# Se seleccionan sólamente los jugadores y su salario

bateo_salarios_hr = pd.merge(bateo_hr, salarios_hr, how="right", on="playerID")
# Se realiza un right join con el método merge()

bateo_salarios_hr_DF = bateo_salarios_hr.groupby(["playerID"])[['HR', 'salary']].agg({'HR':'sum', 'salary':'mean'})
# Se agrupan los datos por jugador.
# Se seleccionan las columnas HR y salary.
# Se asigna el método sum() a HR y mean() a salary

jugadores_hr = jugadores_DF[["playerID", "weight", "height"]]

jugadores_salario_hr = pd.merge(bateo_salarios_hr, jugadores_hr, how="right", on="playerID")

jugadores_salario_hr_DF = jugadores_salario_hr.groupby(["playerID"])[['HR', 'salary', 'weight', 'height']].agg({
   'HR':'sum',
   'salary':'mean',
   'weight':'mean',
   'height':'mean'
})

def estandariza(column):
   media = column.mean()
   desv_est = column.std()
   return((column-media) / desv_est)

j_copy = jugadores_salario_hr_DF[['HR', 'salary', 'weight', 'height']]

for col in j_copy.columns:
   j_copy[col] = estandariza(j_copy[col])

sns.pairplot(data=j_copy)

sns.lmplot(x='HR', y='salary', data=j_copy)