import getopt, sys, socket, struct

# print_cmd function that prints to the screen and to SERVERLOG.txt
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
    packet = packet.encode('utf-8')
    return packet

# unpack function that unpacks the big-endian packet
def unpack_data(packet):
    packet = packet.decode('utf-8')
    # Unpack the integers
    version, type, message_length = struct.unpack("! 3i", packet[:12]) 
    # Decode the remaining bytes to get the string
    message = packet[12:].decode('utf-8')
    print_cmd(logFile, "Recieved Data: version: {0} type: {1} length: {2}".format(version, type, message_length))
    return version, type, message_length, message

# define variables and options list
options = "p:l:"
argumentList = sys.argv[1:]
port = 0
logFile = ''

# get options from the run command
try:
    arguments, values = getopt.getopt(argumentList, options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-p"):
            port = int(currentValue)
        elif currentArgument in ("-l"):
            logFile = currentValue
except getopt.error as err:
    print_cmd(logFile, str(err))
    sys.exit(1)

try:
    # create a socket
    server_socket = socket.socket()
    # bind the socket and listen
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print_cmd(logFile, "Listening on port {0}".format(port))

    while(1):
        # accept new connection
        conn, address = server_socket.accept()

        # recieve and decode message
        recieved = conn.recv(1024)
        recVersion, recType, recLength, recMessage = unpack_data(recieved)
        print_cmd(logFile, "Recieved connection from {0}".format(address))

        # check if the message is "HELLO"
        if recVersion == 17 and 'HELLO' == recMessage:
            packet = pack_data(17, 1, "HELLO")
            conn.send(packet)
            # log the returned message
            print_cmd(logFile, "Returned to client:  {0}".format(recMessage))

            # recieve and decode command
            recieved = conn.recv(1024)
            recVersion, recType, recLength, recMessage = unpack_data(recieved)
            if recVersion == 17:
                print_cmd(logFile, "VERSION ACCEPTED")
                if recType == 1:
                    print_cmd(logFile, "EXECUTING SUPPORTED COMMAND: LIGHTON")
                    res = "SUCCESS"

                elif recType == 2:
                    print_cmd(logFile, "EXECUTING SUPPORTED COMMAND: LIGHTOFF")
                    res = "SUCCESS"
                    
                else:
                    print_cmd(logFile, "IGNORING UNKNOWN COMMAND: {0}".format(recType))
                    res = "UNKNOWN COMMAND"

                packet = pack_data(17, 1, res)
                conn.send(packet)
                print_cmd(logFile, "Returned to client:  {0}".format(res))
                conn.close()
                continue

            else:
                res = "VERSION MISMATCH"
                conn.send(res.encode('utf-8'))
                # Log the invalid message
                print_cmd(logFile, "Returned to client:  {0}".format(res))
                conn.close()
                continue
                

        else:
            res = "Invalid key word"
            conn.send(res.encode('utf-8'))
            # Log the invalid message
            print_cmd(logFile, "Returned to client:  {0}".format(res))
            conn.close()
            continue

        

except socket.error as err:
    print_cmd(logFile, str(err))
    sys.exit(1)