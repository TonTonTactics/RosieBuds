** Check the corresponding folders for the README **

# RosieBuds
Rosiebuds is an IoT-based plant monitoring system that tracks environmental conditions and helps users ensure their plants are thriving. It combines hardware, backend processing, and a user-friendly web interface into one seamless solution.

![Image (2)](https://github.com/user-attachments/assets/31a70585-1556-4cdc-8bde-9de714a0f4e9)


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

<img width="145" height="258" alt="Screenshot 2026-03-30 at 7 39 08 PM" src="https://github.com/user-attachments/assets/2da46ac5-934c-46e4-8cec-449357c9c30d" />

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

  <img width="206" height="258" alt="Screenshot 2026-03-30 at 7 39 19 PM" src="https://github.com/user-attachments/assets/6dad4b3a-6e49-492b-b109-f0a13b04ee24" />

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
  
![Image (1)](https://github.com/user-attachments/assets/5d98cee3-ce5b-41fc-ad22-0ba4492b3808)
![Image](https://github.com/user-attachments/assets/c3ff4864-6408-4313-96d9-817c0611a3d1)

## Made with care, Monday-46

Great work guys!

<img width="396" height="288" alt="Screenshot 2026-03-30 at 11 25 49 PM" src="https://github.com/user-attachments/assets/2ac6909d-a67a-4928-b6e1-b16c0de74ec9" />


## License

[MIT](https://choosealicense.com/licenses/mit/)
