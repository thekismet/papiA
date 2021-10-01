"""
FILENAME:   weather.py
            File 1 of 2
See README.md for more details
BACKGROUND
    Taken from https://learn.adafruit.com/raspberry-pi-e-ink-weather-station-using-python/weather-station-code
    This example queries the Open Weather Maps site API to find out the current
    weather for your location... and display it on a PaPiRus eInk display.
    The original code was written to work with an Adafruit eInk display. This version was
    modified to work with a 2.0" (200x96) PaPiRus eInk display attached to a Raspberry Pi Zero W.
        eInk Display:           https://www.adafruit.com/product/3335
        Raspberry Pi Zero W:    https://www.adafruit.com/product/3708   This model has the header pins installed.
                                https://www.adafruit.com/product/3400   Header pins are not included with this model.
        
        PaPiRus Github Repo:    https://github.com/PiSupply/PaPiRus     Contains installation instructions and sample code for the API.
PROJECT FILES
    1) weather.py
    2) weather_graphics.py
INSTRUCTIONS:
    call 'python3 weather.py' at the command line.
"""

import json
import datetime
import time
import urllib.request
import urllib.parse
from weather_graphics import Weather_Graphics
from papirus import Papirus

# You'll need to get a token from openweathermap.org, looks like:
# 'b6907d289e10d714a6e88b30761fae22'
OPEN_WEATHER_TOKEN = "b6907d289e10d714a6e88b30761fae22"          # Be sure to get your own token. This one won't work.
URL_SUCCESS_CODE = 200

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
# In the US, a ZIP code will usually work, too.
#LOCATION = "New York, New York"
LOCATION = "10001, US"

DATA_SOURCE_URL = "https://api.openweathermap.org/data/2.5/weather"

if len(OPEN_WEATHER_TOKEN) == 0:
  raise RuntimeError(
    "You need to set your token first. If you don't already have one, you can register for a free account at https://home.openweathermap.org/users/sign_up"
  )

# Set up where we'll be fetching data from
params = {"q": LOCATION, "appid": OPEN_WEATHER_TOKEN}
data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)

# Initialize the Display
DISP_ROTATION = 0
img_display_screen = Papirus(rotation = DISP_ROTATION)

gfx = Weather_Graphics(img_display_screen, am_pm = True, celsius = False)
weather_refresh = None

response = urllib.request.urlopen(data_source)
if response.getcode() == URL_SUCCESS_CODE:
  value = response.read()
  print("Response is", json.dumps(json.loads(value), indent = 2, sort_keys = True))
  gfx.display_weather(value)
  print("")
  print("URL=", data_source)
  print("Last refresh: ", datetime.datetime.now().strftime("%I:%M:%S %p"))
  weather_refresh = time.monotonic()
else:
  print("Unable to retrieve data at {}".format(url))
