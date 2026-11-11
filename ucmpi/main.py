from comfort import ComfortConnection
from protocol import ComfortProtocol
from mqtt import MQTTPublisher

from models import (
    ZoneEvent,
    ModeChangeEvent,
    LoginEvent,
    ZoneStateDumpEvent
)

from state import SystemState

from pathlib import Path

from configuration import (
    ComfortConfiguration
)

from homeassistant import (
    HomeAssistantDiscovery
)


def main():

    comfort = ComfortConnection()

    protocol = ComfortProtocol()

    mqtt = MQTTPublisher()

    state = SystemState()
    
    previous_alarm_status = None

    config = ComfortConfiguration()
    
    login_complete = False

    config_file = (
        Path(__file__).resolve().parent
        / "comfort_export.txt"
    )

    config.load_xml(str(config_file))
    print("Zone 18:", config.get_zone_name(18))
    print("Zone 19:", config.get_zone_name(19))
    print("Zone 31:", config.get_zone_name(31))
    print("Zone 39:", config.get_zone_name(39))
    print("Output 1:", config.get_output_name(1))
    print("Flag 1:", config.get_flag_name(1))
    print("Counter 1:", config.get_counter_name(1))
    print("Sensor 1:", config.get_sensor_name(1))



    ha = HomeAssistantDiscovery(
        mqtt
    )

    ha.publish_alarm_discovery()

    ha.publish_alarm_mode_sensor()

    #
    #
    # Publish Zone Discovery
    #
    for zone_number, zone_name in (
        config.zones.items()
    ):

        # Skip unused zones
        if zone_name.startswith("Zone"):
            continue

        ha.publish_zone_discovery(
            zone_number,
            zone_name
        )
        
    #
    # Connect once
    #
    comfort.connect()
    comfort.login("1991")

    #
    # Startup synchronization test
    #
    # comfort.send_command("M?")

    print("Waiting for Comfort messages...\n")

    while True:

        message = comfort.read_message()

        if not message:
            continue

        event = protocol.parse(message)

        if message.startswith("LU"):

            print(
                f"Comfort Login -> {message}"
            )

            login_complete = True

        if login_complete:

            login_complete = False

            print("LOGIN COMPLETE")

            comfort.send_command("u?00")
            comfort.send_command("U?")
            comfort.send_command("V?")
            comfort.send_command("v?")
            comfort.send_command("a?")
            comfort.send_command("b?00")
            comfort.send_command("f?00")
            comfort.send_command("M?")
            comfort.send_command("Y?")
            comfort.send_command("Z?")
            comfort.send_command("y?")
            comfort.send_command("z?")

        if not event:
            print(
                f"Unhandled message: "
                f"{message}"
            )
            continue

        #
        # Update system state
        #
        
        state.update(event)

        #
        # Display events
        #

        if isinstance(event, ZoneStateDumpEvent):

            print(
                "ZONE BITMAP:",
                event.bitmap
            )

            bitmap = bytes.fromhex(
                event.bitmap
            )

            #
            # Decode current state of every configured zone
            #
            for zone_number, zone_name in (
                config.zones.items()
            ):

                # Skip unused zones
                if zone_name.startswith("Zone"):
                    continue

                byte_index = (
                    zone_number - 1
                ) // 8

                bit_index = (
                    zone_number - 1
                ) % 8

                #
                # Ignore zones outside bitmap range
                #
                if byte_index >= len(bitmap):
                    continue

                zone_state = bool(
                    bitmap[byte_index]
                    & (1 << bit_index)
                )

                print(
                    f"STARTUP: "
                    f"{zone_name} -> "
                    f"{'ON' if zone_state else 'OFF'}"
                )

                mqtt.publish_zone(
                    zone_number,
                    zone_state
                )

                ha.publish_zone_state(
                    zone_number,
                    zone_state
                )

            continue

        
        if isinstance(event, ZoneEvent):

            zone_name = config.get_zone_name(
                event.zone
            )

            print(
                f"{zone_name} -> "
                f"{'ON' if event.state else 'OFF'}"
            )

            mqtt.publish_zone(
                event.zone,
                event.state
            )

            ha.publish_zone_state(
                event.zone,
                event.state
            )

        else:

            print(event)

        #
        # Publish Home Assistant alarm state
        #
        
        alarm_status = (
            state.get_alarm_status()
        )

        if alarm_status != previous_alarm_status:

            print(
                f"Alarm Status: "
                f"{alarm_status}"
        )

        ha.publish_alarm_state(
            alarm_status
        )

        previous_alarm_status = (
            alarm_status
        )
        
        #
        # Publish alarm mode
        #
        if isinstance(event, ModeChangeEvent):

            mqtt.client.publish(
                "comfort/alarm/mode",
                event.mode,
                retain=True
            )

if __name__ == "__main__":
    main()