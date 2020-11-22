

require(ggplot2)
library(reshape2)
library(lubridate)
require(dplyr)

line_count_plot = function(data, timeFrame, startDate, endDate) {
  
  ### Plot the count of Imports
  ### Data = 
  ### timeFrame = M for Monthly data, Y for yearly, D for daily
  ### startDate = in form "2012-01-02"
  ### endDate = in form "2020-09-30
  
  if (timeFrame == "Y") {
    data_grouped = data %>%
      filter(between(decision_date,as.Date(startDate),as.Date(endDate))) %>%
      mutate(date2 = format(.$decision_date, "%Y")) %>%
      group_by(date2) %>%
      summarize(count = n())
    
    ggplot(data = data_grouped, aes(seq(from = as.Date(startDate),to = as.Date(endDate),by = "year"), count)) +
      geom_point() +
      geom_line() + 
      geom_smooth(method = "lm", formula = y ~ poly(x, 3), se = TRUE) +
      ggtitle("Car imports by Count, year") +
      xlab("Date")+
      ylab("Nro of Cars Imported") 
    
  } else if (timeFrame == "M") {
    data_grouped = data %>%
      filter(between(decision_date,as.Date(startDate),as.Date(endDate))) %>%
      mutate(date2 = format(.$decision_date, "%Y-%m")) %>%
      group_by(date2) %>%
      summarize(count = n())
    
    ggplot(data = data_grouped, aes(seq(from = as.Date(startDate),to = as.Date(endDate),by = "month"), count)) +
      geom_point() +
      geom_line() + 
      geom_smooth(method = "lm", formula = y ~ poly(x, 3), se = TRUE) +
      ggtitle("Car imports by Count, month") +
      xlab("Date")+
      ylab("Nro of Cars Imported")
    
  } else {
    data_grouped = data %>%
      filter(between(decision_date,as.Date(startDate),as.Date(endDate))) %>%
      mutate(date2 = format(.$decision_date, "%Y-%m-%d")) %>%
      group_by(date2) %>%
      summarize(count = n())
    
    data_grouped = melt(data_grouped)
    data_grouped$date2 = as.Date(data_grouped$date2)
    
    ggplot(data = data_grouped, aes(date2, value)) +
      geom_point() +
      geom_line() + 
      geom_smooth(method = "lm", formula = y ~ poly(x, 3), se = TRUE) +
      ggtitle("Car imports by Count, day") +
      xlab("Date")+
      ylab("Nro of Cars Imported")
    
  }
}

line_count_plot_elif(data = data,timeFrame ="D",startDate = "2016-01-01", endDate = "2020-09-30")






