# analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt

from transform import transformFiles

from sklearn.cluster import KMeans

dataPathsPattern = "./code/data/{}/"

countries = [
	"England",
	"America",
	"Finland",
	]

full_df = list()

for country in countries:
	aPath = dataPathsPattern.format(country)
	datafile = os.listdir(aPath)

	df = transformFiles(aPath, datafile)
	df = df[df['avgRatingLastYear'] > 0]
	df['country'] = country

	full_df.append(df)

full_df = pd.concat(full_df)

X = full_df[["totalReviewsLastYear",
	         "latestReview",
		     "avgRatingLastYear"]]

kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(X)
full_df["clusterGroup"] = kmeans.labels_

full_df.to_csv(dataPathsPattern.format('csv') + 'ready_data.csv', index=False)