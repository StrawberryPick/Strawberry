# Sunlight-duration 
Plant leaves absorb the most sunlight due to their broad shape (flattened surfaces), where plant stems from a sturdy framework to maintain leaves straight and allow for maximum solar exposure. Plant cells include the green pigment chlorophyll as well as organelles called chloroplasts, which are essential components of the photosynthesis process. Chlorophyll absorbs light energy and uses it to convert carbon dioxide and water into carbohydrates and oxygen, meaning plants use the energy they get from the sun to make food.

# General instructions.
Plants absorb sunlight and use the energy it provides to make food. This variable, in correlation with other factors, should have its own weight based on the relevance of how it affects plant development.

# Getting data and test data
Based on data downloaded from FMI https://en.ilmatieteenlaitos.fi/download-observations
https://github.com/StrawberryPick/Strawberry/issues/96

# Cleaning
Getting rid of unnecessary raws and columns.
https://github.com/StrawberryPick/Strawberry/issues/97

# Transformation
- Dividing length of time with 60 – as data was given in minutes of sunlight within one given hour
- Summarizing all hours in one day (sum of 24 characters per day) by creating function.
- From 8760 summarizing to 365 rows
https://github.com/StrawberryPick/Strawberry/issues/98

# Analysing
The function created for converting data from hours to data needs to be manually written for each month, as numbers days in months vary without logical patterns.
https://github.com/StrawberryPick/Strawberry/issues/113

# Interpretation and usage
Presenting data findings visually and using it in our final calculations.
https://github.com/StrawberryPick/Strawberry/issues/115
