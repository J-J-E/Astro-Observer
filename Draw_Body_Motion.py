from astronomy_utils import draw_planet_motion

# Example to find next occurrence of specific body
location_lat = 34.5400  # Prescott, Arizona latitude
location_lon = -112.4685  # Prescott, Arizona longitude
planet_name = 'saturn'
year = 2025
month = 6
day = 18
draw_planet_motion(location_lat, location_lon, planet_name, year, month, day)