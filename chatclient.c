/* CS372 - Project 1
 * C Chat Client
 * Jesse Thoren
 * Referenced www.linuxhowtos.org/C_C++/socket.htm for assistance
 * */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define MAX_LENGTH 500 //max number of bytes in a message
#define MAX_HANDLE 11  //length of handle plus '>'

void error(const char *msg)
{
    perror(msg);
    exit(0);
}

int main(int argc, char *argv[])
{
    int sockfd, clientPort, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    char handle[MAX_HANDLE-1]; //Stores the username of the client
    char message[MAX_LENGTH]; //Stores the message to send to the server
    char nameMessage[MAX_LENGTH + MAX_HANDLE]; //Username added to message

    //Enter user handle
    printf("Enter your handle: ");
    fgets(handle, MAX_HANDLE-1, stdin);
    handle[strcspn(handle, "\n")] = 0;
    
    //Verify there are the correct number of arguments passed to client
    if(argc < 3) {
        fprintf(stderr, "Usage: %s hostname port \n", argv[0]);
        exit(0);
    }
    
    //Get port number for client to connect to
    clientPort = atoi(argv[2]);
    
    //Attempt connection on port
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    
    if (sockfd<0)
        error("ERROR: Could not open socket");
    
    //Get host name (Should be localhost for testing on flip)
    server = gethostbyname(argv[1]);
    
    if (server == NULL) {
        fprintf(stderr, "ERROR: no such host\n");
        exit(0);
    }

    //Establish connection
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr,
            (char *)&serv_addr.sin_addr.s_addr,
            server->h_length);
    serv_addr.sin_port = htons(clientPort);
    if (connect(sockfd,(struct sockaddr *) &serv_addr, sizeof(serv_addr)) <0)
        error("ERROR connecting");

    printf("Now connected to chat server\n");
    
    //Chat loop
    while(1){
        //Get message and format
        printf("%s> ", handle);
    
        memset(message,0, MAX_LENGTH);
        fgets(message,MAX_LENGTH-1,stdin);
        message[strcspn(message, "\n")] = 0;
        
        //Append handle
        memset(nameMessage, 0, MAX_LENGTH + MAX_HANDLE);
        strcpy(nameMessage, handle);
        strcat(nameMessage, "> ");
        strcat(nameMessage, message);
        
        //If we want to sent the quit command, break loop and close sock.
        if(strcmp(message, "\\quit") == 0)
            break;

        //Write message to sock otherwise.
        n = write(sockfd, nameMessage, strlen(nameMessage));
        if (n<0)
            error("ERROR writing to socket");
        
        //Get message from server
        bzero(message,MAX_LENGTH);
        bzero(nameMessage, MAX_LENGTH + MAX_HANDLE);
        //Return error or display message from server
        n = read(sockfd,message, MAX_LENGTH-1);
        if (n<0)
            error("ERROR reading from socket");
        if (n==0)
            error("ERROR Server disconnected");
        strcpy(nameMessage, argv[1]);
        strcat(nameMessage, ">");
        strcat(nameMessage, message);
        printf("%s\n",nameMessage);
    }
    //Close socket and return to command line
    close(sockfd);
    return 0;
}
