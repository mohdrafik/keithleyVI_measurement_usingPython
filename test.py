# import pyvisa

# rm = pyvisa.ResourceManager()
# ke = rm.list_resources()

# # ke= rm.open_resource()
# print(ke)
import serial

# Open a serial connection
ser = serial.Serial('COM3', baudrate=9600, timeout=1)

# Send a command
ser.write(b'Hello, world!')

# Read the response
response = ser.readline()
print(response)

# Close the serial connection
ser.close()