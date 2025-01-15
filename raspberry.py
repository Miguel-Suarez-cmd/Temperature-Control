#!/usr/bin/env python3

import time
import requests
from seeed_dht import DHT
from grove.display.jhd1802 import JHD1802
from mraa import getGpioLookup
from upm import pyupm_buzzer as upmBuzzer

# ThingSpeak Configuration
THINGSPEAK_API_KEY = 'XXXXXXXXXX'  
THINGSPAK_BASE_URL = 'https://api.thingspeak.com/update'

# Temperature thresholds
TEMP_LOW_THRESHOLD = 10
TEMP_HIGH_THRESHOLD = 34

def send_to_thingspeak(temperature, humidity, alert=None):
    """
    Send temperature and humidity data to ThingSpeak.
    Optionally include an alert message in 'field3'.
    """
    payload = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': temperature,  # Temperature data
        'field2': humidity,     # Humidity data
    }
    if alert:
        payload['field3'] = alert  # Optional alert message

    try:
        response = requests.get(THINGSPAK_BASE_URL, params=payload)
        response.raise_for_status()
        if response.text.startswith('0'):
            print("Failed to update ThingSpeak. Response:", response.text)
        else:
            print("Data sent to ThingSpeak successfully!")
    except requests.RequestException as e:
        print("Error sending data to ThingSpeak:", e)

def main():
    # Grove - 16x2 LCD (White on Blue) connected to I2C port
    lcd = JHD1802()

    # Grove - Temperature & Humidity Sensor connected to port D5
    sensor = DHT('11', 5)

    # Grove - Buzzer connected to D6
    buzzer = upmBuzzer.Buzzer(getGpioLookup('GPIO12'))

    while True:
        humi, temp = sensor.read()

        # Handle invalid sensor readings
        if humi is None or temp is None:
            print("Sensor error: Unable to read data.")
            lcd.setCursor(0, 0)
            lcd.write("Sensor error     ")
            time.sleep(2)
            continue

        # Print to console
        print('Temperature: {}C, Humidity: {}%'.format(temp, humi))

        # Display on the LCD
        lcd.setCursor(0, 0)
        lcd.write('Temp: {0:2}C '.format(temp))  # Clear extra characters
        lcd.setCursor(1, 0)
        lcd.write('Humidity: {0:5}%  '.format(humi))

        # Check temperature thresholds
        alert_message = none
        if temp < TEMP_LOW_THRESHOLD:
            alert_message = "Low Temp"
            lcd.setCursor(1, 0)
            lcd.write("Temp below 10C ")
            buzzer.playSound(upmBuzzer.BUZZER_DO, 200000)  # Activate buzzer
        elif temp > TEMP_HIGH_THRESHOLD:
            alert_message = "High Temp"
            lcd.setCursor(1, 0)
            lcd.write("Temp above 34C ")
            buzzer.playSound(upmBuzzer.BUZZER_DO, 200000)  # Activate buzzer

        # ThingSpeak will know inmideatly of the alert just by reading the data
        

        time.sleep(300)  # Wait for 5 minutes before taking another reading

if __name__ == '__main__':
    main()
