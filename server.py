import getopt, sys, random

options = "p:l:"
argumentList = sys.argv[1:]
port = ''
logFile = ''

try:
    arguments, values = getopt.getopt(argumentList, options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s"):
            port = int(currentValue)
        elif currentArgument in ("-p"):
            logFile = currentValue
except getopt.error as err:
    print(str(err))

quotes = []
try:
    quotes = open('quotes.txt', 'r').readlines
    print(quotes)
except FileNotFoundError:
    print('Quotes file could not be read.')
    sys.exit(1)

# create a socket and check for errors
try:
    server_socket = socket.socket()
    server_socket.bind("0.0.0.0", port)
    server_socket.listen(5)

while(1):
    conn, address = server_socket.accept()

    req = conn.recv(1024)
    req = req.decode('utf-8')

    if 'network' in req:
        res = random.choice(quotes)
        conn.send(res.encode('utf-8'))
# log the returned message
        file = open("{0}.txt".format(logFile), "a")
        file.write("{0}\n".format(recieved))
        file.close()
        print("Returned to client:  {0}".format(recieved))

    else:
        conn.send("Invalid key word".encode('utf-8'))

    conn.close()

except socket.timeout:
    print("No response.")
    sys.exit(1)

except socket.error as err:
    print(str(err))
    sys.exit(1)