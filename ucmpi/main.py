from comfort import ComfortConnection
from protocol import ComfortProtocol


def main():

    comfort = ComfortConnection()
    protocol = ComfortProtocol()

    comfort.connect()

    print("Waiting for Comfort messages...\n")

    while True:

        message = comfort.read_message()

        if not message:
            continue

        print(f"RAW -> {message}")

        event = protocol.parse(message)

        if event is not None:
            print(event)


if __name__ == "__main__":
    main()