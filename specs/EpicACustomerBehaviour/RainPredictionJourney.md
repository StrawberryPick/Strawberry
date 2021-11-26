# General instructions.
Main headings to write something under. links to respective root-task, under which variable spesific tasks are found. 
# Getting data and test data
How and from where
Data source: foreca.fi,The data we have rain/snow, moisture, temperature, daylight time, etc.
https://github.com/StrawberryPick/Strawberry/issues/96

# Cleaning
Is there need to clean and if what needs?
There is no need to clean the data for this source, thanks to the simplicity of the html structure of the website
https://github.com/StrawberryPick/Strawberry/issues/97

# Transformation
Anything done before usage in addition to cleaning
Transform the data from json format to csv format, columns {00:00, 01:00, ..., 23:00, dailyTotalRain}, rows {20211125, 20211126, ...} (10 rows)
https://github.com/StrawberryPick/Strawberry/issues/98

# Analysing
We only need to visualize the data to see the rain pattern in the next 10 days
https://github.com/StrawberryPick/Strawberry/issues/113

# Interpretation and usage
In report and dashboard
Build the first version of dashboard using Dash and Plotly
https://github.com/StrawberryPick/Strawberry/issues/115
