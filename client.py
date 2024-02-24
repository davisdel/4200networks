import getopt, sys

print('Making connection.')
argumentList = sys.argv[1:]
options = "s:p:l:"
try:
    arguments, values = getopt.getopt(argumentList, options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-s"):
            print(currentValue)
        elif currentArgument in ("-p"):
            print(currentValue)
except getopt.error as err:
    print(str(err))
print('Done.')