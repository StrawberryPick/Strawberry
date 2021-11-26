# visualization.py

import pandas as pd
import matplotlib.pyplot as plt

# from transform import transformFiles

from sklearn.cluster import KMeans

dataPathsPattern = "./code/data/{}/"


full_df = list()

filePath = dataPathsPattern.format('csv') + 'ready_data.csv'

df = pd.read_csv(filePath)
countries = df['country'].unique()

figure, axis = plt.subplots(3, 1, figsize=(7,10))

for i, country in enumerate(countries):

	sub_df = df[df['country'] == country]
	X = sub_df[["totalReviewsLastYear",
		    	"latestReview",
				"avgRatingLastYear"]].reset_index(drop=True)

	inertia = list()
	K = list()
	for k in range(10):

		kmeans = KMeans(n_clusters=k+1, random_state=0)
		kmeans.fit(X)

		inertia.append(kmeans.inertia_)
		K.append(k+1)

	axis[i].plot(K, inertia)
	axis[i].set_xlabel(f"K group {country}")
	axis[i].set_ylabel("inertia value")

	full_df.append(df)

figure.savefig("./code/graph/elbow_graph.png")
