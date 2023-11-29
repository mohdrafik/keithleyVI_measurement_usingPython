
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
from time import time,sleep

file_path = "measurement_data.txt"

# Initialize the Keithley instrument using PyVISA-py
# rm = pyvisa.ResourceManager()   # this is for LAN connected  instrument.
# keithley = rm.open_resource("TCPIP::192.168.1.100::inst0::INSTR")

rm = pyvisa.ResourceManager('@py')  # this '@py' stands for pyvisa-py library,light wight wrapper for the interface b/w software and hardware. 
# keithley = rm.open_resource('ASRL9::INSTR')  # Replace 'COM1' with the actual COM port where the USB to RS232 cable is connected

# these TWO are MUST FOR  for RS-232 INTERFACE
# TX TERMINATOR: Terminator (CR, LF, CRLF, or LFCR)
# • FLOW: Flow control (NONE or Xon/Xoff)


# keithley = rm.open_resource('ASRL3::INSTR', baud_rate=9600, data_bits=8,stop_bits=pyvisa.constants.StopBits.one, parity=pyvisa.constants.Parity.none, timeout=8000)
keithley = rm.open_resource('ASRL3::INSTR', baud_rate=9600, data_bits=8,
                            stop_bits=pyvisa.constants.StopBits.one, 
                            parity=pyvisa.constants.Parity.none,
                            flow_control=pyvisa.constants.VI_ASRL_FLOW_XON_XOFF,
                            timeout=100000)

keithley.write('*RST')
# keithley.read_termination = '\r' # # Set terminator for read operations to <CR>
keithley.write_termination = '\r'   # # Set terminator for write operations to <CR>


# rm = pyvisa.ResourceManager("@py")   # @py --> this is for GPIB connection.
# keithley = rm.open_resource('GPIB0::12::INSTR')  # can write our GPIB address at place of '12' ,
# '12' with the actual GPIB address of your Keithley 6487

# Configure the Keithley for current measurement
# here source is set, which is voltage(input).
keithley.write(":SOUR:FUNC VOLT")
keithley.write(":SENS:FUNC 'CURR:DC' ")  # Measure current
# .write(): This is a method/function associated with the keithley object. It's used to send a command to the Keithley instrument.
# So, this line of code tells the Keithley instrument
# keithley.write(":SENS:CURR:RANG 13E-9 ")  # disable autoranging
keithley.write(":SENS:CURR:RANG:AUTO ON")
# to configure its current measurement settings so that it can measure currents as low as 1 µA

# [CURRent]:RANGe:AUTO:LLIMit
# Set integration time NPLC stands for "Number of Power Line Cycles," which is a measure of integration time. It's a common parameter in instruments like Keithley. 10 is the value that sets the integration time to 10 PLC.
# keithley.write(":SENS:CURR:NPLC 5")

keithley.write(":OUTP ON")

# Create empty lists to store data
time_values = []
voltage_values = []
current_values = []

# Set up live graph plotting
plt.ion()  # Turn on interactive mode
fig1, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig1.suptitle('Live Voltage and Current Measurements')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Voltage (V)')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Current (A)')

# Set up live graph plotting for Current vs Voltage
fig2, (ax3) = plt.subplots(1, 1, sharex=True)
fig2.suptitle('Live Current vs Voltage')

ax3.set_xlabel('Voltage (V)')
ax3.set_ylabel('Current (uA)')
# -------- this is for the voltage range --------
v_start = 1E-3
v_end = 11E-3
v_step = 1E-3
n =int(((v_end-v_start)/(v_step)) + 1)
# print(n)
volatge_list = [] 
for i in range(1,n+1,1):
    term  = v_start + (i-1)*v_step 
    # print(term)
    volatge_list.append(term)
# ------ volatge range --> volatge_list is created for applying the volatge.



with open(file_path, 'w') as file:

    file.write("Time (s),Voltage (V),Current (UA)\n")

    start_time = time.time()

    # for voltage_step in range(v_start, v_end+1, v_step):
    for voltage_step in volatge_list:
        keithley.write(f":SOUR:VOLT {voltage_step}")
        time.sleep(2)

        # Turn on the output:  This is the command being sent to the instrument. It tells the instrument to turn its output on. When the output is turned on, the instrument will generate or provide the specified output, which in this context is current.
        # keithley.write(":OUTP ON")
        # time.sleep(1) # Wait for 1 seconds

        # current_reading = (keithley.query(":MEAS?")) # reading the current value, here float  is used for typecast the string to float because the keithley.query(":MEAS?") --> returns the measured value.
        # current_reading = float(current_reading.split(',')[0][4:-1])

        # voltage_reading = float(keithley.query(":READ?"))  # --> can read voltage also.
        # keithley.write(":OUTP OFF")  # Turn off the output, it's good practice.

        # current_reading = (keithley.query(":MEAS?")) # reading the current value, here float  is used for typecast the string to float because the keithley.query(":MEAS?") --> returns the measured value.
        # current_reading = float(current_reading.split(',')[0][4:-1])
        keithley.write(':READ?')
        current_reading = keithley.read()
        # time.sleep(1)
        print("before striping:",current_reading)
        current_reading = float(current_reading.split(',')[0].rstrip('A'))
        print("After striping:ACTUAL READING OF CURRENT --> ",current_reading)

        # keithley.write(":OUTP OFF")  # Turn off the output

        timestamp = time.time() - start_time

        # Append data to lists
        time_values.append(timestamp)
        voltage_valuesROUND = round(voltage_step,3)
        voltage_values.append(voltage_valuesROUND)
        
        # voltage_values.append(voltage_reading)
        current_values.append(current_reading)

        # Write data to the file
        file.write(f"{timestamp }, { voltage_step},{ current_reading}\n")

        # Update live graph
        ax1.plot(time_values, voltage_values, 'b-')
        ax2.plot(time_values, current_values, 'g-')

        # Update live graph for Current vs Voltage
        ax3.plot(voltage_values, current_values, 'r-')
        ax3.set_xlim(voltage_values[0], voltage_values[-1])
        ax3.set_ylim(min(current_values), max(current_values))

        fig1.canvas.flush_events()
        fig2.canvas.flush_events()

keithley.close()  # Close the Keithley instrument

# Save the final plot as a PNG image
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
plt.savefig(f"live_measurement_plot_{timestamp}.png")

# Clean up and display the final plot
plt.ioff()
plt.show()
# plt.close()
