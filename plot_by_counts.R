

require(ggplot2)
library(reshape2)
library(lubridate)

count_plot = function(data) {
  ### Plot counts
  
  data_grouped = data %>%
    #filter(year(.$decision_date) < 2015) %>%
    mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
    group_by(date2) %>%
    summarize(count = n())
  
  ggplot(data = data_grouped, aes(1:length(date2), count)) +
    geom_point() +
    geom_line() + 
    geom_smooth(method = "lm", formula = y ~ poly(x, 9), se = TRUE) +
    ggtitle("Car imports by Count")
  
}

count_plot_with_time = function(data, timeFrame) {
  ### Plot the count of Imports
  ### Data = 
  ### timeFrame = M for Monthly data, Y for yearly
  
  if (timeframe == "Y") {
    data_grouped = data %>%
      #filter(year(.$decision_date) < 2015) %>%
      mutate(date2 = format(.$decision_date, "%Y")) %>%
      group_by(date2) %>%
      summarize(count = n())
  
    ggplot(data = data_grouped, aes(1:length(date2), count)) +
      geom_point() +
      geom_line() + 
      geom_smooth(method = "lm", formula = y ~ poly(x, 3), se = TRUE) +
      ggtitle("Car imports by Count, Yearly")
  } else {
    data_grouped = data %>%
      #filter(year(.$decision_date) < 2015) %>%
      mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
      group_by(date2) %>%
      summarize(count = n())
    
    ggplot(data = data_grouped, aes(1:length(date2), count)) +
      geom_point() +
      geom_line() + 
      geom_smooth(method = "lm", formula = y ~ poly(x, 9), se = TRUE) +
      ggtitle("Car imports by Count, Month")
  }
}




























