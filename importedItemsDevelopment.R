# Monthly and yearly tax and Car Import EUR Amounts



carAgeGiven20 %>%
  #filter(year(.$decision_date) < 2015) %>%
  mutate(date2 = format(.$decision_date, "%Y")) %>%
  group_by(date2) %>%
  summarize(taxSum = sum(car_tax, na.rm = TRUE)) %>%
  ggplot(aes(date2, taxSum)) +
  geom_point() +
  ggtitle("Car imports Tax Amounn")


carAgeGiven20 %>%
  #filter(year(.$decision_date) < 2015) %>%
  mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
  group_by(date2) %>%
  summarize(taxSum = mean(car_tax, na.rm = TRUE)) %>%
  ggplot(aes(date2, taxSum)) +
  geom_point() +
  ggtitle("Car mean Tax per Year")

carAgeGiven20 %>%
  #filter(year(.$decision_date) < 2015) %>%
  mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
  group_by(date2) %>%
  summarize(taxation_value = mean(taxation_value, na.rm = TRUE)) %>%
  ggplot(aes(date2, taxation_value)) +
  geom_point() +
  ggtitle("Car mean Taxation value")

carAgeGiven20 %>%
  #filter(year(.$decision_date) < 2015) %>%
  mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
  group_by(date2) %>%
  summarize(car_age = mean(car_age, na.rm = TRUE)) %>%
  ggplot(aes(date2, car_age)) +
  geom_point() +
  geom_smooth(method = lm) +
  ggtitle("Car mean age2")
  
  
carAgeGiven20 %>%
  #filter(year(.$decision_date) < 2015) %>%
  mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
  group_by(date2) %>%
  summarize(power = mean(power_KW, na.rm = TRUE)) %>%
  ggplot(aes(date2, power)) +
  geom_point() +
  geom_smooth(method = lm) +
  ggtitle("Car mean power")

  
  
  