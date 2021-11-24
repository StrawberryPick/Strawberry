# downloadPredictionData.py
import datetime as dt
from rainPredictionScraper import RainPredictionScraper

currDay = dt.datetime.utcnow()
d = 0
dayList = list()

RainPrediction = RainPredictionScraper("Kajaani", "Finland")

while d < 10:
	day = dt.datetime.utcnow() + dt.timedelta(days=d)
	dayString = day.strftime("%Y%m%d")
	print(dayString)
	RainPrediction.downloadData(dayString)
	# dayList.append(dayString)
	d += 1

data = RainPrediction.getData()
RainPrediction.closeAll()
RainPrediction.saveData("code/RainPrediction/data/json/")
