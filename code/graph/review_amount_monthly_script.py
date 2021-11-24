# review_amount_monthly_script.py

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

df = pd.read_csv("./code/data/csv/full_review_last_year.csv", parse_dates=['createdAt'])
df['monthsAgo'] = np.floor(df['monthsAgo'])
df['currMonth'] = df['createdAt'].dt.month
df['monthsOfYear'] = ((df['currMonth'] - df['monthsAgo']) % 12).replace({0:12})

countries = df['country'].unique()

reviewNumDf = df.groupby(['country', 'monthsOfYear'])['avgRating'].count().unstack()

for country in countries:
	countryReviewSeries = reviewNumDf.loc[country]
	plt.plot(countryReviewSeries.index, countryReviewSeries.values,
			 label=country)

plt.legend()
plt.title("total number of reviews last year in different countries")
plt.xlabel("month in year")
plt.ylabel("number of reviews")

plt.savefig("./code/graph/review_amount_monthly.png")