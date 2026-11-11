"""
Home Assistant MQTT Discovery support.
"""

import json


class HomeAssistantDiscovery:
    
    def zones_device(self):

        return {
            "identifiers": [
                "comfort_alarm_zones"
            ],
            "name":
                "Cytech Comfort Alarm Zones",
            "manufacturer":
                "Cytech",
            "model":
                "Comfort"
        }
    
    def publish_zone_discovery(
        self,
        zone_number,
        zone_name
    ):

        entity_name = (
            zone_name
            .lower()
            .replace(" ", "_")
        )

        topic = (
            "homeassistant/"
            "binary_sensor/"
            f"comfort_zone_{zone_number}/"
            "config"
        )

        payload = {
            "name": zone_name,

            "unique_id":
                f"comfort_zone_{zone_number}",

            "state_topic":
                (
                    "comfort/zone/"
                    f"{zone_number}/state"
                ),

            "payload_on": "ON",

            "payload_off": "OFF",

            "device_class": "opening",

            "device":
                self.zones_device()
        }

        self.mqtt.client.publish(
            topic,
            json.dumps(payload),
            retain=True
        )

        print(
            f"HA Zone Discovery -> "
            f"{zone_name}"
    )
        
    def publish_zone_state(
        self,
        zone_number,
        zone_state
    ):

        topic = (
            f"comfort/zone/"
            f"{zone_number}/state"
        )

        payload = (
            "ON"
            if zone_state
            else "OFF"
        )

        self.mqtt.client.publish(
            topic,
            payload,
            retain=True
        )
        
        

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