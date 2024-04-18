import getopt, sys, socket, struct

# print_cmd function that prints to the screen and to logfile
def print_cmd(file, message):
    file = open("{0}.txt".format(file), "a")
    file.write("{0}\n".format(message))
    file.close()
    print(message)
    return

# pack function that creates a big-endian packet
def pack_data(version, metype, message):
    # pack the struct and send user input to the server
    packet = struct.pack("! 3i", version, metype, len(message))
    packet+= message.encode('utf-8')
    return packet

# unpack function that unpacks the big-endian packet
def unpack_data(packet):
    # Unpack the integers
    version, type, message_length = struct.unpack("! 3i", packet[:12]) 
    # Decode the remaining bytes to get the string
    message = packet[12:].decode('utf-8')
    print_cmd(logFile, "Recieved Data: version: {0}".format(version, type, message_length))
    return version, type, message_length, message

# read in user inputs
argumentList = sys.argv[1:]
ipAddr = ''
port = ''
logFile = ''

# create options to check for specific arguments
options = "s:p:l:"

# store each of the inputs into variables and check for any errors
try:
    arguments, values = getopt.getopt(argumentList, options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s"):
            ipAddr = currentValue
        elif currentArgument in ("-p"):
            port = int(currentValue)
        elif currentArgument in ("-l"):
            logFile = currentValue

except getopt.error as err:
    print(str(err))
    sys.exit(1)

# create a socket and check for errors
try:
    client_socket = socket.socket()
    serverAddr = (ipAddr, port)
    # initialize connection
    client_socket.connect(serverAddr)
    # take in user login input from the command line
    message = input('Please enter your login message:  ')

    # construct the login packet
    packet = pack_data(17, 0, message)

    # send the packed data to the server
    client_socket.sendall(packet)
    client_socket.settimeout(5)
    recieved = client_socket.recv(1024)

    recVersion, recType, recLength, recMessage = unpack_data(recieved)

    # check if the server returned packet with version 17
    if recVersion == 17 and recMessage == "HELLO":
        # log the returned message
        print_cmd(logFile, "VERSION ACCEPTED")
        print_cmd("Recieved Message: {0}".format(recMessage))
        # take in user login input from the command line
        message = input('Please enter a command (LIGHTON/LIGHTOFF):  ')
        # construct the login packet based on command given
        if(message == 'LIGHTON'):
            packet = pack_data(17, 1, message)
        elif(message == 'LIGHTOFF'):
            packet = pack_data(17, 2, message)
        else:
            packet = pack_data(17, 3, message)

        client_socket.sendall(packet)
        client_socket.settimeout(5)
        recieved = client_socket.recv(1024)
        recVersion, recType, recLength, recMessage = unpack_data(recieved)

        if recVersion == 17:
            print_cmd(logFile, "VERSION ACCEPTED")
            print_cmd(logFile, "Recieved Message: {0}".format(recMessage))
            close = "DISCONNECT"
            client_socket.sendall(close.encode('utf-8'))
            print_cmd(logFile, "Closing connection")
            client_socket.close()

        else:
            print_cmd(logFile, "VERSION MISMATCH")
            client_socket.close()
            sys.exit(1)

    else:
        print_cmd(logFile, "VERSION MISMATCH")
        client_socket.close()
        sys.exit(1)
    

except socket.timeout:
    print("No server response.")
    sys.exit(1)

except socket.error as err:
    print(str(err))
    sys.exit(1)