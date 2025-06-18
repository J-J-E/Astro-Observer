from astronomy_utils import get_planet_visibility

# Example to find next occurrence of specific body
location_lat = 32.23181639440093
location_lon = -110.95347633006848
planet_name = 'saturn'
number_of_occurrences = 5

get_planet_visibility(location_lat, location_lon, planet_name, number_of_occurrences)