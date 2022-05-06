#!/usr/bin/env python
#
# A polybar indicator for Project Michurin. Displays an icon along with
# a status message to indicate the status of a plant with a Michurin moisture
# sensor. This is just a proof of concept and may have to be completely
# rewritten soon.
#
# Requires MICHURIN_ENDPOINT and MICHURIN_TOKEN environmental variables to be 
# set, or present in `michurin.env` file, for the purpose of communication 
# with your Michurin server.
#
# Author: machaerus
# https://gitlab.com/machaerus

from dateutil import parser
from datetime import datetime as dt
from datetime import timedelta
import json
from pathlib import Path
import os
import sys

import pytz
import requests
from dotenv import load_dotenv


class MichurinPolybar:

	def __init__(self):

		try:
			# Load environment
			env_path = os.path.join(
				os.path.dirname(sys.argv[0]), "michurin.env")
			load_dotenv(dotenv_path=env_path)
			colors_path = os.path.join(
				os.path.dirname(sys.argv[0]), "colors.sh")
			load_dotenv(dotenv_path=colors_path)

			# server access
			self.MICHURIN_TOKEN = os.getenv("MICHURIN_TOKEN")
			self.MICHURIN_ENDPOINT = os.getenv("MICHURIN_ENDPOINT")

			assert self.MICHURIN_TOKEN is not None
			assert self.MICHURIN_ENDPOINT is not None
		except AssertionError:
			print("Michurin: Environment not loaded!")
			sys.exit(1)

		# color definitions
		self.faded_green = os.getenv("faded_green")
		self.faded_yellow = os.getenv("faded_yellow")
		self.faded_red = os.getenv("faded_red")
		self.RESET = os.getenv("RESET")
		# self.RESET = "%{F#3e565e}"

	def get_info(self, sensor_id: int):
		"""
		Fetch the sensor info from the server.

		Parameters
		----------
		sensor_id : int
			ID of the sensor (plant).

		Returns
		-------
		name : str
			Display name of the sensor (plant).
		"""
		endpoint = self.MICHURIN_ENDPOINT + f"sensors/{sensor_id}"
		headers = {"Authorization": self.MICHURIN_TOKEN}
		res = requests.get(endpoint, headers=headers)

		assert res.status_code == 200
		res_json = res.json()
		name = res_json['display_name']
		return name

	def get_values(self, sensor_id: int):
		"""
		Fetch the sensor data from the server.

		Parameters
		----------
		sensor_id : int
			ID of the sensor (plant).

		Returns
		-------
		moistureRelative : float
			Moisture level (latest value).
		timestamp : datetime.datetime
			Measurement time.
		"""
		endpoint = self.MICHURIN_ENDPOINT + f"sensors/{sensor_id}/data/latest"
		headers = {"Authorization": self.MICHURIN_TOKEN}
		res = requests.get(endpoint, headers=headers)

		assert res.status_code == 200
		res_json = res.json()
		# print(res_json)

		# value = res_json['data']['value']
		moistureRelative = res_json['data']['moistureRelative']
		assert type(moistureRelative) == float
		timestamp = parser.parse(res_json['data']['timestamp'])

		return moistureRelative, timestamp

	def show(self, sensor_id: int):
		"""
		Build and show the indicator.

		Parameters
		----------
		sensor_id : int
			ID of the sensor (plant) to be displayed.
		"""
		try:
			info = self.get_info(sensor_id)
		except Exception as e:
			info = None

		try:
			moistureRelative, timestamp = self.get_values(sensor_id)
		except Exception as e:
			moistureRelative = None
			timestamp = None

		if moistureRelative is not None:
			value_f = f"{(moistureRelative * 100):.1f}%"
			if moistureRelative > 0.5:
				plant_indicator = f"{self.faded_green}{self.RESET}"
			elif moistureRelative > 0.3:
				plant_indicator = f"{self.faded_yellow}{self.RESET}"
			else:
				plant_indicator = f"{self.faded_red}{self.RESET}"
		else:
			value_f = "--"
			plant_indicator = ""

		if timestamp is not None:
			now = dt.now(tz=pytz.timezone('utc'))
			if now - timestamp > timedelta(hours=3):
				plant_indicator += " (offline) "

		# print(f"[ мичурин {plant_indicator} {value_f} ]")
		return f"{self.RESET}[ {plant_indicator}  {value_f} ]"


if __name__ == "__main__":

	# ID of your plant
	SENSOR = 5

	mp = MichurinPolybar()
	indicator = mp.show(SENSOR)
	print(indicator)
