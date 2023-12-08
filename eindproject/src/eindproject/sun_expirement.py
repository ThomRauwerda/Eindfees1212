from eindproject.arduino_device import ArduinoVISADevice, list_devices
import statistics as stat
import numpy as np


class DiodeExperiment:
    """Class where the right data is calculated from the experiment.

    Returns:
        scan (method)
        Led_resistor_voltage (method)

    """

    def __init__(self, port):
        """Multiple lists where data can be put in are created."""
        self.device = ArduinoVISADevice(port=port)
        self.mean_Current_led = []
        self.mean_Voltage_led = []
        self.error_current_led = []
        self.error_voltage_led = []

    def identification(self):
        identification = self.device.get_identification()
        return identification

    def scan(self, start, stop, N):
        """A method where data will be gathered from a certain port and will be put in differents lists.

        Args:
            start (int): Starting bitvalue to perform scan over.
            stop (int): Last bitvalue to perform scan over.
            N (int): How many times the scan will be repeated for a more accurate result.

        Returns:
            self.mean_Current_led (list) : list containing average currents for every bitvalue input on CH0.
            self.mean_Voltage_led (list) : list containing average voltages for every bitvalue input on CH0.
            self.error_current_led (list) : list containing average voltage errors for every bitvalue input on CH0.
            self.error_voltage_led (list) : list containing average current errors for every bitvalue input on CH0.
            N (int) : number of times scan has been repeated.
        """

        start_bit = int(start * (1023/3.3))
        stop_bit = int(stop * (1023/3.3))


        # We run every bit value.
        for i in range(start_bit, stop_bit):
            self.Voltage_led = []
            self.currents_led = []

            # For every Voltage value between start and stop we gather N times the current and the voltage over the led.
            for r in range(N):
                self.device.set_output_value(i * (1023/3.3))
                self.Voltage_led.append(self.device.get_input_voltage(1) * 3)
                self.currents_led.append(self.device.get_input_voltage(2) / 4.7)


            # From the N times we iterate over every Voltage value we calculate the mean Current and voltage and the errors for these values.
            self.mean_Current_led.append(float(stat.mean(self.currents_led)))
            self.error_current_led.append(stat.stdev(self.currents_led) / (N**0.5))
            self.mean_Voltage_led.append(float(stat.mean(self.Voltage_led)))
            self.error_voltage_led.append(stat.stdev(self.Voltage_led) / (N**0.5))
            N = N

            if i == stop - 1:
                self.device.set_output_value(0)


        return (
            N,
            np.array(self.mean_Current_led),
            np.array(self.mean_Voltage_led),
            np.array(self.error_current_led),
            np.array(self.error_voltage_led),
        )

    def Led_resistor_voltage(self):
        """A method where for every bitvalue the the bitvalue and the voltage
        value on the led and over the resistor wil be measured and printed.
        """
        for i in range(1024):
            on_led_bit = self.device.set_output_value(i * (3.3 / 1023))
            on_led_volt = self.device.set_output_value(i *  (3.3 / 1023)) * (3.3 / 1023)

            over_resistor_bit = f"{self.device.get_input_value(2)}"
            over_resistor_volt = f"({round(self.device.get_input_voltage(2) , 3)} V)"

            output_line = f"On LED:  {on_led_bit} {on_led_volt}    Over resistor:   {over_resistor_bit}  {over_resistor_volt}"
            print(output_line)

            if i == 1024:
                self.device.set_output_value(0)


def devices():
    """Function where list of active devices will be given.

    returns:
        ports (list): list of all active ports.
    """

    return list_devices()