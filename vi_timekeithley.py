
"""
program is developed for measures the currents while applying volatge from the keithley 6487 module to equiavalent 1Mohm devices.
plot the live graph for the  Applied volatge and measured current w.r.to the time, save the data and graph in png after measurement.
@Writer --> Moh Rafik    

"""
import pyvisa   # pip install pyvisa-py
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

file_path = "measurement_data.txt"

# Initialize the Keithley instrument using PyVISA-py

# rm = pyvisa.ResourceManager()   # this is for LAN connected  instrument.
# keithley = rm.open_resource("TCPIP::192.168.1.100::inst0::INSTR")

# rm = pyvisa.ResourceManager()
# keithley = rm.open_resource('ASRL::COM1::INSTR')  # Replace 'COM1' with the actual COM port where the USB to RS232 cable is connected

rm = pyvisa.ResourceManager("@py")   # @py --> this is for GPIB connection.
keithley = rm.open_resource('GPIB0::12::INSTR')  # can write our GPIB address at place of '12' , 
# '12' with the actual GPIB address of your Keithley 6487

# Create a list of voltages to step through
voltage_steps = np.arange(0, 22, 2)  # From 0V to 20V in 2V steps  
# like this : array([ 0,  2,  4,  6,  8, 10, 12, 14, 16, 18, 20])


# Configure the Keithley for current measurement
keithley.write(":SOUR:FUNC VOLT")   # here source is set, which is voltage(input).
keithley.write(":SENS:FUNC 'CURR'")  # Measure current
# .write(): This is a method/function associated with the keithley object. It's used to send a command to the Keithley instrument.
keithley.write(":SENS:CURR:RANG 1e-6")  # So, this line of code tells the Keithley instrument
# to configure its current measurement settings so that it can measure currents as low as 1 µA
keithley.write(":SENS:CURR:NPLC 10")  # Set integration time NPLC stands for "Number of Power Line Cycles," which is a measure of integration time. It's a common parameter in instruments like Keithley. 10 is the value that sets the integration time to 10 PLC.


# Create empty lists to store data
time_values = []
voltage_values = []
current_values = []

# Set up live graph plotting
plt.ion()  # Turn on interactive mode
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig.suptitle('Live Voltage and Current Measurements')

ax1.set_ylabel('Voltage (V)')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Current (A)')

# Open the file for writing
with open(file_path, 'w') as file:
    # Write a header to the file
    file.write("Time (s),Voltage (V),Current (A)\n")

    start_time = time.time()
    for voltage_step in voltage_steps:
        keithley.write(f":SOUR:VOLT {voltage_step}")
        time.sleep(50)  # Wait for 50 seconds to stabilize the voltage, can change 50 second to other value of your choice also. 


    # for _ in range(10):  # Perform 10 measurements at the current voltage
    keithley.write(":OUTP ON")  # Turn on the output:  This is the command being sent to the instrument. It tells the instrument to turn its output on. When the output is turned on, the instrument will generate or provide the specified output, which in this context is current.
    
    # voltage_reading = float(keithley.query(":READ?"))  # --> can read voltage also.
    # keithley.write(":OUTP OFF")  # Turn off the output, it's good practice.

    current_reading = float(keithley.query(":MEAS?")) # reading the current value, here float  is used for typecast the string to float because the keithley.query(":MEAS?") --> returns the measured value.
    keithley.write(":OUTP OFF")  # Turn off the output

    timestamp = time.time() - start_time

    # Append data to lists
    time_values.append(timestamp)
    voltage_values.append(voltage_step)
    # voltage_values.append(voltage_reading)
    current_values.append(current_reading)

    # Write data to the file
    file.write(f"{timestamp},{voltage_step},{current_reading}\n")

    # Update live graph
    ax1.plot(time_values, voltage_values, 'b-')
    ax2.plot(time_values, current_values, 'g-')
    fig.canvas.flush_events()

keithley.close()  # Close the Keithley instrument

# Save the final plot as a PNG image
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
plt.savefig(f"live_measurement_plot_{timestamp}.png")

# Clean up and display the final plot
plt.ioff()
plt.show()
