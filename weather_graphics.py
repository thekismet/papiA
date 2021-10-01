"""
FILENAME: weather_graphics.py
File 2 of 2
This example queries the Open Weather Maps site API to find out the current
weather for your location... and display it on a PaPiRus eInk display!
Taken from https://learn.adafruit.com/raspberry-pi-e-ink-weather-station-using-python/weather-station-code
PROJECT FILES
  1) weather.py
  2) weather_graphics.py
INSTRUCTIONS:
  call 'python3 weather.py' at the command line.
  
See README.md for more details.
"""

from datetime import datetime
import json
from PIL import Image, ImageDraw, ImageFont
from papirus import Papirus

tiny_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
icon_font = ImageFont.truetype("./meteocons.ttf", 40)

# Map the OpenWeatherMap icon code to the appropriate font character
ICON_MAP = {
  "01d": "B",
  "01n": "C",
  "02d": "H",
  "02n": "I",
  "03d": "N",
  "03n": "N",
  "04d": "Y",
  "04n": "Y",
  "09d": "Q",
  "09n": "Q",
  "10d": "R",
  "10n": "R",
  "11d": "Z",
  "11n": "Z",
  "13d": "W",
  "13n": "W",
  "50d": "J",
  "50n": "K",
}

# Conversion from Kelvins to deg C
KELVINS_TO_DEG_C = 273.15

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Weather_Graphics:
  def __init__(self, display, *, am_pm=True, celsius=True):
    self.am_pm = am_pm
    self.celsius = celsius

    self.tiny_font = tiny_font
    self.small_font = small_font
    self.medium_font = medium_font
    self.large_font = large_font

    self.display = display

    self._weather_icon = None
    self._city_name = None
    self._main_text = None
    self._temperature = None
    self._description = None
    self._time_text = None

  def display_weather(self, weather):
    weather = json.loads(weather)

    # set the icon/background
    self._weather_icon = ICON_MAP[weather["weather"][0]["icon"]]

    city_name = weather["name"] + ", " + weather["sys"]["country"]
    print("city_name:\t", city_name)
    self._city_name = city_name

    main = weather["weather"][0]["main"]
    print("main:\t\t", main)
    self._main_text = main

    humidity = weather["main"]["humidity"]
    self._humidity = "R/H=%d%%" % humidity
    feels_like = weather["main"]["feels_like"] - KELVINS_TO_DEG_C 	# Convert kelvins to degrees C
    temperature = weather["main"]["temp"] - KELVINS_TO_DEG_C 	# Convert kelvins to degrees C

    if self.celsius:
      self._temperature = "%d °C" % temperature
      self._feels_like = "%d °C" % feels_like
    else:
      self._temperature = "%d °F" % ((temperature * 9 / 5) + 32)
      self._feels_like = "%d °F" % ((feels_like * 9 / 5) + 32)

    print("temperature:\t", self._temperature)
    print("feels_like:\t", self._feels_like)

    description = weather["weather"][0]["description"]
    description = description[0].upper() + description[1:]
    print("description:\t", description)
    self._description = description
    # Examples: "thunderstorm with heavy drizzle", "Clear sky", "Cloudy sky"

    self.update_time()

  def update_time(self):
    now = datetime.now()
    #self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
    self._date_text = now.strftime("%a %b %d, %Y")
    self._time_text = now.strftime("%I:%M:%S %p")
    self.update_display()

  def update_display(self):
    image = Image.new("RGB", (200, 96), color=WHITE)
    draw = ImageDraw.Draw(image)

    # Draw the Icon
    (font_width, font_height) = icon_font.getsize(self._weather_icon)
    draw.text(
      (
          self.display.width - font_width - 2,			# x-position
          0,							# y-position
      ),
      self._weather_icon,
      font=icon_font,
      fill=BLACK,
    )

    # Draw the city
    draw.text(
      (5, 5), self._city_name, font=self.medium_font, fill=BLACK,
    )

    # Draw the date
    (font_width, font_height) = medium_font.getsize(self._date_text)
    draw.text(
      (5, font_height + 5),
      self._date_text,
      font=self.tiny_font,
      fill=BLACK,
    )

    # Draw the time
    (font_width, font_height) = medium_font.getsize(self._time_text)
    yheight = font_height + 21
    draw.text(
      (5, yheight),
      self._time_text,
      font=self.tiny_font,
      fill=BLACK,
    )

    # Draw the relative humidity 
    (font_width, font_height) = tiny_font.getsize(self._humidity)
    draw.text(
      (self.display.width - font_width - 5, yheight),
      self._humidity,
      font=self.tiny_font,
      fill=BLACK,
    )

    # Draw the main text
    (font_width, font_height) = large_font.getsize(self._main_text)
    draw.text(
      (5, self.display.height - font_height * 2),
      self._main_text,
      font=self.large_font,
      fill=BLACK,
    )

    # Draw the description
    (font_width, font_height) = small_font.getsize(self._description)
    draw.text(
      (5, self.display.height - font_height - 5),
      self._description,
      font=self.small_font,
      fill=BLACK,
    )

    # Draw the temperature
    (font_width, font_height) = large_font.getsize(self._temperature)
    draw.text(
      (
          self.display.width - font_width - 5,
          self.display.height - font_height * 2,
      ),
      self._temperature,
      font=self.large_font,
      fill=BLACK,
    )

    self.display.display(image)
    self.display.update()
