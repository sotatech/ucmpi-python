"""
MQTT publishing.
"""

import json
import time

import paho.mqtt.client as mqtt


class MQTTPublisher:

    def __init__(
        self,
        broker="192.168.16.101",
        port=1883
    ):

        print("Starting MQTT...")

        self.client = mqtt.Client()
        
        self.client.username_pw_set(
            username="mqtt",
            password="1991Dalton"
        )

        print("Connecting to broker...")

        self.client.connect(
            broker,
            port,
            60
        )

        self.client.loop_start()

        print(
            f"Connected to MQTT broker "
            f"{broker}:{port}"
        )

    def publish_zone(
        self,
        zone: int,
        state: bool
    ):

        topic = (
            f"uhai/core/status/"
            f"zone/{zone}/value"
        )

        payload = {
            "value": 1 if state else 0,
            "notify": True,
            "timestamp": int(
                time.time() * 1000
            )
        }

        print(f"Publishing {topic}")

        result = self.client.publish(
            topic,
            json.dumps(payload),
            retain=True
        )

        print(
            f"Publish result: "
            f"{result.rc}"
        )