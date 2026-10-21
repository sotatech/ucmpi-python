from comfort import ComfortConnection
from protocol import ComfortProtocol
from mqtt import MQTTPublisher

from models import ZoneEvent


def main():

    comfort = ComfortConnection()
    protocol = ComfortProtocol()
    mqtt = MQTTPublisher()

    comfort.connect()

    print("Waiting for Comfort messages...\n")

    while True:

        message = comfort.read_message()

        if not message:
            continue

        event = protocol.parse(message)

        if event:

            print(event)

            if isinstance(event, ZoneEvent):

                mqtt.publish_zone(
                    event.zone,
                    event.state
                )

        else:

            print(
                f"Unhandled message: "
                f"{message}"
            )


if __name__ == "__main__":
    main()