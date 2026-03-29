""" Processing of data

Process data into words.

Antony Wiegand, McMaster, 2026
"""

def rating(sensor_id, selected_data, guide_data):
    m = selected_data.get("moisture")
    t = selected_data.get("temperature")
    h = selected_data.get("humidity")

    if m is None or t is None or h is None or guide_data is None:
        return [{
            "sensor_id": sensor_id,
            "water_next": "No Data",
            "temperature_rating": "No Data",
            "humidity_rating": "No Data"
        }]

    # moisture / watering
    low_m = guide_data["opt_moisture_low"]
    high_m = guide_data["opt_moisture_high"]

    if m < low_m:
        water = "Water now"
    elif m > high_m:
        water = "Too wet"
    else:
        water = "Good"

    # temperature
    low_t = guide_data["opt_temperature_low"]
    high_t = guide_data["opt_temperature_high"]

    if t < low_t:
        temp_rating = "Too Cold"
    elif t > high_t:
        temp_rating = "Too Hot"
    else:
        temp_rating = "Good"

    # humidity
    low_h = guide_data["opt_humidity_low"]
    high_h = guide_data["opt_humidity_high"]

    if h < low_h:
        hum_rating = "Too Dry"
    elif h > high_h:
        hum_rating = "Too Humid"
    else:
        hum_rating = "Good"

    return [{
        "sensor_id": sensor_id,
        "water_next": water,
        "temperature_rating": temp_rating,
        "humidity_rating": hum_rating
    }]