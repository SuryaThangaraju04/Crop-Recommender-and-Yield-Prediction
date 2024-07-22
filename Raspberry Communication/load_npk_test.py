import joblib
import socket

model_file = ''
model = joblib.load(model_file)

def predict(input_data):
    prediction = model.predict([input_data])
    return prediction[0]

# Set up the server socket to receive input from the laptop
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))  # Bind to any IP address and port 65432
server_socket.listen(1)  # Listen for incoming connections

# Set up the UDP socket to send data to ESP32
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
esp32_ip = ''  # Replace with your ESP32's IP address
esp32_port = 12345

print("GETTING INPUT VALUES TO TRAIN....WAIT PLEASE!")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)  # Receive data from the laptop
    if not data:
        break
    input_data = list(map(float, data.decode().split(',')))  # Convert input to a list of floats
    result = predict(input_data)
    conn.sendall(str(result).encode())  # Send the result back to the laptop

    # Send the result to ESP32
    udp_socket.sendto(str(result).encode(), (esp32_ip, esp32_port))

conn.close()
server_socket.close()
udp_socket.close()

