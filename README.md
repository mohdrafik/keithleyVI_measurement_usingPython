
# Keithley 6487 Current Measurement Program

 Overview

This Python program is developed to measure current while applying voltage from the Keithley 6487 module to equivalent 1 Mega-ohm devices. It allows you to plot live graphs for the applied voltage and measured current with respect to time, save the measurement data to a file, and export the final graphs as PNG images.

 Features

- Voltage and Current Measurement: The program configures the Keithley 6487 module to measure the current while applying voltage to the connected devices.

- Live Graphs: It displays live graphs showing the applied voltage and measured current with respect to time using the Matplotlib library.

- Data Logging: The program logs the measurement data, including timestamps, applied voltage, and current readings, to a text file for later analysis.

- PNG Export: After the measurement, the program saves the final graphs as PNG images for documentation and reporting.

 Usage

1. Setup Your Environment:
   - Make sure you have Python installed on your system.
   - Install the required Python libraries using `pip install pyvisa-py numpy matplotlib`.

2. Connect Your Keithley 6487:
   - Connect the Keithley 6487 module to your computer using a suitable USB to GPIB adapter cable.
   - Ensure that your Keithley 6487 is properly configured for the measurements.

3. Run the Program:
   - Run the provided Python script, which will initialize the Keithley, apply voltage, measure current, and display live graphs.

4. Data Storage:
   - The measurement data is logged to a text file named `measurement_data.txt` in the same directory as the script.

5. Graph Export:
   - After the measurement, the final graphs are saved as PNG images with timestamps in their filenames.

6. Customization:
   - You can customize the script to adjust the voltage range, current range, integration time, or other measurement parameters according to your specific setup.

 Example

```python
# Run the Python script with the Keithley 6487 connected and configured.
vi_timekeithley.py
```

 Dependencies

- PyVISA-py
- Numpy
- Matplotlib

 License

This program is provided under the MIT License. Feel free to use, modify, and distribute it.

 Author

Moh Rafik

 Contact:

If you have any questions or need assistance, you can contact me at [rafikiitbhu@gmail.com].
