"""
Comfort serial communications.
"""

import serial


class ComfortConnection:

    def login(
        self,
        user_code="1234"
    ):

        login_command = (
            "\x03"
            + "LI"
            + user_code
            + "\r"
        )

        self.serial.write(
            login_command.encode()
        )

        print(
            f"TX -> LI{user_code}"
        )


    def send_command(self, command):

        command_bytes = (
            command + "\r"
        ).encode()

        self.serial.write(command_bytes)

        print(
            f"TX -> {command} "
            f"({command_bytes.hex(' ').upper()})"
        )
        print(
            f"TX -> {command}"
        )

    def __init__(
        self,
        port="/dev/serial0",
        baudrate=38400,
        timeout=1
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def connect(self):

        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )

        print(f"Connected to {self.port}")

    def read_message(self):

        buffer = bytearray()

        while True:

            data = self.serial.read(1)

            if not data:
                continue

            if data == b"\r":

                try:

                    text = buffer.decode(
                        "ascii",
                        errors="ignore"
                    )

                    text = text.replace("\x03", "")
                    text = text.strip()

                    if text:
                        return text

                finally:
                    buffer.clear()

            else:
                buffer.extend(data)