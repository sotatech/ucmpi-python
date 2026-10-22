"""
Home Assistant MQTT Discovery support.
"""

import json


class HomeAssistantDiscovery:

    def system_device(self):

        return {
            "identifiers": [
                "comfort_alarm_system"
            ],
            "name":
                "Cytech Comfort Alarm System",
            "manufacturer":
                "Cytech",
            "model":
                "Comfort"
        }

    def __init__(self, mqtt_client):

        self.mqtt = mqtt_client

        self.last_state = None

    def publish_alarm_discovery(self):

        topic = (
            "homeassistant/"
            "alarm_control_panel/"
            "comfort_alarm/"
            "config"
        )

        payload = {
            "name": "Comfort Alarm",
            "unique_id": "comfort_alarm",
            "state_topic":
                "comfort/alarm/state",
            "icon": "mdi:shield-home",
            "device":
                self.system_device()
        }

        self.mqtt.client.publish(
            topic,
            json.dumps(payload),
            retain=True
        )

        print(
            "HA Discovery -> "
            "Comfort Alarm"
        )

    def publish_alarm_mode_sensor(self):

        topic = (
            "homeassistant/"
            "sensor/"
            "comfort_alarm_mode/"
            "config"
        )

        payload = {
            "name":
                "Comfort Alarm Mode",
            "unique_id":
                "comfort_alarm_mode",
            "state_topic":
                "comfort/alarm/mode",
            "device":
                self.system_device()
        }

        self.mqtt.client.publish(
            topic,
            json.dumps(payload),
            retain=True
        )

    def publish_alarm_state(
        self,
        status
    ):

        mapping = {

            "off": "disarmed",

            "away": "armed_away",

            "night": "armed_night",

            "day": "armed_home",

            "vacation": "armed_vacation",

            "arming": "arming",

            "arming waiting on zone":
                "pending",

            "exit delay":
                "pending",

            "entry delay":
                "disarming"
        }

        ha_state = mapping.get(
            status,
            "unknown"
        )

        #
        # Publish only if changed.
        #
        if ha_state == self.last_state:
            return

        self.mqtt.client.publish(
            "comfort/alarm/state",
            ha_state,
            retain=True
        )

        print(
            f"HA Alarm State -> "
            f"{ha_state}"
        )

        self.last_state = ha_state