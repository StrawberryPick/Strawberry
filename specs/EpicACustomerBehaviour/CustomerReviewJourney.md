# General instructions.
Main headings to write something under. links to respective root-task, under which variable spesific tasks are found.
- The goal of this task is to find insight from customer recurency through out the year, and to know about more the "pick your own" farming industry in America, England, and Finland.
# Getting data and test data
How and from where
- The data source we use is googlemap.com site. We collect the review data for each farm by Selenium framework
https://github.com/StrawberryPick/Strawberry/issues/96
# Cleaning
Is there need to clean and if what needs?
- Filtering out the reviews that doesn't have the rating point (0 in ratings)
https://github.com/StrawberryPick/Strawberry/issues/97

# Transformation
Anything done before usage in addition to cleaning.
- Normalize the data to scale 0 - 1 before Clustering the farms.
- The raw data is in json files each of which for each farm, we need to aggregate the data into 1 single csv file for analysis, each row for a farm.
https://github.com/StrawberryPick/Strawberry/issues/98

# Analysing
- Clustering the farm based on these features: Number of review last year, Latest receiving review time, Avarage rating from reviews last year
https://github.com/StrawberryPick/Strawberry/issues/113

# Interpretation and usage
In report and dashboard
- We make a powerpoint to show the graphs and charts to deliver the insight
https://github.com/StrawberryPick/Strawberry/issues/115
