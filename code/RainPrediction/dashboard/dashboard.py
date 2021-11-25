# dashboard.py

import sys
import json as js
import pandas as pd
import datetime as dt
sys.path.insert(0, '.')

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

date = dt.datetime.utcnow().strftime("%Y%m%d")

temp_hour_df = pd.read_csv(f"RainPrediction/data/csv/Finland_Kajaani_{date}_rain.csv")

fp = open(f"RainPrediction/data/json/Finland_Kajaani_{date}.json", 'r')
json_data = js.load(fp)

country = json_data["country"]
city = json_data["city"]
createdAt = json_data["createdAt"]

data = json_data["data"]
def transformRainAmountToNum(rainString):
	if type(rainString) != str:
		return rainString
	rainInfoInList = rainString.replace(",", ".").split(" ")
	num, unit = rainInfoInList[-2], rainInfoInList[-1]

	if unit == "cm":
		return float(num) * 10
	else:
		return float(num)

full_df_list = list()

for eachDayData in data:

	day_df = dict()
	day_df["date"] = eachDayData["date"]
	day_df["dailyTotalRain"] = eachDayData["totalRain"]

	full_df_list.append(day_df)

full_df = pd.DataFrame(full_df_list)\
	.reset_index(drop=True)\
	.set_index("date")

full_df["dailyTotalRain"] = full_df["dailyTotalRain"].apply(transformRainAmountToNum)

temp_hour_df['hour'] = temp_hour_df['hour'].apply(
	lambda hourFloat: "{:02.0f}:00".format(hourFloat))


temp_hour_df = (temp_hour_df.set_index('hour').T)
cols = temp_hour_df.columns
for col in cols:
	temp_hour_df[col] = temp_hour_df[col].apply(transformRainAmountToNum)

full_df = pd.concat([temp_hour_df, full_df],axis=1)
full_df.index = pd.to_datetime(full_df.index)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children=f'{country}, {city}'),
    html.H3(children=f'Data updated date: {createdAt}'),

    html.Div(children=[
    	"Choose your hour",
    	dcc.Dropdown(
    		id = "af-drd",
            options=[{"label": col, "value": col} for col in cols],
            value='10:00'
        )]),

    dcc.Graph(id='rain-graph')
    ]
)

@app.callback(
    Output(component_id='rain-graph', component_property='figure'),
	Input(component_id='af-drd', component_property='value')
	)
def update_rain_graph(hour):
	df = full_df[[hour, "dailyTotalRain"]]
	fig = px.line(df, x=df.index, y=df.columns,
				  title="amount of precipitation (mm) per day",
				  labels={
				  	"index": "date",
				  	"value": "mm"
				  })
	return fig

if __name__ == "__main__":
	app.run_server(debug=True)