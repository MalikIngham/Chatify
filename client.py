'''Tkinter GUI chat client'''

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

def recieve():
    '''Handles message receiving'''

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: #if client leaves chat
            break

def send(event=None):
    '''Handles the sending of messages'''

    msg = my_msg.get()
    my_msg.set("") #Empties input field
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event = None):
    '''Function called when the window is closed'''

    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chatify")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() #For messages to be sent
my_msg.set("Type your message here.")
scrollbar = tkinter.Scrollbar(messages_frame) #Navigates through older messages

msg_list = tkinter.Listbox(messages_frame,height = 15, width = 50, yscrollcommand = scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill = tkinter.Y)
msg_list.pack(side=tkinter.LEFT,fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top,textvariable = my_msg)
entry_field.bind("<Return>",send)
entry_field.pack()
send_button = tkinter.Button(top,text = "Send", command = send)
send_button.pack()

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000 #default port
else:
    PORT = int(PORT) #converts the user input to an int

BUFSIZ = 1024
ADDR = (HOST,PORT)
client_socket = socket(AF_INET,SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread= Thread(target=recieve)
receive_thread.start()
tkinter.mainloop()