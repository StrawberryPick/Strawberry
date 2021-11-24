import json as js
import os
import pandas as pd

dataPath = "./code/data/America/"
fileList = os.listdir(dataPath)

transformsDateDict = {
	"11 months ago": 11,
	"10 months ago": 10,
	"9 months ago": 9,
	"8 months ago": 8,
	"7 months ago": 7,
	"6 months ago": 6,
	"5 months ago": 5,
	"4 months ago": 4,
	"3 months ago": 3,
	"2 months ago": 2,
	"a month ago": 1,
	"4 weeks ago": 0.9,
	"3 weeks ago": 0.75,
	"2 weeks ago": 0.5,
	"a week ago": 0.25,
	"6 days ago": 0.2,
	"5 days ago": 0.17,
	"4 days ago": 0.13,
	"3 days ago": 0.1,
	"2 days ago": 0.07,
	"a day ago": 0.03,
}


def transformFiles(dataPath, listOfJsonFiles):
	farmInformation = list()

	for file in listOfJsonFiles:
		path = dataPath + file
		fp = open(path, "r")

		data = js.load(fp)

		farmName = data["farmName"]
		avgRating = data["avgRating"]
		numReview = data["numReview"]
		createdAt = data["createdAt"]
		reviewData = data["data"]
		
		reviewDf = pd.DataFrame(reviewData)
		filterDf = reviewDf[~reviewDf['date'].str.contains("year")]\
			.reset_index(drop=True)

		if filterDf.shape[0] <= 1:
			continue

		filterDf['date'] = filterDf['date']\
			.replace(transformsDateDict)\
			.apply(lambda value: 0.015 if type(value) == str else value,)\
			.astype(float)

		frequency = filterDf['date'].sort_values().diff(1).mean()
		totalReviewsLastYear = filterDf.shape[0]
		latestReview = filterDf['date'].min()
		avgRatingLastYear = filterDf['rating'].mean().round(1)

		dataDict = {
			"farmName": farmName,
			"avgRating": avgRating,
			"numReview": numReview,
			"createdAt": createdAt,
			"frequency": frequency,
			"totalReviewsLastYear": totalReviewsLastYear,
			"latestReview": latestReview,
			"avgRatingLastYear": avgRatingLastYear
		}

		farmInformation.append(dataDict)

	df = pd.DataFrame(farmInformation)
	df = df[df['numReview'] >= df['totalReviewsLastYear']].reset_index(drop=True)
	df = df[df['avgRatingLastYear'] > 0]
	return df


def readLastYearFromAllFiles(dataPath, listOfJsonFiles):
	farmInformation = list()

	fullReviewDf = list()

	for file in listOfJsonFiles:
		path = dataPath + file
		fp = open(path, "r")

		data = js.load(fp)

		farmName = data["farmName"]
		avgRating = data["avgRating"]
		numReview = data["numReview"]
		createdAt = data["createdAt"]
		reviewData = data["data"]

		reviewDf = pd.DataFrame(reviewData)
		filterDf = reviewDf[~reviewDf['date'].str.contains("year")]\
			.reset_index(drop=True)

		if filterDf.shape[0] <= 1:
			continue

		filterDf['monthsAgo'] = filterDf['date']\
			.replace(transformsDateDict)\
			.apply(lambda value: 0.015 if type(value) == str else value,)\
			.astype(float)
		filterDf['farmName'] = farmName
		filterDf['avgRating'] = avgRating
		filterDf['numReview'] = numReview
		filterDf['createdAt'] = createdAt

		fullReviewDf.append(filterDf)


	fullReviewDf = pd.concat(fullReviewDf)
	fullReviewDf = fullReviewDf.drop_duplicates(['title', 'farmName', 'body'])

	return fullReviewDf[['createdAt', 'title', 'rating', 'body', 'monthsAgo',
						 'date', 'farmName', 'avgRating', 'numReview']]
