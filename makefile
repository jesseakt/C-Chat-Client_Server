compile: chatclient.c 
	gcc -o client chatclient.c

clean: 
	$(RM) client
