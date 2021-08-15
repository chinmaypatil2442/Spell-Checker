
# =============================================================================
# Import modules
import socket
import json
import os
import tkinter as tk
from tkinter import messagebox

# =============================================================================

# =============================================================================
# Constants
target_host = '127.0.0.1' # Server IP
target_port = 2005 # Server port

# =============================================================================

# =============================================================================
# Main Code

try:
    
    # Executed when Connect button is presssed
    def main_func():
        if not (input1.get() and input2.get()): # validating empty inputs
            return
        username = input1.get()
        file_path = input2.get()
        if not os.path.exists(os.path.join(os.getcwd(),file_path)): # checking if file exists on the given path
            messagebox.showinfo("Error","Error: File not found.")
            # print('File not found.')
            return
        else:
            with open(file_path,'r') as f: # opening and reading input file
                file_data = f.read().split()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
                s.connect((target_host, target_port)) # connecting to socket with ip and port
                # print(f'Connected to HOST: {target_host} and PORT: {target_port}')
                request_str = json.dumps({"name":username,"data":file_data}) # json stringify name and file contents
                s.send(request_str.encode()) # convert string to bytes and send data
                messagebox.showinfo("Success","Success: Connection established. File uploaded.")
                # print('Request Sent')
                response = s.recv(1024) # receive server response with buffer size of 1024 bytes
                response_object = json.loads(response.decode()) # convert received bytes to string to json
                # print(f'Response:\n {response_object}')
            
            if response_object['is_error']==True: # check for error from response object
                messagebox.showinfo("Error",f'Error: {response_object["error_message"]}')
                # print(f'Error: {response_object["error_message"]}')
            else:
                with open(f'{os.path.basename(file_path).split(".")[0]}_processed.txt','w') as f: # write recevied data to a file
                    f.write(response_object['file_data'])
                messagebox.showinfo("Success",f'Success: File saved as {os.path.basename(file_path).split(".")[0]}_processed.txt')
            
            input1.delete(0,tk.END) # clear input
            input2.delete(0,tk.END) # clear input
    
    window = tk.Tk() # create window
    window.title('Client')
    tk.Label(window, text='Enter Username: ').grid(row=0) # create label
    tk.Label(window, text='Enter file path: ').grid(row=1) # create label
    
    
    
    
    
    input1 = tk.Entry(window) # create input
    input2 = tk.Entry(window) # create input
    
    
    input1.grid(row=0, column=1) # position input
    input2.grid(row=1, column=1) # position input
    
    # create button
    tk.Button(window, text='Connect', command=main_func).grid(row=2, column=1, sticky=tk.W, pady=4)
    
    
        
    tk.mainloop() # run the main loop of window
    
    
                    
except socket.error as e: # cath socket exceptions
    print(e)  

# =============================================================================


