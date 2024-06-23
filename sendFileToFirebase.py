import serial
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('/Users/govindpandey/Desktop/ayaan-ki-dua-firebase-adminsdk-d13yx-b523f1c9ad.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ayaan-ki-dua-default-rtdb.firebaseio.com/'
})

# Replace 'COM3' with your Arduino's port name
arduino_port = 'COM3'
baud_rate = 9600

# Open the serial connection
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for the connection to establish

# Reference to the Firebase database path
ref = db.reference('soilMoistureSensor')

try:
    while True:
        if ser.in_waiting > 0:
            # Read the line from the serial port
            sensor_value = ser.readline().decode('utf-8').strip()
            print(f"Read from Arduino: {sensor_value}")

            # Upload to Firebase
            ref.push({
                'timestamp': int(time.time()),
                'value': int(sensor_value)
            })
            print("Uploaded to Firebase")

except KeyboardInterrupt:
    print("Exiting program")

finally:
    ser.close()
