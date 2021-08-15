# Spell-Checker

1.	Server file named, “Server.py”, needs to be executed first, with the command “python  Server.py”. 
2.	The server checks if the “lexicon.txt” file exists in the same directory, if it does then read it else exit with error.
3.	Server will bind to the socket with IP-127.0.0.1 and PORT-2005 and wait for connections.
4.	The client file named “Client.py” can be run using “python Client.py“. It can be run in multiple separate terminals at the same time to simulate many clients.
5.	The client will be asked for username and file path, after entering these it will read the file and send a proper request to the server, if file is not readable or the wrong path is entered an error will be shown instead.
6.	The server will accept the client request. In a separate thread, check if the username already exists with an active connection, if true then terminate the connection with an error else first put to sleep for 3 seconds then process the data.
7.	After processing, the server sends the data as a proper response to the client and terminates the connection with a success message. The client will store the file as “<filename>_processed.txt”
8.	Same will be repeated for each incoming connection
