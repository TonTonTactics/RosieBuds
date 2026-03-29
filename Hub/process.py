""" Processing of data

Process data into words.

Antony Wiegand, McMaster, 2026
"""

from statistics import mean, median, StatisticsError

COMPARISONREADINGS = 6
MAXTEMPVARIANCE = 5
MAXHUMIDVARIANCE = 20


def validate_sensor_data(sensors):
    m = [r.moisture for r in sensors]
    t = [r.temperature for r in sensors]
    h = [r.humidity for r in sensors]

    try:
        median_m = median(m)
    except StatisticsError:
        median_m = None

    try:
        tempdeltas = []
        for datapoint in range(1, len(t) - 1):
            tempdeltas.append(t[datapoint] - t[datapoint + 1])

        tempprediction = t[1] + mean(tempdeltas)

        if abs(t[0] - tempprediction) > MAXTEMPVARIANCE:
            validated_t = None
        else:
            validated_t = t[0]
    except (StatisticsError, IndexError):
        validated_t = None

    try:
        humiddeltas = []
        for datapoint in range(1, len(h) - 1):
            humiddeltas.append(h[datapoint] - h[datapoint + 1])

        humidprediction = h[1] + mean(humiddeltas)

        if abs(h[0] - humidprediction) > MAXHUMIDVARIANCE:
            validated_h = None
        else:
            validated_h = h[0]
    except (StatisticsError, IndexError):
        validated_h = None

    return {
        "moisture": median_m,
        "temperature": validated_t,
        "humidity": validated_h
    }


def range_rating(value, low, high):
    if value is None or low is None or high is None:
        return "No Data"
    if low <= value <= high:
        return "Good"
    return "Bad"


def water_message(value, low, high):
    if value is None or low is None or high is None:
        return "No Data"
    if value < low:
        return "Water Needed"
    if value > high:
        return "Too Wet"
    return "Good"


def rating(sensor_id, sensor_data, guide_data):
    return [{
        "sensor_id": sensor_id,
        "plant_name": guide_data.get("name"),
        "moisture": water_message(
            sensor_data.get("moisture"),
            guide_data.get("opt_moisture_low"),
            guide_data.get("opt_moisture_high")
        ),
        "temperature": range_rating(
            sensor_data.get("temperature"),
            guide_data.get("opt_temperature_low"),
            guide_data.get("opt_temperature_high")
        ),
        "humidity": range_rating(
            sensor_data.get("humidity"),
            guide_data.get("opt_humidity_low"),
            guide_data.get("opt_humidity_high")
        )
    }]