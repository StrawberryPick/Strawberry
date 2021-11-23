# clusterBarChart.py
import pandas as pd

dataPathsPattern = "./code/data/{}/"

filePath = dataPathsPattern.format('csv') + 'ready_data.csv'

df = pd.read_csv(filePath)

agg_df = df.groupby(["clusterGroup", "country"])['avgRatingLastYear'].count()
agg_df.unstack()\
	.plot(kind='bar', stacked=True)\
	.figure\
	.savefig("./code/graph/group_components.png")
