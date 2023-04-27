# %% [markdown]
# # Taller 2 en Python
# *Ronald Vence Márquez*
# 
# > El siguiente es un cuaderno de Jupyter en el que realizo el taller 2 de nuevo, pero con python.
# 
# 1. Cargue los paquetes de tidyverse y de Lahman.
# 
# El primer problema es que ninguno de los paquetes existe en Python, pero existen alternativas.
# 
# ```powershell
# pip install pandas
# pip install tq-lahman-datasets
# ```
# 
# Después, se importan estas librerías dentro de un script de python

# %%
import pandas as pd
from teqniqly.lahman_datasets import LahmanDatasets
import seaborn as sns

# %% [markdown]
# Siguiendo la documentación de tq-lahman-datasets, se cargan los datasets y se obtienen los nombres:

# %%
ld = LahmanDatasets()

ld.load()

df_names = ld.dataframe_names

# %% [markdown]
# 2. Cargue las bases de datos de batting, people y salaries

# %% [markdown]
# Después, se cargan los diferentes dataframes en variables con nombres significativos:

# %%
bateo_DF = ld["Batting"]
jugadores_DF = ld["People"]

# %% [markdown]
# No obstante, en este paquete no se incluye salarios, así que es necesario exportarlo desde R:
# 
# ```r
# library(Lahman) # Importar Lahman a R
# library(readr) # Importar readr a R
# 
# salarios <- as_tibble(Salaries) # Guardar salarios en un espacio
# write_csv(salarios, file = ".\\salarios.csv") # Uso "\\" por que uso Windows
#    # Escribir un csv con la data del espacio utilizando readr::write_csv
# ```

# %% [markdown]
# Para poder importarlo en Python como un Dataframe de Pandas:

# %%
salarios_DF = pd.read_csv("..\\salarios.csv")

# %% [markdown]
# 3. Indique cada una de las unidades de observación de cada una de las bases de datos que cargó en el punto anterior. 
# 
# ```r
# bateo %>%
#    count(playerID, yearID, stint) %>%
#    filter(n > 1)
#    # Jugadores por año y orden de aparición por temporada
# 
# jugadores %>%
#    count(playerID) %>%
#    filter(n > 1)
#    # Jugadores
# 
# salarios %>%
#    count(yearID, playerID, teamID) %>%
#    filter(n > 1)
#    # Jugadores por equipo y año
# ```
# 
# 4. Describa cada una de las variables registradas en sus bases de datos, e indique la cantidad de observaciones que hay en cada una de las bases de datos.
# > Se explican en el entregable del taller realizado con `R`.
# 
# 5. Indique las relaciones que hay entre las bases de datos y especifique las variables que permiten que existan dichas relaciones (recuerde que una relación solo se puede establecer para parejas de bases de datos).
# 
# > Las diferentes tablas en la base de datos condensan diferente información acerca de los jugadores:
# > 1. Todas las bases de datos tienen la variable `playerID`.
# > 2. Además de `playerID`, las bases bateo y salarios se relacionan por medio de `yearID`, `teamID` y `leagueID`.
# 
# 6. Indique las llaves de cada una de las bases de las interacciones que planteo en el punto anterior.
# 
# > `bateo$playerID`, `jugadores$playerID`, `salarios$playerID`
# 
# 7. Realice una unión que le permita saber cuántos fueron los homeruns(HR) del jugador que más gana

# %% [markdown]
# Primero se seleccionan los datos en cada base y luego se realiza la unión por medio del método `merge()`:

# %%
bateo_salarios_hr = pd.merge(bateo_DF, salarios_DF, how="inner", on=["playerID", "yearID", "teamID"])
# Se realiza un inner join con el método merge()

# %% [markdown]
# Para poder averiguar cuántos homeruns tiene el jugador con mayor salario es necesario resumir todas las observaciones por jugador, sumar los homeruns por jugador y hallar el salario promedio de cada jugador.

# %%
bateo_salarios_hr_DF = bateo_salarios_hr.groupby(["playerID"])[['HR', 'salary']].agg({'HR':'sum', 'salary':'mean'})
# Se agrupan los datos por jugador.
# Se seleccionan las columnas HR y salary.
# Se asigna el método sum() a HR y mean() a salary

# %% [markdown]
# > Para este caso, utilizo la media del salario por jugador ya que los salarios del jugador varían en diferentes observaciones. Para este caso, el jugador que más gana es `tanakma01` con 22,000,000USD y 0 HR totales, y le sigue `rodrial01` con 18,109,829.64USD con un total de 696 HR.

# %% [markdown]
# 8. Realice una unión y un select que le permita tener una base de datos donde que consigne, la altura, el peso, el número de homeruns, el salario y el ID del jugador

# %%
jugadores_hr = pd.merge(bateo_salarios_hr, jugadores_DF, how="inner", on="playerID")

jugadores_salario_hr = jugadores_hr[["playerID", "weight","height", "HR", "salary"]]

jugadores_salario_hr_DF = jugadores_salario_hr.groupby(["playerID"])[['HR', 'salary', 'weight', 'height']].agg({
   'HR':'sum',
   'salary':'mean',
   'weight':'mean',
   'height':'mean'
})

# %% [markdown]
# Se realiza el mismo procedimiento que para los puntos anteriores.
# 
# 9. Realice un scatterplot(geom_point) o una línea suavizada ajustada(geom_smooth) donde relacione el salario con cada una de las otras variables de las que dispone en la base de datos del punto 8. E indique cual tiene una relación más fuerte con los salarios.
# 10. Genere una función que le permita restar la media y dividir sobre la desviación estándar de una variable a cada observación de la - misma variable.

# %%
def estandariza(column):
   media = column.mean()
   desv_est = column.std()
   return((column-media) / desv_est)

j_copy = jugadores_salario_hr_DF[['HR', 'salary', 'weight', 'height']]

for col in j_copy.columns:
   j_copy[col] = estandariza(j_copy[col])

# %%
sns.pairplot(data=j_copy)

# %% [markdown]
# En Python `seaborn` nos permite graficar un recuadro parecido al de `pairs()` en R. Se puede ver la misma relación entre las variables y se evidencia la misma relación entre salarios y homeruns totales en las carreras de los diferentes jugadores.

# %%
sns.lmplot(x='HR', y='salary', data=j_copy)

# %% [markdown]
# Y parece haber la misma relación entre los datos. Se podría decir que sí podría existir una relación directa entre los homeruns de los jugadores con el promedio de sus ingresos (salario) durante sus carreras.
# 
# 11. Teniendo en cuenta las bases de datos de las que dispone genere una hipótesis que pueda responder a partir de esos datos (use todas las bases de datos).
# 
# > Además de plantear la hipótesis de que a una mayor cantidad de homeruns, mayor serán los ingresos del jugador, también se puede plantear que estos jugadores tienen alturas y pesos mayormente promedio, que puede deberse a que si existen dificultades para moverse a altas velocidades (zancada pequeña o sobrepeso) evitan que los jugadores logren más homeruns, lo que los convierte en jugadores menos valiosos y, por tanto, limita sus ingresos.


