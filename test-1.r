library(tidyverse)
library(gapminder)

paises <- gapminder

grouped_paises <- group_by(paises, country) %>%
   mutate(gdp = pop * gdpPercap)

final_paises <- summarise(grouped_paises,
   mean_lifeExp = mean(lifeExp, na.rm = TRUE),
   mean_pop = mean(pop, na.rm = TRUE),
   mean_gpdPerCap = mean(gdpPercap, na.rm = TRUE),
   mean_gdp = mean(gdp, na.rm = TRUE)
)

ggplot(data = final_paises,
mapping = aes(mean_gpdPerCap, mean_lifeExp)) +
   geom_smooth() +
   geom_point()

ggplot(data = final_paises,
mapping = aes(mean_gdp, mean_lifeExp)) +
   geom_point() +
   geom_smooth(se = FALSE)
