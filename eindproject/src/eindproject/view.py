import matplotlib.pyplot as plt
import csv
from eindproject.sun_expirement import DiodeExperiment


def UI_graph(start=0, stop=1024, iterations=10):
    """
    Creates Voltage/Current plot.

    args:
        start (int): starting voltage bitvalue for the data.
        stop (int) : last voltage bitvalue in the data.
        iterations (int) : number of times the Current is measured at a certain voltage.

    return:
        graph: A Voltage/Current graph representing the data
        CSV_file : A CSV file containg the measured data

    """
    scan = DiodeExperiment('ASRL6::INSTR')
    # Values we can alter depending on the the start and stop voltage (bitvalue) and how many times we want to do the the expirement.

    # Here all the needed data from our experiment is collected.
    data = scan.scan(start, stop, iterations)
    current = data[1]
    voltage = data[2]
    yerr = data[3]
    xerr = data[4]

    # Here the plot is created
    plt.errorbar(voltage, current, yerr=yerr, xerr=xerr, fmt="r.")
    plt.ylabel("I (Ampere)")
    plt.xlabel("U (Volt)")
    plt.title("Current_Voltage Graph for LED")
    plt.show()

    # Here a CSV file representing the data is written.
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
        for volt, cur, y_err, x_err in zip(voltage, current, yerr, xerr):
            writer.writerow([volt, cur, y_err, x_err])


UI_graph()