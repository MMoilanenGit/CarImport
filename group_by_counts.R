



# how many cars imported per month from 01-2012 to 09-2020
MonthCounts = clean_data_func %>% group_by(year_month) %>% summarise(n = n())

require(ggplot2)
library(reshape2)
library(lubridate)
##The values Year, Value, School_ID are
##inherited by the geoms


carAgeGiven20 %>%
  #filter(year(.$decision_date) < 2015) %>%
  mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
  group_by(date2) %>%
  summarize(count = n()) %>%
  ggplot(aes(date2, count)) +
  geom_point() +
  geom_line() + 
  ggtitle("Car imports by Count")

carAgeGiven20 %>%
  #filter(year(.$decision_date) < 2015) %>%
  mutate(date2 = format(.$decision_date, "%Y")) %>%
  group_by(date2) %>%
  summarize(count = n()) %>%
  ggplot(aes(date2, count)) +
  geom_point() +
  geom_line() + 
  ggtitle("Car imports by Count")






library(reshape2)












str(dd)



