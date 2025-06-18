from astronomy_utils import find_visible_planets

# Example t0 find all visible planets at specific datetime location
location_lat = 34.5400  # Prescott, Arizona latitude
location_lon = -112.4685  # Prescott, Arizona longitude
year = 2025
month = 3
day = 13
hour = 00
minute = 00
find_visible_planets(location_lat, location_lon, year, month, day, hour, minute)
