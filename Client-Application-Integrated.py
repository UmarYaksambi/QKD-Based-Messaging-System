import customtkinter as ctk
from tkinter import messagebox
import numpy as np
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

# Global variables
eavesdropper = False
server_ip = '127.0.0.1'  # Hotspot IP 192.168.107.13
server_port = 12345
client_socket = None
num_bits = 64
eavesdropping_probability = 0.3
bob_bits = np.random.randint(0, 2, num_bits, dtype=np.uint8)
bob_bases = np.random.randint(0, 2, num_bits, dtype=np.uint8)
alice_bases = np.zeros(num_bits, dtype=np.uint8)
eve_bits = np.zeros(num_bits, dtype=np.uint8)
KEY = np.zeros(num_bits, dtype=int)
error_rate = 0
error_limit = 10

# Eavesdrop check
def eavesdrop_and_measure(bob_bits, bob_bases, num_bits, eavesdropping_probability):
    global error_rate  # Ensure error_rate is updated globally
    eaves_bits = np.zeros(num_bits, dtype=int)
    eaves_bases = np.random.randint(0, 2, num_bits)
    intercepted = (np.random.rand(num_bits) < eavesdropping_probability)
    
    error_count = 0
    
    for i in range(num_bits):
        if intercepted[i]:
            if eaves_bases[i] == bob_bases[i]:
                eaves_bits[i] = bob_bits[i]
            else:
                eaves_bits[i] = np.random.randint(0, 2)
                error_count += 1  # Increment error count for mismatched bases

    if not eavesdropper:
        error_rate = np.round(np.random.uniform(3, 10), 2)
    else:
        error_rate = np.round(np.random.uniform(8,20 ), 2)

    return eaves_bits, eaves_bits, error_rate

def generate_key(alice_bases, bob_bases):
    global KEY, error_rate  # Ensure KEY and error_rate are updated globally
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            KEY[i] = bob_bits[i]

    # Update GUI key label
    key_label.configure(text=f"Key: {''.join(map(str, KEY))}")

def encrypt_message(message, key):
    key = bytearray(key)  # Convert key to mutable bytearray
    encrypted = bytearray(message.encode())
    
    # Perform XOR encryption
    for i in range(len(encrypted)):
        encrypted[i] ^= key[i % len(key)]
    
    return encrypted

def decrypt_message(ciphertext, key):
    key = bytearray(key)  # Convert key to mutable bytearray
    decrypted = bytearray(ciphertext)
    
    # Perform XOR decryption
    for i in range(len(decrypted)):
        decrypted[i] ^= key[i % len(key)]
    
    return decrypted.decode()

# Function to handle connection to server
def connect_to_server():
    global client_socket, num_bits, alice_bases, eve_bits
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            connection_status.configure(text=f"Connected to ('{server_ip}',{server_port})", text_color=colors["text"])

            # Receive initial messages from server
            num_bits_data = client_socket.recv(4)
            num_bits = int.from_bytes(num_bits_data, byteorder='big')
            
            alice_bases_data = client_socket.recv(num_bits)
            alice_bases = np.frombuffer(alice_bases_data, dtype=np.uint8)
            
            eve_bits_data = client_socket.recv(num_bits)
            eve_bits = np.frombuffer(eve_bits_data, dtype=np.uint8)
            
            # Send Bob's bases to server
            client_socket.sendall(bob_bases.tobytes())

            # Check for eavesdropping and update the error rate
            eaves_bits, eaves_bits, error_rate = eavesdrop_and_measure(bob_bits, bob_bases, num_bits, eavesdropping_probability)
            
            # Update GUI labels
            key_label.configure(text=f"Key: {''.join(map(str, KEY))}")
            error_rate_label.configure(text=f"Error Rate: {error_rate:.2f}%")

            # Generate key after receiving Alice's bases
            generate_key(alice_bases, bob_bases)

            threading.Thread(target=receive_messages, daemon=True).start()

            break  # Break the loop once connected

        except Exception as e:
            print(f"Error connecting to server: {e}")
            messagebox.showerror("Error", f"Error connecting to server: {e}")

# Function to receive messages from the server
def receive_messages():
    global client_socket, KEY, num_bits, alice_bases, eve_bits, error_rate
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            # Assuming the data is a message from Alice after key exchange
            decrypted_message = decrypt_message(data, KEY)
            display_message(f"Alice: {decrypted_message}", sent=False)

        except Exception as e:
            print(f"Error receiving message: {e}")
            break
        
    # Connection closed or error occurred
    messagebox.showinfo("Disconnected", "Server disconnected.")
    connection_status.configure(text="Server disconnected", text_color="red")
    client_socket.close()  # type: ignore
    client_socket = None

# Function to send messages to the server
def send_message():
    message = input_field.get()
    if message:
        eavesdropping_detected = (error_rate > error_limit)
        connection_secure = not eavesdropping_detected
        encrypted_message = encrypt_message(message, KEY)

        # Convert encrypted message to a displayable string format (hex)
        encrypted_message_display = encrypted_message.hex()

        key_label.configure(text=f"Key: {''.join(map(str, KEY))}")
        error_rate_label.configure(text=f"Error Rate: {error_rate:.2f}%")
        eavesdropping_label.configure(text=f"Eavesdropping Detected: {'Yes' if eavesdropping_detected else 'No'}")
        connection_label.configure(text=f"Connection Secure: {'Yes' if connection_secure else 'No'}")
        encrypt_message_label.configure(text=f"Encrypted Message: {encrypted_message_display}")

        display_message(f"You: {message}", sent=True)
        
        if eavesdropping_detected:
            display_message("Error: Eavesdropping detected, message cannot be sent.", sent=False)
        else:
            if client_socket:
                try:
                    client_socket.send(encrypted_message)
                    input_field.delete(0, 'end')

                except Exception as e:
                    display_message(f"Error sending message: {e}", sent=True)
            else:
                display_message("Error: Not connected to server", sent=True)

# Function to display messages in the GUI
def display_message(message, sent):
    scrollable_chat.configure(state='normal')
    scrollable_chat.insert(ctk.END, f"{message}\n", ('sent' if sent else 'received'))
    scrollable_chat.configure(state='disabled')
    scrollable_chat.yview(ctk.END)

# Function to clear chat
def clear_chat():
    scrollable_chat.configure(state='normal')
    scrollable_chat.delete(1.0, ctk.END)
    scrollable_chat.configure(state='disabled')

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
    if client_socket:
        client_socket.close()
    root.destroy()

# GUI setup
root = ctk.CTk()
root.title("QKD Secured Messaging App - Client")
root.geometry("800x800")
root.configure(fg_color=colors["background"])

# Header
header = ctk.CTkFrame(root, fg_color=colors["primary"], height=50)
header.pack(side="top", fill="x", padx=10, pady=10)

app_name = ctk.CTkLabel(header, text="QKD Messaging App (Client)", text_color=colors["text"], font=("Urbanist", 20, "bold"))
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

# Button actions
send_button.configure(command=send_message)
clear_button.configure(command=clear_chat)
exit_button.configure(command=exit_chat)

# Connect to server on startup
threading.Thread(target=connect_to_server, daemon=True).start()

root.mainloop()
