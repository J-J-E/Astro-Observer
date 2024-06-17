# Astronomy Utils Usage Guide

This guide provides instructions on how to use the functions available in the `astronomy_utils` module. The module includes utilities to find visible planets from a given location and to determine the next occurrences when a specific planet will be visible.

## Requirements

```python
pip install -r requirements.txt
```

## Finding Visible Planets

To find all visible planets at a specific date, time, and location, use the `find_visible_planets` function.

### Example Usage

```python
from astronomy_utils import find_visible_planets, get_planet_visibility

# Define location and datetime
location_lat = 34.5400  # Prescott, Arizona latitude
location_lon = -112.4685  # Prescott, Arizona longitude
year = 2024
month = 6
day = 25
hour = 3
minute = 00

# Find all visible planets at the specified datetime and location
find_visible_planets(location_lat, location_lon, year, month, day, hour, minute)
```

## Finding Next Occurrences of a Specific Planet

To find the next occurrences when a specific planet will be visible from a given location, use the `get_planet_visibility` function.

### Example Usage

```python
from astronomy_utils import get_planet_visibility

# Define location and planet details
location_lat = 34.5400  # Downtown Phoenix, Arizona latitude
location_lon = -112.4685  # Downtown Phoenix, Arizona longitude
planet_name = 'saturn'
number_of_occurrences = 7

# Find the next occurrences of the specified planet visibility at the location
get_planet_visibility(location_lat, location_lon, planet_name, number_of_occurrences)
```
