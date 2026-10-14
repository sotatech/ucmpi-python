"""
Comfort serial communications.

Initial version for testing access to the Comfort RS485 interface
through the Raspberry Pi UART.

Author: Pat Rooney
"""

from datetime import datetime
import serial


class ComfortConnection:
    """Handles connection to the Comfort serial interface."""

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
        """Open the serial port."""

        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout
        )

        print(f"Connected to {self.port}")

    def read_loop(self):
        """Read data from the serial port indefinitely."""

        print("Waiting for data...\n")

        while True:
            data = self.serial.read(self.serial.in_waiting or 1)

            if data:
                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                )[:-3]

                print(
                    f"{timestamp} RX: "
                    f"{data.hex(' ').upper()}"
                )