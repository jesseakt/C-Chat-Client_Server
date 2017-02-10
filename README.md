# CS372-project1

Jesse Thoren
Project 1
CS 372

In order to run the chat program, do the following.

1. Extract all files to test directory on flip.
2. Run the makefile by entering "make" into the command line.
3. Execute the chat server with the command:
      python3 chatserve.py [portNumber]
   The port number will take a value between 0 and 65535.
   I have tested the files with ports around 30000.
4. Execute the chat client with the command:
      client localhost [portNumber]
   When testing on flip, the server will be localhost.
   Make sure to choose the same portNumber you entered for the server.
5. Enter a handle on the client.
6. Messages will now alternate between the client and the server.
   You can terminate the chat by entering '\quit' into either the client
   or the server. The client will terminate the process, and the server will
   revert to accepting new connections.
