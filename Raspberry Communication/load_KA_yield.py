import joblib
import socket
import numpy as np

# Load the new model
model_file = ''
model = joblib.load(model_file)
preprocessor_file = ''
preprocessor = joblib.load(preprocessor_file)

def predict(input_data):
    features = np.array([input_data])
    transform_features = preprocessor.transform(features)
    prediction = model.predict(transform_features).reshape(1,-1)
    return prediction[0][0]
    '''# Process input data to convert only numeric strings to floats
    processed_data = []
    for item in input_data:
        try:
            processed_data.append(float(item))  # Convert numeric strings to floats
        except ValueError:
            processed_data.append(i tem)  # Keep non-numeric strings as is

    prediction = model.predict([processed_data])
    return prediction[0]'''

# Set up the server socket to receive input from the laptop
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))  # Bind to any IP address and port 65432
server_socket.listen(1)  # Listen for incoming connections

# Set up the UDP socket to send data to ESP32
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
esp32_ip = ''  # Replace with your ESP32's IP address
esp32_port = 12345

print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)  # Receive data from the laptop
    if not data:
        break
    input_data = data.decode().split(',')  # Convert input to a list of strings
    result = predict(input_data)
    conn.sendall(str(result).encode())  # Send the result back to the laptop

    # Send the result to ESP32
    udp_socket.sendto(str(result).encode(), (esp32_ip, esp32_port))

conn.close()
server_socket.close()
udp_socket.close()
