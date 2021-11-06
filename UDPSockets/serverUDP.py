from socket import *
import random

serverPort = 12001
# Create UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Bind to INADDR_ANY and set port
serverSocket.bind(('', serverPort))

i = 1

while True:

	# Receive client's message
	message, clientAddress = serverSocket.recvfrom(2048)
	# Make message all uppercase
	modifiedMessage = message.decode().upper()
	# Generate random number [0,9]
	randomNum = random.randint(0, 9)

	pingNumber = modifiedMessage[5]
	# Add a 0 if its the 10th ping
	if modifiedMessage[6].isnumeric():
		pingNumber += '0'

	# Print the connection even if it's a repeat
	print("connection from ('"+ str(clientAddress[0]) +
		"', "  + str(serverPort) + ") message " + pingNumber)
	# Enters approximately 30% of the time (0, 1, 2)
	if randomNum < 3:
		continue

	# Send message
	serverSocket.sendto(modifiedMessage.encode(), clientAddress)
