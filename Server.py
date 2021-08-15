
# =============================================================================
# Import modules
import socket 
import json
import os
import threading
import tkinter as tk
from tkinter import messagebox
import time
# =============================================================================

# =============================================================================
# Constants
TCP_IP = '127.0.0.1' # Server IP
TCP_PORT = 2005 # Server port
BUFFER_SIZE = 1024 # buffer size for socket
thread_counter = 1 # keep count of all the threads
thread_list = [] # add all the threads to the list
lexicon_list = [] # lexicon words list
active_user_list = [] # all the connected users will be added to this list and removed when disconnected
list_box = [] # contains names of all active users for displaying them onto GUI
# =============================================================================

# =============================================================================
# Classes and funtions
class ClientThread(threading.Thread): # initializes and runs a thread, each with separate client connection
 
    def __init__(self,connection,ip,port,thread_id): 
        threading.Thread.__init__(self) # initialize a thread
        self.connection = connection
        self.ip = ip 
        self.port = port 
        self.thread_id = thread_id
        
    def run(self): 
        global lexicon_list
        global active_user_list
        global list_box
        
        while True:
            try:
                request = self.connection.recv(BUFFER_SIZE) # receive data from the connection
                request_str = request.decode() # convert byte data to string
                request_json = json.loads(request_str) # convert string to json
                
                if request_json['call'] == 'connect':
                    thread_skip_flag = False
                    for index,active_user_obj in enumerate(active_user_list):
                        if active_user_obj['status'] == 'Active' and active_user_obj['name'] == request_json['name']: # check if username already exists
                            response_obj = response(error_message='Username already in use. Please pick a different username.',is_error=True) # prepare response from response class
                            response_str = json.dumps(vars(response_obj)) # convert json to string
                            self.connection.sendall(response_str.encode()) # convert string to bytes and send data to client 
                            self.connection.close() # close the connection
                            thread_skip_flag = True
                            break
                    if thread_skip_flag == True:
                        break
                    else:
                        response_obj = response(is_error=False,success_message='Connection established.') # prepare response from response class
                        response_str = json.dumps(vars(response_obj)) # convert json to string
                        self.connection.sendall(response_str.encode()) # convert string to bytes and send data to client 
                        active_user_list.append({"name":request_json['name'],"status":"Active","conn":self.connection}) # append to active users list
                        list_box.insert(thread_counter,request_json['name']) # add to list box for display
                        list_box.update() # updating the list box view
                

                elif request_json['call'] == 'spell_check':
                    proc_list = [] #  for output
                    append_flag = False # false meaning word not found in lexicon and append to list normally, true meaning word found append bracketed word to processed list
                    for word2 in request_json['data']: # loop over recevied file data
                        for word1 in lexicon_list: # loop over lexicon words list
                            if word1 == word2.lower(): # check if word matches ignoring the case
                                proc_list.append(word2.replace(word2, f"[{word2}]")) # bracket the word and add to processed list
                                append_flag = True
                                break
                        if append_flag == False: # check if the word was added already
                            proc_list.append(word2)
                        append_flag = False
                    
                    proc_str = ' '.join(proc_list) # convert list to string
                    response_obj = response(file_data=proc_str, success_message='Spell Check Completed.') # prepare response with processed data
                    response_str = json.dumps(vars(response_obj)) # convert json to string
                    self.connection.sendall(response_str.encode()) # convert sting to byte and send to the client
                
                elif request_json['call'] == 'poll':
                    add_lex_list = request_json['lex_list']
                    for lex in add_lex_list:
                        if lex not in lexicon_list:
                            lexicon_list.append(lex.lower())
                    response_obj = response(success_message=f'Poll successfully received:\n{add_lex_list}') # prepare response with processed data
                    response_str = json.dumps(vars(response_obj)) # convert json to string
                    self.connection.sendall(response_str.encode()) # convert sting to byte and send to the client

                elif request_json['call'] == 'disconnect':  
                    self.connection.close() # clost the connection
                    for index,active_user_obj in enumerate(active_user_list):
                        if active_user_obj['name'] == request_json['name']: # find the client name
                            active_user_list.pop(index) # remove the client from active list
                            break
                    
                    for index,item in enumerate(list_box.get(0,tk.END)):
                        if item == request_json['name']: # find the client name
                            list_box.delete(index) # remove the client name from display list
                            list_box.update() # update list box view
                            break
                    break
            except:
                # messagebox.showinfo("Error",'Thread-{self.thread_id}: Connection Terminated Abruptly.') # show error if any error occurs
                self.connection.close() # close the connection

class response: # response model
     def __init__(self, file_data='', error_message='', is_error=False, req_poll=False, success_message=''):
        self.file_data = file_data
        self.error_message = error_message
        self.is_error = is_error
        self.req_poll = req_poll
        self.success_message = success_message


def sock_func():
    global thread_list
    global thread_counter
   
    while True: 
        try:
            Server.listen(3) # maintain at max 3 connections
            (conn, (ip,port)) = Server.accept() # # accept all incoming connections
            new_thread = ClientThread(conn,ip,port,thread_counter) # assign a new thread for each of the connection
            thread_counter += 1
            new_thread.setDaemon(True) # close the thread when main thread ends
            new_thread.start() # start the newly assigned thread, executes the run function of the class
            thread_list.append(new_thread) # add to thread list 
        except:
            messagebox.showinfo("Error",'Error: Something went wrong. Shutting down server.')
            break # break loop in case of any exception

    Server.close() # clost the socket

def poll_func():
    global thread_list
    global active_user_list

    while True: 
        try:
            time.sleep(60)
            for connection in active_user_list:
                response_obj = response(req_poll=True) # prepare response from response class
                response_str = json.dumps(vars(response_obj)) # convert json to string
                connection['conn'].sendall(response_str.encode()) # convert string to bytes and send data to client 
        except:
            messagebox.showinfo("Error",'Error: Something went wrong.')
            break # break loop in case of any exception    


# =============================================================================

# =============================================================================
# Main code
try:
    if os.path.exists('lexicon.txt'): # check if lexicon file exists
        with open('lexicon.txt','r') as f: # open lexicon file
            lexicon_list = f.read().lower().split() # read, lowercase and split the data of the file into list
    else:
        messagebox.showinfo("Error",'Error: "lexicon.txt" File not found.') # show file not found error
        os._exit(os.EX_OK) # exit

    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    Server.bind((TCP_IP, TCP_PORT)) # start the socket

    socket_thread = threading.Thread(target=sock_func) # create a thread for running socket
    socket_thread.setDaemon(True) # close the thread when main thread ends
    socket_thread.start() # start the socket thread
    thread_list.append(socket_thread) # add to thread list

    poll_thread = threading.Thread(target=poll_func) # create a thread for running socket
    poll_thread.setDaemon(True) # close the thread when main thread ends
    poll_thread.start() # start the socket thread
    thread_list.append(poll_thread) # add to thread list


    window = tk.Tk() # create window
    window.title('Server')
    tk.Label(window, text=f"Socket Info: IP-{TCP_IP} PORT-{TCP_PORT}\n Waiting for connections...\nConnected Devices:").grid(row=0) # create label
    list_box = tk.Listbox(window) # create list box for display
    list_box.grid(row=1) # give list box position on the window
    tk.mainloop() # run the main loop of window

    Server.close() # clost the socket

    if os.path.exists('lexicon.txt'): # check if lexicon file exists
        with open('lexicon.txt','w+') as f: # open lexicon file
            text = ''
            for word in lexicon_list:
                text = text + word + ' '
            f.write(text) # write, the data to the file

except:
    print('Shutting Down')

# =============================================================================


