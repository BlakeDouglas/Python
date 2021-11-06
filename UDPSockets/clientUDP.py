from socket import *
import time
from datetime import datetime
import sys

serverName = ''
serverPort = 12001

# Connect to server
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

# Helper variable declaration
i = 0
flag = 0
maxRTT = 0
minRTT = 10
avgRTT = 0
packetRetrans = 0
packetLoss = 0

# Loop until we've sent the 10th ping
while i < 10:

    # Only transmit 3 times. If fail, we lose the packet
    if flag > 2:
        flag = 0
        i += 1
        packetLoss += 1

    start = time.time()
    # Set the message to be sent
    message = "Ping " + str(i+1) + " " + str(datetime.now())

    # if we are retransmitting, print with a tab
    if flag > 0:
        packetRetrans += 1.0
        print("\t" + message)
    else:
        print(message)

    try:
        # Send the message
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # Receive message from server
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

        # Check if server replied in less than a second
        end = time.time()

        # Print server message
        print("\tserver resp: " + modifiedMessage.decode())
        i += 1

        # Calculate all RTTs
        total = (end - start)
        print("\tCalculated Round Trip Time = %g seconds\n" % total)
        maxRTT = max(maxRTT, total)
        minRTT = min(minRTT, total)
        avgRTT += total
        flag = 0

    except:
            # If we timed out
            flag += 1
            print("\tRequest timed out")
            print("\tPacket retransmitted")

# Print all RTTs
print("Maximum RTT = " + str(maxRTT))
print("Minimum RTT = " + str(minRTT))
print("Average RTT = " + str((avgRTT / 10)))
print("Packet Loss Percentage = %.1f" % ((packetLoss / packetRetrans) * 100))
print("Packet retransmitted = " + str(packetRetrans))
clientSocket.close()
