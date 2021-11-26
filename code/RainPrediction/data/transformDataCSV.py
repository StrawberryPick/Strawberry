# transformDataCSV.py

import json as js
import pandas as pd

import datetime as dt

date = dt.datetime.utcnow().strftime("%Y%m%d")
fp = open(f"RainPrediction/data/json/Finland_Kajaani_{date}.json", 'r')
json_data = js.load(fp)

# print(json_data["data"])
full_df_list = list()
for eachDayData in json_data["data"]:

	day_df = pd.DataFrame(eachDayData["data"])
	day_df["date"] = eachDayData["date"]
	day_df["dailyTotalRain"] = eachDayData["totalRain"]

	full_df_list.append(day_df)
full_df = pd.concat(full_df_list)

full_df.groupby(["hour", "date"])["temperature"].first().unstack().to_csv(
	f"RainPrediction/data/csv/Finland_Kajaani_{date}_temperature.csv")

full_df.groupby(["hour", "date"])["rainAmount"].first().unstack().to_csv(
	f"RainPrediction/data/csv/Finland_Kajaani_{date}_rain.csv")

# print(json_data["data"][0]["data"])
