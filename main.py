from datetime import datetime
from astronomy_utils import find_visible_planets, get_planet_visibility

location_lat = 34.5400  # Prescott, Arizona latitude
location_lon = -112.4685  # Prescott, Arizona longitude
year = 2024
month = 6
day = 25
hour = 3
minute = 00


# Example t0 find all visible planets at specific datetime location
find_visible_planets(location_lat, location_lon, year, month, day, hour, minute)

print("\n\n")
# Example to find next occurence of specific body
location_lat = 33.45962348861347  # Downtown Phoenix, Arizona
location_lon = -112.06095556252873  # Downtown Phoenix, Arizona
planet_name = 'saturn'
number_of_occurrences = 7
get_planet_visibility(location_lat, location_lon, planet_name, number_of_occurrences)
