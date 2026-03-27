# The Tracker

## Overview
The tracker runs a micropython script to continuously check and transmit temperature and humidity data to the hub, over wifi.

## Requirements
requirements.txt contains all required libraries/packages. Note that these requirements must be installed on the tracker controller itself, not the machine flashing code to the controller. It is recommended to use an IDE that can download modules from a requirements.txt file.

## How to Use

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Resources

- [Micropython Docs](https://docs.micropython.org/en/latest/)
- [Urequests Module Docs](https://makeblock-micropython-api.readthedocs.io/en/latest/public_library/Third-party-libraries/urequests.html)
- [DHT20 Micropython Module](https://github.com/flrrth/pico-dht20). NOTE: The module used in our project is a slightly modified version of this module.
