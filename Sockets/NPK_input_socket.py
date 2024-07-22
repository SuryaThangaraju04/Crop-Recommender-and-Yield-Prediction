import socket

raspberry_pi_ip = ''  # Replace with your Raspberry Pi's IP address
port = 65432

# Define the input data
#input_data = [90,42,43,20.87974371,82.00274423,6.502985292]   #Replace with your actual input values
input_data = []
prompts = [
    ("Enter Nitrogen content of soil N : ", int), 
    ("Enter Phosphorous content of soil P : ", int), 
    ("Enter Potassium content of soil K : ", int), 
    ("Enter Soil Temperature of soil in °C : ", float),
    ("Enter Soil Moisture/Humidity in % : ", float), 
    ("Enter Soil pH : ", float)
]

# Collect input from the user and convert to appropriate types
for prompt, data_type in prompts:
    while True:
        try:
            user_input = data_type(input(prompt))
            input_data.append(user_input)
            break
        except ValueError:
            print(f"Please enter a valid {data_type.__name__}.")

# Create a socket and connect to the Raspberry Pi
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((raspberry_pi_ip, port))

# Send input data to the Raspberry Pi
input_str = ','.join(map(str, input_data))
client_socket.sendall(input_str.encode())

# Receive the result from the Raspberry Pi
result = client_socket.recv(1024)
print(f"Prediction: {result.decode()}")

client_socket.close()
