import pywapi
import database


def getweather(location, manualweather):
    try:
        if not manualweather:
            locationid = pywapi.get_location_ids(location)

            for key in locationid:
                locationid = key
        else:
            locationid = manualweather
        weather = pywapi.get_weather_from_weather_com(str(locationid), units='imperial')
        condition = str(weather['current_conditions']['text']).lower()
        feels_like = str(weather['current_conditions']['feels_like'])
        temperature = str(weather['current_conditions']['temperature'])
        wind = str(weather['current_conditions']['wind']['speed'])
        humidity = str(weather['current_conditions']['humidity'])
        location = str(weather['location']['name'])
        if wind == "calm":
            wind = f"the wind is {wind}"
        else:
            wind = f"and wind at {wind} mph"
        if condition == "":
            final = f"It is {temperature}° with humidity at {humidity}% and wind at {wind} mph in {location}. It feels like {feels_like}°\n\n"
        else:
            final = f"""It is {condition} and {temperature}° with humidity at {humidity}% 
    {wind} in {location}. It feels like {feels_like}°\n\n"""
        return final

    except Exception as e:
        print(location + " has an invalid location for weather!")
        database.log(f"weather", str({location}), None, None, None, None, "Weather error, most likely invalid location.")
        return ""


def getallweather(location, manualweather):
    try:
        if not manualweather:
            locationid = pywapi.get_location_ids(location)

            for key in locationid:
                locationid = key
        else:
            locationid = manualweather
        weather = pywapi.get_weather_from_weather_com(str(locationid), units='imperial')
        final = weather['current_conditions']['temperature']
        if final == '':
            return 50  # For handling exceptions if the site returns null
        else:
            return final

    except Exception as e:
        print(location + " Error trying to get all weather location for stats.")
        print(str(e))
        database.log(f"weather", str({location}), None, None, None, None, "Weather error, most likely invalid location. " + str(e))
        return 50  # For handling exceptions if the site returns null
