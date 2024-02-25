import getopt, sys, socket

# read in user inputs
argumentList = sys.argv[1:]

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

# create a socket and check for errors
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddr = (ipAddr, port)
# initialize connection
    client_socket.connect(serverAddr)
# take in user input from the command line
    message = input('Please enter your message:  ')
# send user input to the server
    client_socket.sendall(message.encode('utf-8'))
    client_socket.settimeout(5)
    recieved = client_socket.recv(1024)

    if recieved:
        recieved = (recieved.decode('utf-8'))
# log the returned message
        file = open("{0}.txt".format(logFile), "a")
        file.write("{0}\n".format(recieved))
        file.close()

    client_socket.close()

except socket.timeout:
    print("No server response")    

except socket.error as err:
    print(str(err))