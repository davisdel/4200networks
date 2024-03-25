import getopt, sys, random, socket

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
quotes = []

# get options from the run command
try:
    arguments, values = getopt.getopt(argumentList, options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-p"):
            port = int(currentValue)
        elif currentArgument in ("-l"):
            logFile = currentValue
except getopt.error as err:
    print_cmd(str(err))
    sys.exit(1)

# read in quotes list
try:
    quotes = open('quotes.txt', 'r').readlines()
except FileNotFoundError:
    print_cmd('Quotes file could not be read.')
    sys.exit(1)

try:
    # create a socket
    server_socket = socket.socket()
    # bind the socket and listen
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print_cmd("Listening on port {0}".format(port))

    while(1):
        # accept new connection
        conn, address = server_socket.accept()

        # recieve and decode message
        req = conn.recv(1024)
        req = req.decode('utf-8')
        print_cmd("Recieved from ({1}) client:  {0}".format(req,address))

    # check if the message is "network"
        if 'network' == req:
            res = random.choice(quotes)
            conn.send(res.encode('utf-8'))
    # log the returned message
            print_cmd("Returned to client:  {0}".format(res))

        else:
            conn.send("Invalid key word".encode('utf-8'))

    conn.close()

except socket.error as err:
    print_cmd(str(err))
    sys.exit(1)