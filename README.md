# Spell-Checker

1. Server file named, “Server.py”, needs to be executed first, with the command “python Server.py”.
2. The server checks if the “lexicon.txt” file exists in the same directory, if it does then read it else exit with error.
3. Server will bind to the socket with IP-127.0.0.1 and PORT-2005 and wait for connections.
4. The client file named “Client.py” can be run using “python Client.py”. It can be run in
multiple separate terminals at the same time to simulate many clients.
5. The client enters a username and clicks on “Connect” button to send a connection request
to the server.
6. The server will accept the client request. In a separate thread, check if the username already
exists with an active connection, if true then terminate the connection with an error.
7. The client can enter a file path in the second input field and click on Submit button for
Spell Check.
8. The server processes the file data and sends the processed data as a proper response to the
client with a success message. The client will store the file as “<filename>_processed.txt”.
9. The client can make additions to the server lexicon via entering the word in the third input field and click Add button which will put the word in a queue, client can do this as many
times as it wants.
10. The server conducts a poll every 60 seconds with connected clients in which the server
requests the queue of words and adds them to the lexicon if they don’t already exist, also returns a success message for the poll.