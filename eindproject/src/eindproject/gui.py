import sys
from PySide6 import QtWidgets
import pyqtgraph as pg
from eindproject.ui_mainwindow import Ui_MainWindow
from eindproject.sun_expirement import DiodeExperiment, devices
import csv
import numpy as np

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    """Class with methods to create a GUI of the experiment with option to represent data in a graph or CSV file"""

    def __init__(self):
        """Method to show the GUI and connect the buttons in the GUI with the program."""
        super().__init__()

        self.scan = DiodeExperiment('ASRL6::INSTR')

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.plot_button.clicked.connect(self.plot_func)

        self.show()

    def port_change(self):
        """Method where the current device in the chosen in the GUI will be used in the model."""
        self.port = self.ui.list_devices.currentText()
        self.scan = DiodeExperiment('ASRL6::INSTR')

    def plot_func(self):
        """Data will be gathered from the model and represented in a graph."""
        self.ui.plot_graph.clear()

        data = self.scan.scan(
            self.ui.start_button.value(),
            self.ui.stop_button.value(),
            self.ui.iterations_button.value(),
        )

        _, self.current, self.voltage, self.yerr, self.xerr = data

        self.ui.plot_graph.plot(
            self.voltage, self.current, symbol="o", symbolsize=5, pen=None
        )
        error_bars = pg.ErrorBarItem(
            x=self.voltage, y=self.current, width=2 * self.xerr, height=2 * self.yerr
        )
        self.ui.plot_graph.addItem(error_bars)
        self.ui.plot_graph.setLabel("left", "Current (ampere)")
        self.ui.plot_graph.setLabel("bottom", "Voltage (volt)")

    def CSV_file(self):
        """Data will be represented in a CSV file."""
        with open("Results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "Voltage_led (volt)",
                    "Current_led (ampere)",
                    "Error_voltage (volt)",
                    "Error_current (ampere)",
                ]
            )
            for volt, cur, y_err, x_err in zip(
                self.voltage, self.current, self.yerr, self.xerr
            ):
                writer.writerow([volt, cur, y_err, x_err])


def main():
    """Method to show the GUI."""
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()