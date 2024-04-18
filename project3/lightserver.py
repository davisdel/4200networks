import getopt, sys, socket

# print_cmd function that prints to the screen and to SERVERLOG.txt
def print_cmd(file, message):
    file = open("{0}.txt".format(file), "a")
    file.write("{0}\n".format(message))
    file.close()
    print(message)
    return

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
        req = conn.recv(1024)
        req = req.decode('utf-8')
        print_cmd(logFile, "Recieved connection from {0}".format(address))
        print_cmd(logFile, "Recieved data: version:{0}, message_type:{1}, length:{3}".format(req.version, req.type, req.length))

        # check if the message is "HELLO"
        if 'HELLO' == req:
            res = "HELLO"
            conn.send(res.encode('utf-8'))
            # log the returned message
            print_cmd(logFile, "Returned to client:  {0}".format(res))

        else:
            res = "Invalid key word"
            conn.send(res.encode('utf-8'))
            # Log the invalid message
            print_cmd(logFile, "Returned to client:  {0}".format(res))
            conn.close()
            continue

        # recieve and decode header
        header = conn.recv(1024)
        header = header.decode('utf-8')
        print_cmd(logFile, "Recieved connection from {0}".format(address))
        if header.version != 17:
            print_cmd(logFile, "VERSION MISMATCH")
            conn.close()
            continue
        else:
            if header.type == 1:
                print_cmd(logFile, "EXECUTING SUPPORTED COMMAND: LIGHTON")
                res = "SUCCESS"
                conn.send(res.encode('utf-8'))
            else if header.type == 2:
                print_cmd(logFile, "EXECUTING SUPPORTED COMMAND: LIGHTOFF")
                res = "SUCCESS"
                conn.send(res.encode('utf-8'))
            else:
                print_cmd(logFile, "IGNORING UNKNOWN COMMAND: {0}".format(header.type))
                conn.close()
                continue

except socket.error as err:
    print_cmd(logFile, str(err))
    sys.exit(1)