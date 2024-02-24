import getopt, sys, socket

argumentList = sys.argv[1:]
options = "s:p:l:"
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

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# check for errors

serverAddr = (ipAddr, port)

# check for errors

message = input('Please enter your message:  ')

client_socket.connect(serverAddr)

client_socket.sendall(message.encode('utf-8'))

recieved = client_socket.recv(1024)

print(recieved.decode('utf-8'))

# log the returned message

client_socket.close()