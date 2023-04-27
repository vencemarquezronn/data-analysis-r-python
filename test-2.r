# 1. Cargue los paquetes de tidyverse y Lahman
library(tidyverse)
library(Lahman)
# library(GGally)
# library(readr) # nolint

# 2. Cargue las bases de datos de batting, people y salaries
bateo <- as_tibble(Batting)
jugadores <- as_tibble(People)
salarios <- as_tibble(Salaries)

# write_csv(salarios, file = ".\\salarios.csv") # nolint

moda <- function(x) {
  u <- unique(x)
  tab <- tabulate(match(x, u))
  u[tab == max(tab)]
}

# 3. Indique cada las unidades de observación de cada una
# de las bases de datos que cargó en el punto anterior

bateo %>%
   count(playerID, yearID, stint) %>%
   filter(n > 1)
   # Jugadores por año y orden de aparición por temporada

jugadores %>%
   count(playerID) %>%
   filter(n > 1)
   # Jugadores

salarios %>%
   count(yearID, playerID, teamID) %>%
   filter(n > 1)
   # Jugadores por año y equipo

# 4. Describa cada una de las variables registradas en sus
# bases de datos, e indique la cantidad de observaciones
# que hay en cada una de las bases de datos
# (se responde en entregable).

# 5. Indique las relaciones que hay entre las bases de
# datos y especifique las variables que permiten que
# existan dichas relaciones (recuerde que una relación solo
# se puede establecer para parejas de bases de datos)
# (se responde en entregable).

# 6. Indique las llaves de cada una de las bases de las
# interacciones que planteo en el punto anterior
# (se responde en entregable).

# 7. Realice una unión que le permita saber cuántos fueron
# los homeruns(HR) del jugador que más gana.

bateo_hr <- bateo %>%
   inner_join(salarios, by = c(
      "playerID",
      "yearID",
      "teamID"
   ))

# Cargando los datos necesarios y
# conservar los datos de la base sal

bateo_hr %>%
   group_by(playerID) %>%
   summarise(
      total_HR = sum(HR),
      moda_salarios = mean(salary)
   ) %>%
   View()

# Agrupar los datos por jugador,
# sumar los homeruns y obtener el
# salario prom

# 8. Realice una unión y un select que le permita tener una
# base de datos donde que consigne, la altura, el peso, el
# número de homeruns, el salario y el ID del jugador.

jugadores_hr <- jugadores %>%
   inner_join(bateo_hr, by = "playerID") %>%
   select(
      playerID, weight, height, HR, salary
   )

jugadores_hr_2 <- jugadores_hr %>%
   group_by(playerID) %>%
   summarise(
      Weight = moda(weight),
      Height = moda(height),
      prom_salario = mean(salary),
      total_hr = sum(HR)
   ) # Resumo la información por jugador

# jugadores_hr %>%
#    select(-playerID) %>%
#    ggpairs()
## Para usar este, es necesario instalar GGally

# 9. Realice un scatterplot(geom_point) o una línea
# suavizada ajustada(geom_smooth) donde relacione el
# salario con cada una de las otras variables de las que
# dispone en la base de datos del punto 8. E indique cual
# tiene una relación más fuerte con los salarios.

ggplot(data = jugadores_hr_2, mapping = aes(total_hr, prom_salario)) +
   geom_jitter() +
   geom_smooth()
   # Hacemos ambas

# 10. Genere una función que le permita restar la media y
# dividir sobre la desviación estándar de una variable a
# cada observación de la misma variable.

estandariza <- function(fuente) {
    media <- mean(fuente, na.rm = TRUE)
    desv_est <- sd(fuente, na.rm = TRUE)
    (fuente - media) / desv_est
}

jugadores_hr_3 <- jugadores_hr_2 %>%
   select(-playerID)

for (i in seq_along(jugadores_hr_3)) {
  jugadores_hr_3[[i]] <- estandariza(jugadores_hr_3[[i]])
}

jugadores_hr_3 %>%
   pairs()