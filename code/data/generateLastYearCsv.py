# generateCSV.py
import os
import sys

sys.path.insert(0, '.')

from code.analysis import transform

import pandas as pd

countries = [
	"England",
	"America",
	"Finland"
]

full_df = list()

for country in countries:
	dataPath = f"./code/data/{country}/"
	fileList = os.listdir(dataPath)

	country_df = transform.readLastYearFromAllFiles(dataPath, fileList)
	country_df['country'] = country

	full_df.append(country_df)

full_df = pd.concat(full_df)
full_df.to_csv("./code/data/csv/full_review_last_year.csv", index=False)
