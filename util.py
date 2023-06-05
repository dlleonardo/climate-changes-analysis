import pandas as pd
import requests

# Representing the months as list of integers, used in calculate_df_season function to simplify the season check
springMonths = [3, 4, 5]
summerMonths = [6, 7, 8]
autumnMonths = [9, 10, 11]
winterMonths = [12, 1, 2]

# Given the url, geographical coordinates and time interval, get the open-meteo data in JSON format and returns the Dataframe with Raw data
def get_json_data(url, latitude, longitude, start_date, end_date):
    params = {
        "latitude":latitude,
        "longitude":longitude,
        "start_date":start_date,
        "end_date":end_date,
        "hourly":"temperature_2m,precipitation"
    }

    # Call to open-meteo API and parse the response into json
    response = requests.get(url, params=params)
    data = response.json()

    # Create a Pandas DataFrame containing weather data
    time_data = data["hourly"]["time"]
    temperature_data = data["hourly"]["temperature_2m"] 
    precipitation_data = data["hourly"]["precipitation"]

    dfWeather = pd.DataFrame({"time":time_data, "temperature":temperature_data, "precipitation":precipitation_data})

    return dfWeather

# Given a string representing a datetime, converts the string into a datetime object
def convert_to_datetime(strTime):
    return pd.to_datetime(strTime, format='%Y-%m-%dT%H:%M:%S')

# Given the Dataframe of Precipitation and a string representing the season
def calculate_mean_prec_season(dfPrec, season):
    season = season.lower()
    
    if season == "spring":
        months = springMonths
    elif season == "summer":
        months = summerMonths
    elif season == "autumn":
        months = autumnMonths
    elif season == "winter":
        months = winterMonths
    else:
        months = []
    # To simplify the analysis we assume that the winter season is in the same year as the other seasons
    dfRes = dfPrec \
            .where( dfPrec["month"].isin(months) ) \
            .groupby( dfPrec["year"] ) \
            .agg( {"precipitation":"mean"} ) \
            .reset_index()
    
    dfRes["season"] = season
    
    return dfRes
