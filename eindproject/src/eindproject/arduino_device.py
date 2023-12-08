# import pyvisa


from eindproject.nsp2visasim import sim_pyvisa as pyvisa

class ArduinoVISADevice:
    """Class were data will be measured from an active port.

    Returns:
        methods: containing
    """

    def __init__(self, port):
        """Open communication with a certain port.

        Args:
            port (string): The port where the program has to communicate with
        """
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

    def get_identification(self):
        """Gives IDN of device.

        Returns:
            string: Device Name
        """
        return self.device.query("*IDN?")

    # def set_output_value(self, value):
    #     """Set output voltage of device on channel 0

    #     Args:
    #         value (int): Voltage value channel 0 of the device will output

    #     Returns:
    #         int: the output Voltage channel 0 is set to
    #     """
    #     output_value = int(self.device.query(f"OUT:CH0 {value * (1023 / 3.3)}"))
    #     return output_value


    def set_output_value(self, value):
        """Set output voltage of device on channel 0

        Args:
            value (int): Voltage value channel 0 of the device will output

        Returns:
            int: the output Voltage channel 0 is set to
        """
        output_value = self.device.query(f"OUT:CH0 {value}")
        return output_value

    def get_output_value(self):
        """Gives previously set output value

        Returns:
            int: previously set output value
        """

        CH0_value = int(self.device.query(f"MEAS:CH0"))
        return CH0_value

    def get_input_value(self, channel):
        """Gets input bitvalue on a certain channel of the device

        Args:
            channel (int): the channel on the device where the input value will be measured

        Returns:
            int: bitvalue going over the channel
        """
        input_value = int(self.device.query(f"MEAS:CH{channel}?"))
        return input_value

    def get_input_voltage(self, channel):
        """Gets input voltage value on a certain channel of the device.

        Args:
            channel (int): the channel on the device where the input value will be measured.

        Returns:
            int: voltage value going over the channel.
        """
        input_voltage = int(self.device.query(f"MEAS:CH{channel}?")) * (3.3 / 1023)
        return input_voltage


def list_devices():
    """Generate list of active devices.

    Returns:
        list: list of active devices.
    """
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    print(ports)

    return ports

list_devices()
