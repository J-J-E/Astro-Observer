from astronomy_utils import find_visible_planets, get_planet_visibility, draw_planet_motion

# Example t0 find all visible planets at specific datetime location
location_lat = 34.5400  # Prescott, Arizona latitude
location_lon = -112.4685  # Prescott, Arizona longitude
year = 2024
month = 6
day = 17
hour = 3
minute = 00
#find_visible_planets(location_lat, location_lon, year, month, day, hour, minute)

# Example to find next occurence of specific body
location_lat = 34.5400  # Prescott, Arizona latitude
location_lon = -112.4685  # Prescott, Arizona longitude
planet_name = 'saturn'
number_of_occurrences = 1
#get_planet_visibility(location_lat, location_lon, planet_name, number_of_occurrences)


draw_planet_motion(location_lat, location_lon, planet_name, year, month, day)