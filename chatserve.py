#CS 372 Project 1
#Python Chat Server intended for use with C Chat Client
#Jesse Thoren
#Referenced Lecture 15 for socket programming assistance

from socket import *
import sys
import signal

#Handle SIGINT
def signal_handler_noConn(signal, frame):
    print("\nSignal received, shutting down the server.")
    sys.exit(1)

def signal_handler_Conn(signal, franme):
    print("\nSignal received, closing connection and shutting down server.")
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
def chat(socket, msg_length):
    #Handle SIGINT if it occurs while in chat
    signal.signal(signal.SIGINT,signal_handler_Conn)
    #Stay in chat until '\quit' is typed by server or client
    print("Chat link established.")
    print("Respond with '\quit' to end chat with this user.")
    print("Send a SIGINT to shut down the chat server.")
    while 1:
        sentence = socket.recv(msg_length)
        if len(sentence) <= 0:
            print("Client disconnected.\n")
            socket.close()
            break

        print(sentence.decode('UTF-8'))
        
        response = ""
        while 1:
            response = input("localhost> ")
            if len(response)>=500:
                print("Response must be less than 500 bytes")
                continue
            else:
                break

        if(response == "\quit"):
            socket.close()
            break
        socket.send(bytes(response, 'UTF-8'))
    return

#Main Method
#Set port number
servPortNo = setUpPorts(sys.argv)
print("Port set as", servPortNo)

#Create connection (Referenced lecture 15):
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',servPortNo))
serverSocket.listen(1)

#Set maximum message length as required by project description:
MAX_LENGTH = 500
#Length of handle plus '>'
MAX_HANDLE = 11
#Calculate max amount to receive
MAX_MESSAGE = MAX_LENGTH + MAX_HANDLE

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
    chat(connectionSocket, MAX_MESSAGE)
