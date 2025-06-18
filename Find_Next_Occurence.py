from astronomy_utils import get_planet_visibility

# Example to find next occurrence of specific body
location_lat = 34.5400  # Prescott, Arizona latitude
location_lon = -112.4685  # Prescott, Arizona longitude
planet_name = 'saturn'
number_of_occurrences = 5

get_planet_visibility(location_lat, location_lon, planet_name, number_of_occurrences)