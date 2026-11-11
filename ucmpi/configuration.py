"""
Comfort configuration import.
"""

import xml.etree.ElementTree as ET


class ComfortConfiguration:

    def __init__(self):

        self.zones = {}
        self.outputs = {}
        self.flags = {}
        self.counters = {}        
        self.sensors = {}

    def load_xml(self, filename):

        tree = ET.parse(filename)

        root = tree.getroot()

        zones = root.find("Zones")

        if zones is None:
            return

        for zone in zones.findall("Zone"):

            number = int(
                zone.get("Number", "0")
            )

            name = zone.get(
                "Name",
                f"Zone{number}"
            )

            self.zones[number] = name

        print(
            f"Loaded "
            f"{len(self.zones)} zones, "
            f"{len(self.outputs)} outputs, "
            f"{len(self.flags)} flags, "
            f"{len(self.counters)} counters, "
            f"{len(self.sensors)} sensors"
        )


    def get_zone_name(
        self,
        zone_number
    ):

        return self.zones.get(
            zone_number,
            f"Zone {zone_number}"
        )
        
    def get_output_name(
        self,
        output_number
    ):

        return self.outputs.get(
            output_number,
            f"Output {output_number}"
        )


    def get_flag_name(
        self,
        flag_number
    ):

        return self.flags.get(
            flag_number,
            f"Flag {flag_number}"
        )


    def get_counter_name(
        self,
        counter_number
    ):

        return self.counters.get(
            counter_number,
            f"Counter {counter_number}"
        )


    def get_sensor_name(
        self,
        sensor_number
    ):

        return self.sensors.get(
            sensor_number,
            f"Sensor {sensor_number}"
        )