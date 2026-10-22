"""
Comfort configuration import.
"""

import xml.etree.ElementTree as ET


class ComfortConfiguration:

    def __init__(self):

        self.zones = {}

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

    def get_zone_name(
        self,
        zone_number
    ):

        return self.zones.get(
            zone_number,
            f"Zone {zone_number}"
        )