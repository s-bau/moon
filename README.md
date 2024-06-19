# Moon events
A python application that displays the dates of moon events that have a strong effect on tides
* Distance to the earth (Perigee/Apogee)
* Position relative to the earth and sun (Full/New moon)

[moonevents.streamlit.app](https://moonevents.streamlit.app/)


### Calculations
The python app uses [NASA's Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html)
* to determine the days of Perigee/Apogee based on the distance of the moon to the earth
* and to determine lunar phases based on the brightness of the moon
