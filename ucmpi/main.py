from comfort import ComfortConnection
from protocol import ComfortProtocol
from state import SystemState


def main():

    comfort = ComfortConnection()
    protocol = ComfortProtocol()
    state = SystemState()

    comfort.connect()

    print("Waiting for Comfort messages...\n")

    while True:

        message = comfort.read_message()

        if not message:
            continue

        event = protocol.parse(message)

        if event:

            print(event)

            state.update(event)

            state.dump()

        else:

            print(
                f"Unhandled message: "
                f"{message}"
            )


if __name__ == "__main__":
    main()
