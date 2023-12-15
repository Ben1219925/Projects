import serial
import matplotlib.pyplot as plt
import numpy as np
import time

# Configuration
port = "COM5"  # Change this to the correct COM port
baud_rate = 57600
data_size = 1 # Number of seconds of data to collect

# ADC parameters
adc_resolution = 12  # Bits
reference_voltage = 3.3  # Volts

# Open the serial port
ser = serial.Serial(port, baud_rate, timeout=1)

# Function to process the received byte
def process_byte(byte):
    # Extract data bits from the received byte and remove the two most significant bits
    print(byte)
    data = int.from_bytes(byte, byteorder='big') & 0b00111111
    return data

# Function to collect data and plot
def collect_and_plot_data():
    # Initialize data buffer
    received_data = []

    # Record start time
    start_time = time.time()

    while (time.time() - start_time) < 1:
        # Read two bytes from the serial port (two packets)
        byte1 = ser.read(size=1)
        byte2 = ser.read(size=1)

        if byte1 and byte2:
            # Process each byte and combine them into a 12-bit sample
            data1 = process_byte(byte1)
            data2 = process_byte(byte2)
            combined_data = (data1 << 6) | data2
            
            # Interpret the 12-bit sample as voltage
            voltage = (combined_data / (2**adc_resolution - 1)) * reference_voltage
            
            # Append the voltage to the buffer
            received_data.append(voltage)

    # Generate time values covering the specified duration
    time_values = np.linspace(0, data_size * 1000, len(received_data))

    # Plot the received data with y-axis limits set to 0 to reference_voltage
    plt.plot(time_values, received_data, '.')
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (V)')
    plt.title('Voltage Data from COM5')
    plt.ylim(0, reference_voltage)  # Set y-axis limits
    plt.show()

# Read and plot data
try:
    collect_and_plot_data()

    # Command input loop
    while True:
        command = input("Enter command (or 'exit' to quit): ")
        if command.lower() == 'exit':
            break
        # Send the command to the serial port
        ser.write(command.encode())
        
        # Collect and plot data after entering a new command
        collect_and_plot_data()

finally:
    # Close the serial port
    ser.close()

# import serial
# import matplotlib.pyplot as plt
# import numpy as np
# import time

# # Configuration
# port = "COM5"  # Change this to the correct COM port
# baud_rate = 115200
# data_size = 1  # Number of seconds of data to collect

# # ADC parameters
# adc_resolution = 12  # Bits
# reference_voltage = 3.3  # Volts

# # Open the serial port
# ser = serial.Serial(port, baud_rate, timeout=1)

# # Function to process the received byte
# def process_byte(byte):
#     # Extract data bits from the received byte and remove the two most significant bits
#     data = int.from_bytes(byte, byteorder='big') & 0b00111111
#     return ((data << 6) | 000000000000)

# # Function to collect data and plot
# def collect_and_plot_data():
#     # Initialize data buffer
#     received_data = []

#     # Record start time
#     start_time = time.time()

#     while (time.time() - start_time) < data_size:
#         # Read one byte from the serial port
#         byte = ser.read(size=1)

#         if byte:
#             data = process_byte(byte)

#             # Interpret the sample as voltage
#             voltage = (data / (2**adc_resolution - 1)) * reference_voltage

#             # Append the voltage to the buffer
#             received_data.append(voltage)

#     # Generate time values covering the specified duration
#     time_values = np.linspace(0, data_size * 1000, len(received_data))

#     # Plot the received data with y-axis limits set to 0 to reference_voltage
#     plt.plot(time_values, received_data)
#     plt.xlabel('Time (ms)')
#     plt.ylabel('Voltage (V)')
#     plt.title('Voltage Data from COM5')
#     plt.ylim(0, reference_voltage)  # Set y-axis limits
#     plt.show()

# # Read and plot data
# try:
#     collect_and_plot_data()

#     # Command input loop
#     while True:
#         command = input("Enter command (or 'exit' to quit): ")
#         if command.lower() == 'exit':
#             break
#         # Send the command to the serial port
#         ser.write(command.encode())
        
#         # Collect and plot data after entering a new command
#         collect_and_plot_data()

# finally:
#     # Close the serial port
#     ser.close()

