
# =============================================================================
# Import modules
import socket
import json
import os
import tkinter as tk
from tkinter import messagebox
import threading

# =============================================================================

# =============================================================================
# Constants
target_host = '127.0.0.1' # Server IP
target_port = 2005 # Server port
lex_list = []
thread_list = []
username = ''
# =============================================================================

# =============================================================================
# Main Code

try:
    
    # Executed when Connect button is presssed
    def spell_check():
        global s
        
        if not (input1.get() and input2.get()): # validating empty inputs
            return
        username = input1.get()
        file_path = input2.get()
        
        if not os.path.exists(os.path.join(os.getcwd(),file_path)): # checking if file exists on the given path
            messagebox.showinfo("Error","Error: File not found.")
            return
        else:
            with open(file_path,'r') as f: # opening and reading input file
                file_data = f.read().split()           
              
                request_str = json.dumps({"call":"spell_check","name":username,"data":file_data}) # json stringify name and file contents
                s.send(request_str.encode()) # convert string to bytes and send data                


                # response = s.recv(1024) # receive server response with buffer size of 1024 bytes
                # response_object = json.loads(response.decode()) # convert received bytes to string to json
            
            # if response_object['is_error']==True: # check for error from response object
            #     messagebox.showinfo("Error",f'Error: {response_object["error_message"]}')
            # else:
            #     with open(f'{os.path.basename(file_path).split(".")[0]}_processed.txt','w') as f: # write recevied data to a file
            #         f.write(response_object['file_data'])
            #     messagebox.showinfo("Success",f'Success: File saved as {os.path.basename(file_path).split(".")[0]}_processed.txt')
            
    
    
    def add_lex():
        global lex_list
        global list_box
        
        if not (input3.get()): # validating empty inputs
            return
        lex = input3.get()
        
        lex_list.append(lex)
        list_box.insert(list_box.size(), lex)
    
        input3.delete(0,tk.END) # clear input
    
    
    def receive_func():
        global s
        global lex_list
        global username
        global list_box

        try:
            while True:
                response = s.recv(1024) # receive server response with buffer size of 1024 bytes
                response_object = json.loads(response.decode()) # convert received bytes to string to json

                if response_object['is_error']==True: # check for error from response object
                    messagebox.showinfo("Error",f'Error: {response_object["error_message"]}')
                elif response_object['req_poll']==True:
                    if len(lex_list):
                        request_str = json.dumps({"name":username,"call":"poll","lex_list":lex_list}) # json stringify request
                        s.send(request_str.encode()) # convert string to bytes and send data
                        lex_list.clear()
                        list_box.delete(0, tk.END)
                else:
                    messagebox.showinfo("Success",f"Success: {response_object['success_message']}")
                    if response_object['file_data'] != '':
                        file_path = input2.get()
                        with open(f'{os.path.basename(file_path).split(".")[0]}_processed.txt','w') as f: # write recevied data to a file
                            f.write(response_object['file_data'])
                        input2.delete(0,tk.END) # clear input
        except:
            print('e')


    def connection():
        global s
        global username
        global receive_thread

        if not (input1.get()): # validating empty inputs
            return
        username = input1.get()
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_host, target_port)) # connecting to socket with ip and port

        receive_thread.start() # start the socket thread

        request_str = json.dumps({"name":username,"call":"connect"}) # json stringify name and file contents
        s.send(request_str.encode()) # convert string to bytes and send data

        connect_button.config(state=tk.DISABLED)

        # response = s.recv(1024) # receive server response with buffer size of 1024 bytes
        # response_object = json.loads(response.decode()) # convert received bytes to string to json

        # if response_object['is_error']==True: # check for error from response object
        #     messagebox.showinfo("Error",f'Error: {response_object["error_message"]}')
    
        # else:
        #     messagebox.showinfo("Success","Success: Connection established.")
    
    def disconnection():
        global s
        
        if not (input1.get()): # validating empty inputs
            return
        username = input1.get()
        
        request_str = json.dumps({"name":username,"call":"disconnect"}) # json stringify name and file contents
        s.send(request_str.encode()) # convert string to bytes and send data
        
        s.close()
        
        input1.delete(0,tk.END) # clear input
        input2.delete(0,tk.END) # clear input
        input3.delete(0,tk.END) # clear input
        
        connect_button.config(state=tk.NORMAL)
        messagebox.showinfo("Success","Success: Disconnected from Server.")
             
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    receive_thread = threading.Thread(target=receive_func) # create a thread for running socket
    receive_thread.setDaemon(True) # close the thread when main thread ends
    
    
    window = tk.Tk() # create window
    window.title('Client')
    tk.Label(window, text='Enter Username: ').grid(row=0) # create label
    tk.Label(window, text='Enter file path: ').grid(row=1) # create label
    tk.Label(window, text='Enter New word: ').grid(row=2) # create label    
    
    input1 = tk.Entry(window) # create input
    input2 = tk.Entry(window) # create input
    input3 = tk.Entry(window) # create input    
    
    input1.grid(row=0, column=1) # position input
    input2.grid(row=1, column=1) # position input
    input3.grid(row=2, column=1) # position input
    
    # create button
    connect_button = tk.Button(window, text='Connect', command=connection)
    connect_button.grid(row=0, column=2, sticky=tk.W)
    tk.Button(window, text='Disconnect', command=disconnection).grid(row=0, column=3, sticky=tk.W)    
    tk.Button(window, text='Submit', command=spell_check).grid(row=1, column=2, sticky=tk.W)
    tk.Button(window, text='Add', command=add_lex).grid(row=2, column=2, sticky=tk.W)
         
    list_box = tk.Listbox(window, width=30) # create list box for display
    list_box.grid(row=3, column=1) # give list box position on the window 
    
    tk.mainloop() # run the main loop of window
    
    
                    
except socket.error as e: # cath socket exceptions
    print(e)  

# =============================================================================


