from astronomy_utils import draw_planet_motion

# Example to find next occurrence of specific body
location_lat = 32.23181639440093
location_lon = -110.95347633006848
planet_name = 'pluto'
year = 2025
month = 6
day = 18

draw_planet_motion(location_lat, location_lon, planet_name, year, month, day)
