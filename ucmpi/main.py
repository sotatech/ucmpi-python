from comfort import ComfortConnection
from protocol import ComfortProtocol
from mqtt import MQTTPublisher

from models import (
    ZoneEvent,
    ModeChangeEvent
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

    comfort.connect()

    print("Waiting for Comfort messages...\n")

    while True:

        message = comfort.read_message()

        if not message:
            continue

        event = protocol.parse(message)

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
        from models import ModeChangeEvent

        #
        # Display events
        #
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