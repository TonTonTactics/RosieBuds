# RosieBuds
Rosiebuds is an IoT-based plant monitoring system that tracks environmental conditions and helps users ensure their plants are thriving. It combines hardware, backend processing, and a user-friendly web interface into one seamless solution.

The system is composed of three main components:

## The Tracker

The Tracker is a lightweight sensor device responsible for collecting environmental data.
- Powered by an ESP32 microcontroller
- Equipped with:
  - IP65 Capacitive Soil Moisture Sensor
  - DHT Sensor (temperature & humidity)
- Collects:
  - Soil moisture
  - Temperature
  - Humidity
- Transmits real-time data to the central hub

## The Hub

The Hub acts as the brain of the system, storing and processing incoming data.
- Hosted on a Raspberry Pi 4
- Uses:
  - FastAPI for backend API services
  - SQLite for data storage
- Responsibilities:
  - Receives and stores sensor data
  - Processes data based on plant-specific optimal ranges
  - Determines whether conditions are optimal or not

## The Web App

The web application provides an intuitive interface for users to interact with their plant data.
- Built with React
- Features:
  - Real-time dashboard displaying plant conditions
  - Plant selection for customized optimal ranges
- A built-in guidebook with care tips, including:
  - Sun exposure
  - Planting instructions
  - Watering frequency
  - (factors that cannot be measured directly by sensors)

## License

[MIT](https://choosealicense.com/licenses/mit/)
