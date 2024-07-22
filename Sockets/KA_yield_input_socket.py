import socket

raspberry_pi_ip = ''  # Replace with your Raspberry Pi's IP address
port = 65432

# Define the input data as strings
#input_data = ['Karnataka','Chikballapur','2022','Cowpea','Kharif','0.7','25.03']  # Replace with your actual input values, including any necessary strings
input_data = []

# List of prompts for the user
prompts = [
    "ENTER YOUR STATE NAME [AVAILABLE STATES = Karnataka ] : ", 
    "ENTER YOUR DISTRICT NAME [AVAILABLE DISTRICTS = Bagalkot, Chikmagalur, Chitradurga, Dakshin kannad, Davangere, Dharwad, Gadag, Gulbarga, Hassan, Haveri, Kodagu, Bangalore rural, Kolar, Koppal, Mandya, Mysore, Raichur, Ramanagara, Shimoga, Tumkur, Udupi, Uttar kannad, Belgaum, Vijayanagar, Yadgir, Bellary, Bengaluru urban, Bidar, Bijapur, Chamarajanagar, Chikballapur]: ",
    "ENTER THE CURRENT YEAR : ", 
    "ENTER CROP NAME = [ AVAILABLE CROPS = Arhar_Tur, Bajra, Castor_seed, Cotton, Cowpea, Dry_chillies, Groundnut, Horse_Gram, Jowar, Maize, Onion, Potato, Ragi, Rice, Sesmum, Soyabean, Sunflower, Urad] :",
    "ENTER THE SEASON [AVAILABLE SEASONS = Kharif, Rabi] : ", 
    "ENTER SOIL MOISTURE MEASURED IN % : ",
    "ENTER SOIL TEMPERATURE MEASURED IN °C : "
]

# Collect input from the user
for prompt in prompts:
    user_input = input(prompt)
    input_data.append(user_input)
    
# Create a socket and connect to the Raspberry Pi
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((raspberry_pi_ip, port))

# Send input data to the Raspberry Pi
input_str = ','.join(input_data)
client_socket.sendall(input_str.encode())

# Receive the result from the Raspberry Pi
result = client_socket.recv(1024)
print(f"Yield predcited: {result.decode()}")

client_socket.close()