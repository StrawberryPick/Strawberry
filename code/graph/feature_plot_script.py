# featureVisulization.py

import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
pca = PCA(2)

dataPathsPattern = "./code/data/{}/"

filePath = dataPathsPattern.format('csv') + 'ready_data.csv'

df = pd.read_csv(filePath)

X = df[["totalReviewsLastYear",
	    "latestReview",
	    "avgRatingLastYear"]].reset_index(drop=True)

X['totalReviewsLastYear'] = (X['totalReviewsLastYear'] - X['totalReviewsLastYear'].min())\
	/ (X['totalReviewsLastYear'].max() - X['totalReviewsLastYear'].min())

X['latestReview'] = 1 - (X['latestReview'] - X['latestReview'].min())\
	/ (X['latestReview'].max() - X['latestReview'].min())

X['avgRatingLastYear'] = (X['avgRatingLastYear'] - X['avgRatingLastYear'].min())\
	/ (X['avgRatingLastYear'].max() - X['avgRatingLastYear'].min())

pca_df = pca.fit_transform(X)

df['feat_1'] = pca_df[:,0]
df['feat_2'] = pca_df[:,1]

groups = df['clusterGroup'].unique()

color = ['green', 'blue', 'orange']

fig, axs = plt.subplots(figsize = (10,6))

for i, group in enumerate(groups):
	sub_df = df[df['clusterGroup'] == group]
	feat_1 = sub_df['feat_1']
	feat_2 = sub_df['feat_2']

	center_1 = feat_1.mean()
	center_2 = feat_2.mean()

	plt.scatter(feat_1, feat_2, label = f"group {group}" , s=10, c=color[i], marker='x')
	plt.scatter(center_1, center_2, c='black', marker='o', s=20)
	plt.text(center_1+0.02, center_2+0.05, f"avg rating: {sub_df['avgRatingLastYear'].mean().round(2)} star")
	plt.text(center_1+0.02, center_2, f"latest review: {sub_df['latestReview'].mean().round(2)} months")
	plt.text(center_1+0.02, center_2-0.05, f"total review: {sub_df['totalReviewsLastYear'].mean().round(2)} reviews")

plt.legend()
plt.xlabel("pca_feature 1")
plt.ylabel("pca_feature 2")

plt.savefig("./code/graph/features_plot.png")
