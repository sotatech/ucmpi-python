"""
Comfort serial communications.
"""

import serial


class ComfortConnection:

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