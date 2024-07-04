import customtkinter as ctk
from tkinter import messagebox
import random
import string
import socket
import threading

# Define the colors
colors = {
    "background": "#FAF3F3",  # Light pastel pink
    "primary": "#81D4FA",  # Light blue
    "secondary": "#B3E5FC",  # Lighter blue
    "accent": "#FF7043",  # Coral
    "text": "#333333",  # Dark grey
    "border": "#D3D3D3",  # Light grey
    "input_area": "#E1BEE7",  # Lavender
    "display_area": "#E0F7FA",  # Light cyan
    "button": "#F06292",  # Pink
}

# QKD simulation functions
def generate_key(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def simulate_error_rate():
    return random.uniform(0, 0.1)

def detect_eavesdropping(error_rate):
    return error_rate > 0.8

def encrypt_message(message, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key))

def decrypt_message(encrypted, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(encrypted, key))

# Global variables
server_ip = '127.0.0.1'  # Replace with server IP if different
server_port = 12345
server_socket = None
client_socket = None

# Function to start the server
def start_server():
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        threading.Thread(target=accept_clients, daemon=True).start()
        connection_status.configure(text=f"Server started at {server_ip}:{server_port}", text_color=colors["text"])

        print("Server started, waiting for connections...")
    except Exception as e:
        print(f"Failed to start server: {e}")
        connection_status.configure(text=f"Failed to start server: {e}", text_color="red")
        messagebox.showerror("Error", f"Failed to start server: {e}")

# Function to accept client connections
def accept_clients():
    global client_socket, connection_status
    while True:
        try:
            conn, address = server_socket.accept()  # type: ignore 
            client_socket = conn
            connection_status.configure(text=f"Connected to {address}", text_color=colors["text"])
            print(f"Connected to {address}")
            threading.Thread(target=receive_messages).start()
        except Exception as e:
            print(f"Error accepting clients: {e}")
            break

# Function to receive messages from the client
def receive_messages():
    global client_socket, connection_status
    while True:
        try:
            if client_socket:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                display_message(f"Friend: {data}", sent=False) ###
        except Exception as e:
            print(f"Error receiving message: {str(e)}")
            break
        
    # Client has disconnected
    connection_status.configure(text="Client disconnected", text_color="red")
    client_socket.close()   # type: ignore
    client_socket = None

# Function to clear chat
def clear_chat():
    scrollable_chat.configure(state='normal')
    scrollable_chat.delete(1.0, ctk.END)
    scrollable_chat.configure(state='disabled')

# Function to show help message
def show_help():
    help_text = """
    Quantum Key Distribution (QKD) is a method for securely sharing cryptographic keys using the principles of quantum mechanics. It leverages properties such as superposition and entanglement to ensure that any attempt to intercept the key distribution will be detected.

    Key aspects of QKD:
    - Key Generation: Quantum properties are used to generate a random key.
    - Key Distribution: The key is distributed between the sender and receiver using quantum signals.
    - Security: Detection mechanisms ensure that any eavesdropping attempts are detectable.

    This app simulates the secure message exchange using QKD principles.
    """
    messagebox.showinfo("Help - Quantum Key Distribution (QKD)", help_text)

# Function to exit the chat application
def exit_chat():
    if server_socket:
        server_socket.close()
    if client_socket:
        client_socket.close()
    root.destroy()

# Function to send messages from GUI
def send_message():
    message = input_field.get()
    if message:
        key = generate_key(len(message))
        error_rate = simulate_error_rate()
        eavesdropping_detected = detect_eavesdropping(error_rate)
        connection_secure = not eavesdropping_detected
        encrypted_message = encrypt_message(message, key)

        key_label.configure(text=f"Key: {key}")
        error_rate_label.configure(text=f"Error Rate: {error_rate:.2%}")
        eavesdropping_label.configure(text=f"Eavesdropping Detected: {'Yes' if eavesdropping_detected else 'No'}")
        connection_label.configure(text=f"Connection Secure: {'Yes' if connection_secure else 'No'}")
        encrypt_message_label.configure(text=f"Encrypted Message: {encrypted_message}")

        display_message(f"You: {message}", sent=True)
        
        if eavesdropping_detected:
            display_message("Error: Eavesdropping detected, message cannot be decrypted.", sent=False)
        else:
            decrypted_message = decrypt_message(encrypted_message, key)
            display_message(f"Decrypted: {decrypted_message}", sent=False)

        if client_socket:
            try:
                client_socket.send(encrypted_message.encode())
            except Exception as e:
                display_message(f"Error sending message: {e}", sent=True)
        else:
            display_message("Error: Not connected to client", sent=True)

    input_field.delete(0, 'end')

# Function to display messages in the GUI
def display_message(message, sent):
    scrollable_chat.configure(state='normal')
    scrollable_chat.insert(ctk.END, f"{message}\n", ('sent' if sent else 'received'))
    scrollable_chat.configure(state='disabled')
    scrollable_chat.yview(ctk.END)

# GUI setup
root = ctk.CTk()
root.title("QKD Secured Messaging App")
root.geometry("800x800")
root.configure(fg_color=colors["background"])

# Header
header = ctk.CTkFrame(root, fg_color=colors["primary"], height=50)
header.pack(side="top", fill="x", padx=10, pady=10)

app_name = ctk.CTkLabel(header, text="QKD Messaging App (Server)", text_color=colors["text"], font=("Urbanist", 20, "bold"))
app_name.pack(side="left", padx=20, pady=15)

help_button = ctk.CTkButton(header, text="Help", fg_color=colors["accent"], text_color=colors["background"], font=("Urbanist", 12, "bold"), command=show_help)
help_button.pack(side="right", padx=20)

# Information area
info_area = ctk.CTkFrame(root, fg_color=colors["background"])
info_area.pack(side="top", fill="x", padx=10, pady=10)

key_label = ctk.CTkLabel(info_area, text="Key: ", text_color=colors["text"], font=("Urbanist", 14))
key_label.pack(anchor="w", padx=20)

error_rate_label = ctk.CTkLabel(info_area, text="Error Rate: ", text_color=colors["text"], font=("Urbanist", 14))
error_rate_label.pack(anchor="w", padx=20)

eavesdropping_label = ctk.CTkLabel(info_area, text="Eavesdropping Detected: ", text_color=colors["text"], font=("Urbanist", 14))
eavesdropping_label.pack(anchor="w", padx=20)

connection_label = ctk.CTkLabel(info_area, text="Connection Secure: ", text_color=colors["text"], font=("Urbanist", 14))
connection_label.pack(anchor="w", padx=20)

encrypt_message_label = ctk.CTkLabel(info_area, text="Encrypted Message: ", text_color=colors["text"], font=("Urbanist", 14))
encrypt_message_label.pack(anchor="w", padx=20)

# Chat Area
chat_area = ctk.CTkFrame(root, fg_color=colors["display_area"], corner_radius=10)
chat_area.pack(side="top", fill="both", padx=10, pady=10, expand=True)

scrollable_chat = ctk.CTkTextbox(chat_area, fg_color=colors["display_area"], text_color=colors["text"], wrap=ctk.WORD, state='disabled', font=("Urbanist", 16), corner_radius=10)
scrollable_chat.pack(fill="both", expand=True, padx=10, pady=10)

# Input Area
input_area = ctk.CTkFrame(root, fg_color=colors["input_area"], corner_radius=10)
input_area.pack(side="top", fill="x", padx=10, pady=10)

connection_area = ctk.CTkFrame(input_area, fg_color=colors["input_area"])
connection_area.pack(anchor="w", padx=5)

# Connection status
connection_status = ctk.CTkLabel(connection_area, text="Waiting for connection...", text_color=colors["text"], font=("Urbanist", 14), anchor= "w")
connection_status.pack(side="bottom", padx=10, pady=10)

input_field = ctk.CTkEntry(input_area, fg_color=colors["input_area"], text_color=colors["text"], font=("Urbanist", 16), corner_radius=10)
input_field.pack(side="top", fill="x", padx=10, pady=10, expand=True)

button_frame = ctk.CTkFrame(input_area, fg_color=colors["input_area"])
button_frame.pack(side="top", fill="x", padx=10, pady=10)

send_button = ctk.CTkButton(button_frame, text="Send", fg_color=colors["button"], text_color=colors["background"], font=("Urbanist", 16), corner_radius=10, command=send_message)
send_button.pack(side="left", padx=5, pady=5)

clear_button = ctk.CTkButton(button_frame, text="Clear Chat", fg_color=colors["button"], text_color=colors["background"], font=("Urbanist", 16), corner_radius=10, command=clear_chat)
clear_button.pack(side="left", padx=5, pady=5)

exit_button = ctk.CTkButton(button_frame, text="Exit Chat", fg_color=colors["button"], text_color=colors["background"], font=("Urbanist", 16), corner_radius=10, command=exit_chat)
exit_button.pack(side="right", padx=5, pady=5)

# Start server
start_server()

root.mainloop()
