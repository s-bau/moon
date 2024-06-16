from datetime import datetime
from datetime import timedelta
import json
import numpy as np
import pandas as pd
import re
import requests
import streamlit as st

##### streamlit interface #####

def main():
    
    st.title("Moon events") 

    # layout: container
    c = st.container()
    start = st.date_input("Choose a different start date") 
    df_moon = moon(start)
    c.dataframe(df_moon)


##### functions #####

def moon(start):
    # cleaning start and stop date for API URL   
    stop = start + timedelta(weeks=53)
    stop = stop.strftime("%Y-%m-%d")
    start = start.strftime("%Y-%m-%d")

    # Define API URL for moon, chosen date, deldot info
    url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=json&COMMAND='301'&OBJ_DATA='YES'&MAKE_EPHEM='YES'&EPHEM_TYPE='OBSERVER'&CENTER='500@399'&START_TIME={start}&STOP_TIME={stop}&STEP_SIZE='1d'&QUANTITIES='20'"

    r = requests.get(url)

    # accessing data
    data = r.json()

    if "result" in data:
        moon_data = data["result"]
    else:
        print("Couldn't find result")

    # defining column names
    columns = ["date", "delta", "deldot"]

    # Find the start and end of the ephemeris data
    start_index = moon_data.find("$$SOE")
    end_index = moon_data.find("$$EOE")

    # Extract the relevant data
    if start_index != -1 and end_index != -1:
        ephemeris_data = moon_data[start_index + 6:end_index]

    # define start of each line as YYYY-Mon-DD TT:TT and end as \n
    pattern = r"\d{4}-[A-Za-z]{3}-\d{2} \d{2}:\d{2} .*?\n"
    matches = re.findall(pattern, ephemeris_data, re.IGNORECASE)

    # replace everything that is more than 1 whitespace with ", "
    rows = []
    for match in matches:
        match = match.strip()
        clean = re.sub(r"\s{2,}", ", ", match)
        rows.append(clean)

    moon = pd.DataFrame()

    for row in rows:
        try:
            values = row.split(",")
            # Reshape values to match expected shape
            values = np.array(values)
            values = values.reshape(1,3)
            df = pd.DataFrame(values, columns=columns)
            moon = pd.concat([moon, df])   
        except ValueError:
            next

    # setting an index and choosing only relevant columns
    moon.reset_index(inplace=True)
    moon = moon[["date", "deldot"]]

    # Function to determine perigee/apogee based on the value of the row after
    def event_setter(row):
        current_index = row.name
        current_value = row["deldot"]
        if current_index < len(moon) - 1:
            next_value = moon.at[current_index + 1, "deldot"]
            if current_value[1] == "-" and next_value[1] != "-":
                return "Perigee"
            elif current_value[1] != "-" and next_value[1] == "-":
                return "Apogee"
        return None

    # Applying function to the dataframe
    moon["event"] = moon.apply(event_setter, axis=1)

    # keeping only rows with an event
    moon.dropna(inplace=True)

    # change format of date column
    moon["date"] = moon["date"].apply(lambda x: datetime.strptime(x, "%Y-%b-%d %H:%M").strftime("%Y-%b-%d"))

    # drop deldot column
    moon = moon[["date", "event"]]
    moon.set_index("date", inplace=True)

    return moon

main()

# to create requirements.txt: python -m pipreqs.pipreqs