# Moon and tides
A python application that displays the dates of moon events of the next 3 months that have an effect on tides. Tides are usually more extreme during perigee (when the moon is closest to the earth) as well as during full and new moon. Tides are usually less extreme during apogee (when the moon is farthest from the earth).
The application is deployed on streamlit and the user can choose a custom start date to display a different 3-month timeframe.

[moonevents.streamlit.app](https://moonevents.streamlit.app/)


### Calculations
The python app uses [NASA's JPL Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html)
* Perigee/Apogee are calculated based on the distance of the moon to the earth
* Lunar phases are calculated based on the brightness of the moon

### Files
**moon.py** is the basic python code for the calculations and creation of a dataframe, which is then integrated into **moon_streamlit.py**
