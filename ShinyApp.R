#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Car Import Analysis"),

    # Sidebar with a slider input for number of bins 


        # Show a plot of the generated distribution
    mainPanel(
        plotOutput(outputId = "CarImportCount")
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
    
    output$CarImportCount <- renderPlot({
        
        count_plot(data)
        
    })

}

# Run the application 
shinyApp(ui = ui, server = server)
