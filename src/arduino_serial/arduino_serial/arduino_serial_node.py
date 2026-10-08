#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial


class ArduinoSerialNode(Node):

    def __init__(self):
        super().__init__('arduino_serial_node')

        self.serial_port = '/dev/ttyUSB0'
        self.baud_rate = 9600

        try:
            self.arduino = serial.Serial(
                self.serial_port,
                self.baud_rate,
                timeout=1
            )

            self.get_logger().info(
                f'Connected to Arduino on {self.serial_port}'
            )

        except serial.SerialException as e:
            self.get_logger().error(
                f'Failed to connect to Arduino: {e}'
            )
            self.arduino = None

    def send_command(self, command):

        if self.arduino is not None:
            self.arduino.write(command.encode())

            self.get_logger().info(
                f'Sent command: {command}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = ArduinoSerialNode()

    try:
        while rclpy.ok():

            command = input(
                'Enter command (1 = ON, 0 = OFF, q = quit): '
            )

            if command == '1':
                node.send_command('1')

            elif command == '0':
                node.send_command('0')

            elif command == 'q':
                break

            else:
                print('Invalid command. Use 1, 0, or q.')

    except KeyboardInterrupt:
        pass

    finally:

        if node.arduino is not None:
            node.arduino.close()

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()