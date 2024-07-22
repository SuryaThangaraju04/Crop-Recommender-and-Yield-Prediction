import socket

raspberry_pi_ip = ''  # Replace with your Raspberry Pi's IP address
port = 65432

# Define the input data as strings
input_data = []

# List of prompts for the user
prompts = [
    "ENTER CURRENT YEAR : ", 
    "ENTER SOIL TEMPERATURE MEASURED IN °C : ", 
    "ENTER SOIL MOISTURE MEASURED IN % : ", 
    "ENTER YOUR DISTRICT NAME = [ AVAILABLE DISTRICTS = Ariyalur, Coimbatore, Krishnagiri, Madurai, Thirunelveli, Cuddalore,Dharmapuri, Dindigul, Erode, Kanchipuram, Kanniyakumari, Karur,Nagapattinam, Namakkal, Perambalur, Pudukkottai, Ramanathapuram, Salem,Sivaganga, Thanjavur, The nilgiris, Theni, Thiruvallur, Thiruvarur,Thoothukudi, Tiruchirappalli, Tiruppur, Tiruvannamalai, Vellore, Villupuram, Virudhunagar, Adilabad, Bhadradri, Nagarkurnool, Sangareddy, Siddipet,Jagitial, Jangoan, Jayashankar, Jogulamba, Kamareddy, Karimnagar,Khammam, Komaram bheem asifabad, Mahabubabad, Mahbubnagar, Mancherial, Medak,Medchal, Nalgonda, Nirmal, Nizamabad, Peddapalli, Rajanna,Rangareddi, Suryapet, Vikarabad, Wanaparthy, Warangal, Warangal urban,Yadadri, Anantapur, Chittoor, Guntur, Vishakapatanam, WestGodavari,East godavari, Kadapa, Krishna, Kurnool, Prakasam, Spsr nellore,Srikakulam, Vizianagaram, BengaluruUrban, Hassan, Kolar, Mysore,Udupi, Bagalkot, Bangalore rural, Belgaum, Bellary, Bidar,Bijapur, Chamarajanagar, Chikballapur, Chikmagalur, Chitradurga, Davangere,Dharwad, Gadag, Gulbarga, Haveri, Kodagu, Koppal, Mandya, Raichur, Ramanagara, Shimoga, Tumkur, Uttar kannad,Yadgir, Ahmednagar, Akola, Amravati, Aurangabad, Beed,Bhandara, Buldhana, Chandrapur, Dhule, Gadchiroli, Gondia,Hingoli, Jalgaon, Jalna, Kolhapur, Latur, Nagpur,Nanded, Nandurbar, Nashik, Osmanabad, Palghar, Parbhani,Pune, Sangli, Satara, Sindhudurg, Solapur, Thane,Wardha, Washim, Yavatmal, Karaikal, Pondicherry, Yanam] : ",
    "ENTER CROP NAME [AVAILABLE CROPS = Cotton, Groundbut, Maize, Onion, Urad] : ", 
    "ENTER THE SEASON [AVAILABE SEASONS = Rabi, Kharif] : "
]

# Collect input from the user
for prompt in prompts:
    user_input = input(prompt)
    input_data.append(user_input)

# Create a socket and connect to the Raspberry Pi
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((raspberry_pi_ip, port))

# Convert all input data to strings for transmission
input_data = list(map(str, input_data))

# Send input data to the Raspberry Pi
input_str = ','.join(input_data)
client_socket.sendall(input_str.encode())

# Receive the result from the Raspberry Pi
result = client_socket.recv(1024)
print(f"Yield predicted: {result.decode()}")

client_socket.close()
