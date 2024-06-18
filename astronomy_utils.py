from skyfield.api import Topos, load
from skyfield.almanac import find_discrete, risings_and_settings
from datetime import datetime, timedelta
import pytz
from timezonefinder import TimezoneFinder
import matplotlib.pyplot as plt

# Mapping of user-friendly planet names to their Skyfield barycenter names
planet_name_mapping = {
    'sun': 'sun',
    'moon': 'moon',
    'mercury': 'mercury barycenter',
    'venus': 'venus barycenter',
    'earth': 'earth barycenter',
    'mars': 'mars barycenter',
    'jupiter': 'jupiter barycenter',
    'saturn': 'saturn barycenter',
    'uranus': 'uranus barycenter',
    'neptune': 'neptune barycenter',
    'pluto': 'pluto barycenter',
}

def format_direction(degrees):
    """
    Convert azimuth degrees to human-readable direction.

    Parameters:
    - degrees (float): Azimuth angle in degrees.

    Returns:
    - str: Human-readable direction (e.g., 'N', 'NE', 'E', ...).
    """
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    return directions[int((degrees + 11.25) // 22.5) % 16]

def find_visible_planets(location_lat, location_lon, year, month, day, hour, minute):
    """
    Finds which planets are above the horizon at a specified date and time for a given location.

    Parameters:
    - location_lat (float): Latitude of the observer's location in degrees.
    - location_lon (float): Longitude of the observer's location in degrees.
    - year (int): Year of the observation.
    - month (int): Month of the observation (1-12).
    - day (int): Day of the month of the observation.
    - hour (int): Hour of the observation (24-hour format).
    - minute (int): Minute of the observation.

    Prints:
    - Prints observation date and time, observer's location, and visible planets with their positions.
    """
    # Load ephemeris data
    planets = load('de421.bsp')

    # Define location based on latitude and longitude
    location = Topos(latitude_degrees=location_lat, longitude_degrees=location_lon)

    # Determine timezone automatically based on coordinates
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location_lon, lat=location_lat)

    if timezone_str:
        tz = pytz.timezone(timezone_str)
    else:
        raise ValueError("Could not determine timezone for the given coordinates.")

    # Create a datetime object in local time and localize it
    local_time = tz.localize(datetime(year, month, day, hour, minute))

    # Convert local time to UTC
    utc_time = local_time.astimezone(pytz.utc)

    # Convert UTC time to Skyfield's timescale
    ts = load.timescale()
    t = ts.from_datetime(utc_time)

    # Define planets
    planet_names = ['moon', 'mercury barycenter', 'venus barycenter', 'mars barycenter', 'jupiter barycenter', 'saturn barycenter',
                    'uranus barycenter', 'neptune barycenter', 'pluto barycenter']

    # Calculate the apparent altitudes, azimuths, and directions of each planet from the observer's position on Earth
    visible_planets = {}
    for name in planet_names:
        planet = planets[name]
        astrometric = (planets['earth'] + location).at(t).observe(planet)
        alt, az, distance = astrometric.apparent().altaz()

        # Convert azimuth to degrees and get human-readable direction
        azimuth_degrees = az.degrees
        direction = format_direction(azimuth_degrees)

        # Store planet data in visible_planets dictionary
        if alt.degrees > 0:
            visible_planets[name.replace(" barycenter", "")] = (alt.degrees, azimuth_degrees, direction)

    # Print observation date, time, location, and visible planets with their positions
    print(f"Observation Date and Time (local time): {local_time.strftime('%Y-%m-%d %I:%M %p')} {tz.zone}")
    print(f"Observer's Location: Latitude {location_lat}, Longitude {location_lon}\n")

    if visible_planets:
        print("Visible planets and their positions:")
        for planet, (altitude, azimuth, direction) in visible_planets.items():
            message = f" - {planet}: Altitude {altitude:.2f} degrees, Azimuth {azimuth:.2f} degrees ({direction})"
            caution_message = " -> (CAUTION: Altitude <10 degrees above horizon, planet may not be visible.)"
            if altitude < 10:
                print(message + caution_message)
            else:
                print(message)
    else:
        print("No planets are currently above the horizon at the specified time and location.")

def get_planet_visibility(location_lat, location_lon, planet_name, number_of_occurrences=1):
    now = datetime.now()
    start_date = datetime(now.year, now.month, now.day, now.hour, now.minute)

    if planet_name.lower() in planet_name_mapping:
        planet_name_barycenter = planet_name_mapping[planet_name.lower()]
    else:
        planet_name_barycenter = planet_name.lower() + ' barycenter'

    occurrences = _calculate_planet_visibility_period(location_lat, location_lon, start_date, planet_name_barycenter, number_of_occurrences)

    if occurrences:
        print(f'Celestial Body: {planet_name}')
        print(f"# of Future Occurrences Requested: {len(occurrences)}")

        for occurrence in occurrences:
            formatted_message = _format_visibility_message(**occurrence)
            print(formatted_message)
    else:
        print(f"No occurrences of {planet_name.capitalize()} rising in the next 30 days.")

def _calculate_planet_visibility_period(location_lat, location_lon, start_date, planet_name, number_of_occurrences):
    planets = load('de421.bsp')
    ts = load.timescale()
    location = Topos(latitude_degrees=location_lat, longitude_degrees=location_lon)

    # Determine timezone automatically based on coordinates
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location_lon, lat=location_lat)

    if timezone_str:
        tz = pytz.timezone(timezone_str)
    else:
        raise ValueError("Could not determine timezone for the given coordinates.")

    # Ensure start_date is naive before localizing
    if start_date.tzinfo is not None:
        start_date = start_date.replace(tzinfo=None)

    start_date = tz.localize(start_date)
    start_time = ts.utc(start_date.astimezone(pytz.utc))
    end_time = ts.utc((start_date + timedelta(days=30)).astimezone(pytz.utc))
    planet = planets[planet_name]
    f = risings_and_settings(planets, planet, location)
    times, is_rise = find_discrete(start_time, end_time, f)
    occurrences = []

    for i in range(len(times) - 1):
        if is_rise[i]:
            rise_time = times[i]
            set_time = times[i + 1]
            observer = planets['earth'] + location

            # Calculate max altitude by checking altitudes at more intervals
            interval_count = 50  # Increase the number of intervals
            max_alt = float('-inf')
            for j in range(interval_count + 1):
                time = rise_time + (set_time - rise_time) * j / interval_count
                alt, _, _ = observer.at(time).observe(planet).apparent().altaz()
                max_alt = max(max_alt, alt.degrees)

            # Get rise direction and azimuth
            alt, az, _ = observer.at(rise_time).observe(planet).apparent().altaz()
            direction = az.degrees
            direction_str = format_direction(direction)

            duration = (set_time.utc_datetime() - rise_time.utc_datetime()).total_seconds() / 3600
            rise_time_local = rise_time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(tz)
            set_time_local = set_time.utc_datetime().replace(tzinfo=pytz.utc).astimezone(tz)

            occurrences.append({
                'rise_time': rise_time_local,
                'direction': direction_str,
                'azimuth': az.degrees,  # Include azimuth
                'duration': duration,
                'max_alt': max_alt,
                'set_time': set_time_local
            })

            if len(occurrences) == number_of_occurrences:
                break

    return occurrences

def _format_visibility_message(rise_time, direction, azimuth, duration, max_alt, set_time):
    rise_time_formatted = rise_time.strftime('%Y-%m-%d %I:%M %p')
    set_time_formatted = set_time.strftime('%Y-%m-%d %I:%M %p')

    formatted_message = (
        f"{rise_time_formatted}: rise from {direction} ({azimuth:.2f} degrees), visible for {duration:.2f} hours, "
        f"maximum altitude of ~{max_alt:.2f} degrees, set on {set_time_formatted}."
    )
    return formatted_message


def draw_planet_motion(location_lat, location_lon, planet_name, year, month, day):
    """
    Draws a PNG image of the motion of a planetary body.

    Parameters:
    - location_lat (float): Latitude of the observer's location in degrees.
    - location_lon (float): Longitude of the observer's location in degrees.
    - planet_name (str): Name of the planetary body.
    - year (int): Year of the observation.
    - month (int): Month of the observation (1-12).
    - day (int): Day of the month of the observation (1-31).
    """
    planets = load('de421.bsp')
    ts = load.timescale()
    location = Topos(latitude_degrees=location_lat, longitude_degrees=location_lon)

    # Determine timezone automatically based on coordinates
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location_lon, lat=location_lat)

    if timezone_str:
        tz = pytz.timezone(timezone_str)
    else:
        raise ValueError("Could not determine timezone for the given coordinates.")

    # Create a datetime object in local time and localize it
    local_date = datetime(year, month, day)
    start_date = tz.localize(local_date)

    start_time = ts.utc(start_date.astimezone(pytz.utc))
    end_time = ts.utc((start_date + timedelta(days=2)).astimezone(pytz.utc))  # Extended to 2 days
    planet = planets[planet_name_mapping[planet_name.lower()]]

    f = risings_and_settings(planets, planet, location)
    times, is_rise = find_discrete(start_time, end_time, f)

    if len(times) < 2:
        print("The planet does not rise and set within the specified date range.")
        return

    rise_time = None
    set_time = None

    for i in range(len(times) - 1):
        if is_rise[i] and not is_rise[i + 1]:
            rise_time = times[i]
            set_time = times[i + 1]
            break

    if rise_time is None or set_time is None:
        print("The planet does not rise and set within the specified date range.")
        return

    observer = planets['earth'] + location

    # Include exact rise and set times
    times_list = [rise_time.utc_datetime()]
    time_interval = timedelta(hours=1)
    current_time = rise_time.utc_datetime() + time_interval

    while current_time < set_time.utc_datetime():
        times_list.append(current_time)
        current_time += time_interval

    # Ensure set time is included in the list
    times_list.append(set_time.utc_datetime())

    altitudes = []
    azimuths = []

    for time in times_list:
        t = ts.utc(time)
        alt, az, _ = observer.at(t).observe(planet).apparent().altaz()
        altitudes.append(alt.degrees)
        azimuths.append(az.degrees)

    fig, ax = plt.subplots()

    # Plot horizon
    ax.plot([azimuths[0], azimuths[-1]], [0, 0], 'k-')
    ax.text(azimuths[0], -2, f'{format_direction(azimuths[0])} ({(times_list[0].astimezone(tz)).strftime("%Y-%m-%d")})',
            horizontalalignment='center')
    ax.text(azimuths[-1], -2,
            f'{format_direction(azimuths[-1])} ({(times_list[-1].astimezone(tz)).strftime("%Y-%m-%d")})',
            horizontalalignment='center')

    # Plot the motion of the planet
    ax.plot(azimuths, altitudes, 'b-')
    ax.scatter(azimuths, altitudes, color='red')

    for i, time in enumerate(times_list):
        local_time = time.astimezone(tz)
        ax.text(azimuths[i], altitudes[i], local_time.strftime('%H:%M'), fontsize=8, verticalalignment='bottom',
                horizontalalignment='right')

    ax.set_xlabel('Azimuth (degrees)')
    ax.set_ylabel('Altitude (degrees)')
    ax.set_title(
        f'Motion of {planet_name.capitalize()} on {start_date.strftime("%Y-%m-%d")} and {(start_date + timedelta(days=1)).strftime("%Y-%m-%d")}')
    ax.set_ylim(bottom=-5)

    plt.savefig(f'{planet_name}_motion.png')
    plt.close()

    print(f"The motion of {planet_name.capitalize()} has been saved as '{planet_name}_motion.png'.")


