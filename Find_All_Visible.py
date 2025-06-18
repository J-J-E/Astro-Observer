from astronomy_utils import find_visible_planets

# Example t0 find all visible planets at specific datetime location
location_lat = 32.23181639440093
location_lon = -110.95347633006848
year = 2025
month = 6
day = 18
hour = 00
minute = 12
find_visible_planets(location_lat, location_lon, year, month, day, hour, minute)
