import pywapi


def getweather(location):
    try:
        locationid = pywapi.get_location_ids(location)
        for key in locationid:
            locationid = key
        weather = pywapi.get_weather_from_weather_com(str(locationid), units='imperial')
        condition = str(weather['current_conditions']['text']).lower()
        feels_like = str(weather['current_conditions']['feels_like'])  # Could change to exact but this is more fun for that minot wind chill
        humidity = str(weather['current_conditions']['humidity'])
        location = str(weather['location']['name'])
        if condition == "":
            final = f"It is {feels_like}° with humidity at {humidity}% in {location}."
        else:
            final = f"It is {condition} and {feels_like}° with humidity at {humidity}% in {location}."
        return final

    except Exception as e:
        print(location + " has an invalid location for weather!")

