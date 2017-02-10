#CS 372 Project 1
#Jesse Thoren

from socket import *
import sys
import signal

#Handle SIGINT
def signal_handler_noConn(signal, frame):
    print("\nSignal received, shutting down the server.")
    sys.exit(1)

def signal_handler_Conn(signal, franme):
    print("\nSignal received, closing connection and shutting down server.")
    servResponse = serverHandle + "has terminated the server." 
    connectionSocket.send(servResponse)
    connectionSocket.close()
    sys.exit(1)

#Get server port number from command line.
def setUpPorts(arguments):
    servPortNo = ""

    #Check if port number is included
    if len(arguments)==1:
        print("\nUsage: python3 chatserve.py portNumber\n")
        sys.exit(0)

    #Try to set port number to first argument from command line
    try: 
        servPortNo = int(arguments[1])
        #If outside of range raise exception
        if servPortNo < 0 or servPortNo > 65535:
            raise Exception()

    #Quit if an invalid port number occurs
    except:
        print("\nUsage: python3 chatserve.py portNumber")
        print("Error: portNumber must be an integer in [0, 65535]")
        print(" Hint: For best success, make the port number between 30000 and 65535\n")
        sys.exit(0)

    return servPortNo

#Chat implementation
def chat(handle, socket, msg_length):
    #Handle SIGINT if it occurs while in chat
    signal.signal(signal.SIGINT,signal_handler_Conn)
    #Stay in chat until '\quit' is typed by server or client
    print("Chat link established.")
    print("Respond with '\quit' to end chat with this user.")
    print("Send a SIGINT to shut down the chat server.")
    while 1:
        sentence = socket.recv(msg_length)
        print(sentence)

        response = input(handle, ">")
        if(response == "\quit"):
            servResponse = handle + " has left the chat."
            socket.send(servResponse)
            socket.close()
            break
        servResponse = handle + ">" + response
        socket.send(servResponse)
    return

#Main Method
#Set port number
servPortNo = setUpPorts(sys.argv)
print("Port set as", servPortNo)

#Get server's handle from user.
serverHandle = input("Enter the chat server's handle: ")
serverHandle = serverHandle[:10]
print("Handle set to: ", serverHandle)

#Create connection (Referenced lecture 15):
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',servPortNo))
serverSocket.listen(1)

#Set maximum message length as required by project description:
MAX_LENGTH = 500

#Exchange information with client
while 1:
    #Set up connectionless signal handler
    signal.signal(signal.SIGINT,signal_handler_noConn)
    #Inform user that server is waiting for connection
    print("The server is ready to receive.")
    print("Send a SIGINT to terminate the chat server.")
    #Wait for connection until SIGINT is received
    connectionSocket, addr = serverSocket.accept()
    #Initiate chat with connection
    chat(serverHandle, connectionSocket, MAX_LENGTH)
