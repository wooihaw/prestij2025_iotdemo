import time
import paho.mqtt.client as mqtt
from json import dumps
from random import randint # Import the random module

def main():
    # Configure MQTT
    mqtt_broker = "demo.thingsboard.io"  # Adjust this to your MQTT broker
    mqtt_topic = "v1/devices/me/telemetry"

    mqtt_users1 =["MMU2025heart1a", 
                  "MMU2025heart1b", 
                  "MMU2025heart1c", 
                  "MMU2025heart1d", 
                  "MMU2025heart1e", 
                  "MMU2025heart1f",
                  "MMU2025heart1g",
                  "MMU2025heart1h",
    ]

    mqtt_users2 =["MMU2025heart2a", 
                  "MMU2025heart2b", 
                  "MMU2025heart2c", 
                  "MMU2025heart2d", 
                  "MMU2025heart2e", 
                  "MMU2025heart2f",
                  "MMU2025heart2g",
                  "MMU2025heart2h",
    ]

    mqtt_users3 =["MMU2025heart3a", 
                  "MMU2025heart3b", 
                  "MMU2025heart3c", 
                  "MMU2025heart3d", 
                  "MMU2025heart3e", 
                  "MMU2025heart3f",
                  "MMU2025heart3g",
                  "MMU2025heart3h",                  
    ]
    
    mqtt_users = mqtt_users1 + mqtt_users2 + mqtt_users3

    mqtt_clients = []

    for user in mqtt_users:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(user)
        client.connect(mqtt_broker, 1883, 60)
        mqtt_clients.append(client)
        client.loop_start() # Start MQTT client loop to handle reconnections and messages

    try:
        while True:
            # Generate random heart rate within normal range (60-100 bpm)
            random_heart_rate = round(randint(60.0, 100.0), 2)
            
            # Generate random respiratory rate within normal range (12-20 breaths per minute)
            random_respi_rate = round(randint(12.0, 20.0), 2)
            
            payload = dumps({'heart_rate': random_heart_rate, 'respi_rate': random_respi_rate})
            
            for client in mqtt_clients:
                client.publish(mqtt_topic, payload)
                
            print(f'Published: Heart Rate: {random_heart_rate}, Respiratory Rate: {random_respi_rate}')
            
            time.sleep(3) # Publish every 3 seconds

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        for client in mqtt_clients:
            client.loop_stop() # Stop the MQTT client loop
            client.disconnect()
        print("Disconnected from MQTT broker")

if __name__ == "__main__":
    main()